import argparse
import os
import re
import json
import statistics
from collections import defaultdict, Counter
from shapely.geometry import Point, Polygon
from tqdm import tqdm
from vgrid.binning.bin_helper import get_default_stats_structure, append_stats_value
from vgrid.generator.settings import graticule_dggs_to_feature
from vgrid.conversion.latlon2dggs import latlon2tilecode
from vgrid.dggs import mercantile
import pandas as pd
import geopandas as gpd

def process_input_data(data, lat_col="lat", lon_col="lon", delimiter=None, **kwargs):
    if isinstance(data, gpd.GeoDataFrame):
        return data
    elif isinstance(data, pd.DataFrame):
        if "geometry" in data.columns:
            return gpd.GeoDataFrame(data, geometry="geometry", crs="EPSG:4326")
        elif lat_col in data.columns and lon_col in data.columns:
            gdf = gpd.GeoDataFrame(
                data.copy(),
                geometry=gpd.points_from_xy(data[lon_col], data[lat_col]),
                crs="EPSG:4326",
            )
            return gdf
        else:
            raise ValueError(f"DataFrame must have either a 'geometry' column or '{lat_col}' and '{lon_col}' columns.")
    elif isinstance(data, list):
        gdf = gpd.GeoDataFrame.from_features(data)
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif isinstance(data, dict) and "type" in data:
        if data["type"] == "FeatureCollection":
            gdf = gpd.GeoDataFrame.from_features(data["features"])
            gdf.set_crs(epsg=4326, inplace=True)
            return gdf
        elif data["type"] == "Feature":
            gdf = gpd.GeoDataFrame.from_features([data])
            gdf.set_crs(epsg=4326, inplace=True)
            return gdf
        else:
            raise ValueError(f"Unsupported GeoJSON type: {data['type']}")
    elif isinstance(data, str):
        ext = os.path.splitext(data)[1].lower()
        if ext in [".csv", ".txt", ".tsv"]:
            if delimiter is None:
                if ext == ".tsv":
                    delimiter = "\t"
                else:
                    delimiter = ","
            df = pd.read_csv(data, delimiter=delimiter, **kwargs)
            if lat_col in df.columns and lon_col in df.columns:
                gdf = gpd.GeoDataFrame(
                    df.copy(),
                    geometry=gpd.points_from_xy(df[lon_col], df[lat_col]),
                    crs="EPSG:4326",
                )
                return gdf
            else:
                raise ValueError(f"Tabular file must have columns '{lat_col}' and '{lon_col}'")
        else:
            gdf = gpd.read_file(data, **kwargs)
            return process_input_data(gdf, lat_col=lat_col, lon_col=lon_col)
    else:
        raise ValueError(f"Unsupported input type: {type(data)}")

def tilecode_bin(data, resolution, stats, category=None, numeric_field=None, lat_col="lat", lon_col="lon", **kwargs):
    gdf = process_input_data(data, lat_col=lat_col, lon_col=lon_col, **kwargs)
    tilecode_bins = defaultdict(lambda: defaultdict(get_default_stats_structure))
    for _, row in tqdm(gdf.iterrows(), total=len(gdf), desc="Binning points"):
        geom = row.geometry
        props = row.to_dict()
        if geom is None:
            continue
        if geom.geom_type == "Point":
            tilecode_id = latlon2tilecode(geom.y, geom.x, resolution)
            append_stats_value(tilecode_bins, tilecode_id, props, stats, category, numeric_field)
        elif geom.geom_type == "MultiPoint":
            for p in geom.geoms:
                tilecode_id = latlon2tilecode(p.y, p.x, resolution)
                append_stats_value(tilecode_bins, tilecode_id, props, stats, category, numeric_field)
    records = []
    for tilecode_id, categories in tilecode_bins.items():
        match = re.match(r"z(\d+)x(\d+)y(\d+)", tilecode_id)
        z = int(match.group(1))
        x = int(match.group(2))
        y = int(match.group(3))
        bounds = mercantile.bounds(x, y, z)
        min_lat, min_lon = bounds.south, bounds.west
        max_lat, max_lon = bounds.north, bounds.east
        cell_polygon = Polygon(
            [
                [min_lon, min_lat],
                [max_lon, min_lat],
                [max_lon, max_lat],
                [min_lon, max_lat],
                [min_lon, min_lat],
            ]
        )
        if not cell_polygon.is_valid:
            continue
        row_data = {
            "tilecode": tilecode_id,
            "geometry": cell_polygon,
            "resolution": resolution,
        }
        for cat, values in categories.items():
            key_prefix = "" if category is None else f"{cat}_"
            if stats == "count":
                row_data[f"{key_prefix}count"] = values["count"]
            elif stats == "sum":
                row_data[f"{key_prefix}sum"] = sum(values["sum"])
            elif stats == "min":
                row_data[f"{key_prefix}min"] = min(values["min"])
            elif stats == "max":
                row_data[f"{key_prefix}max"] = max(values["max"])
            elif stats == "mean":
                row_data[f"{key_prefix}mean"] = statistics.mean(values["mean"])
            elif stats == "median":
                row_data[f"{key_prefix}median"] = statistics.median(values["median"])
            elif stats == "std":
                row_data[f"{key_prefix}std"] = statistics.stdev(values["std"]) if len(values["std"]) > 1 else 0
            elif stats == "var":
                row_data[f"{key_prefix}var"] = statistics.variance(values["var"]) if len(values["var"]) > 1 else 0
            elif stats == "range":
                row_data[f"{key_prefix}range"] = max(values["range"]) - min(values["range"]) if values["range"] else 0
            elif stats == "minority":
                freq = Counter(values["values"])
                min_item = min(freq.items(), key=lambda x: x[1])[0] if freq else None
                row_data[f"{key_prefix}minority"] = min_item
            elif stats == "majority":
                freq = Counter(values["values"])
                max_item = max(freq.items(), key=lambda x: x[1])[0] if freq else None
                row_data[f"{key_prefix}majority"] = max_item
            elif stats == "variety":
                row_data[f"{key_prefix}variety"] = len(set(values["values"]))
        records.append(row_data)
    result_gdf = gpd.GeoDataFrame(records, geometry="geometry", crs="EPSG:4326")
    return result_gdf

def convert_to_output_format(result, output_format, output_path=None):
    if result.empty:
        print("Warning: No features found in result. This may happen when:")
        print("  - No point features were found in the input data")
        print("  - Input geometry contains no valid Point or MultiPoint features")
        print("Suggestions:")
        print("  - Check that input data contains Point or MultiPoint geometries")
        print("  - Verify that input file can be read properly")
        raise ValueError("No features found in result")
    if 'geometry' in result.columns:
        result.set_geometry('geometry', inplace=True)
    else:
        geom_cols = [col for col in result.columns if hasattr(result[col].iloc[0], 'geom_type')]
        if geom_cols:
            result.set_geometry(geom_cols[0], inplace=True)
        else:
            raise ValueError("No geometry column found in GeoDataFrame")
        if result.empty:
            raise ValueError("GeoDataFrame is empty")
        if not result.geometry.is_valid.all():
            print("Warning: Some geometries are invalid")
    def get_default_path(ext):
        res = None
        if 'resolution' in result.columns:
            res = result['resolution'].iloc[0]
        else:
            res = 'unknown'
        return f"tilecodebin_{res}.{ext}"
    if output_format is None:
        return result
    if output_format.lower() == "geojson":
        if output_path is None:
            return result.to_json()
        result.to_file(output_path, driver="GeoJSON")
        return output_path
    elif output_format.lower() == "gpkg":
        if output_path is None:
            output_path = get_default_path("gpkg")
        result.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format.lower() == "parquet":
        if output_path is None:
            output_path = get_default_path("parquet")
        result.to_parquet(output_path, index=False)
        return output_path
    elif output_format.lower() == "csv":
        if output_path is None:
            return result.to_csv(index=False)
        result.to_csv(output_path, index=False)
        return output_path
    elif output_format.lower() == "shapefile":
        if output_path is None:
            output_path = get_default_path("shp")
        result.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    else:
        raise ValueError(
            f"Unsupported output output_format: {output_format}. Supported formats: geojson, gpkg, parquet, csv, shapefile"
        )

def tilecodebin(
    data,
    resolution,
    stats,
    category=None,
    numeric_field=None,
    output_format=None,
    output_path=None,
    **kwargs,
):
    if not isinstance(resolution, int):
        raise TypeError(f"Resolution must be an integer, got {type(resolution).__name__}")
    if resolution < 0 or resolution > 29:
        raise ValueError(f"Resolution must be in range [0..29], got {resolution}")
    if stats != "count" and not numeric_field:
        raise ValueError("A numeric_field is required for statistics other than 'count'")
    result_gdf = tilecode_bin(data, resolution, stats, category, numeric_field, **kwargs)
    return convert_to_output_format(result_gdf, output_format, output_path)

def tilecodebin_cli():
    parser = argparse.ArgumentParser(description="Binning point data to Tilecode DGGS")
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help="Input data: GeoJSON file path, URL, or other vector file formats",
    )
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        default=15,
        help="Resolution of the grid [0..29]",
    )
    parser.add_argument(
        "-stats",
        "--statistics",
        choices=[
            "count",
            "min",
            "max",
            "sum",
            "mean",
            "median",
            "std",
            "var",
            "range",
            "minority",
            "majority",
            "variety",
        ],
        required=True,
        help="Statistic option",
    )
    parser.add_argument(
        "-category",
        "--category",
        required=False,
        help="Optional category field for grouping",
    )
    parser.add_argument(
        "-field", "--field", dest="numeric_field", required=False, help="Numeric field to compute statistics (required if stats != 'count')"
    )
    parser.add_argument(
        "-o", "--output", 
        required=False, 
        help="Output file path (optional, will auto-generate if not provided)"
    )
    parser.add_argument(
        "-f", "--output_format",
        required=False,
        default=None,
        choices=["geojson", "gpkg", "parquet", "csv", "shapefile"],
        help="Output output_format (default: None, returns GeoDataFrame)",
    )
    args = parser.parse_args()
    try:
        result = tilecodebin(
            data=args.input,
            resolution=args.resolution,
            stats=args.statistics,
            category=args.category,
            numeric_field=args.numeric_field,
            output_format=args.output_format,
            output_path=args.output,
        )
        if isinstance(result, str):
            print(f"Output saved to {result}")      
    except Exception as e:
        print(f"Error: {str(e)}")
        return

if __name__ == "__main__":
    tilecodebin_cli()
