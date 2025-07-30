import argparse
import os
import statistics
import json
from collections import defaultdict, Counter
from shapely.geometry import Point, Polygon
from tqdm import tqdm
from vgrid.dggs import s2
import pandas as pd
import geopandas as gpd
from vgrid.binning.bin_helper import get_default_stats_structure, append_stats_value
from vgrid.conversion.latlon2dggs import latlon2s2
from vgrid.utils.antimeridian import fix_polygon


def process_input_data(data, lat_col="lat", lon_col="lon", delimiter=None, **kwargs):
    """
    Process input data and extract point features for binning.
    
    Args:
        data: Input data in one of the following formats:
            - File path (str): Path to vector file (shapefile, GeoJSON, CSV, TXT, etc.)
            - URL (str): URL to vector data
            - pandas.DataFrame: DataFrame with geometry or lat/lon columns
            - geopandas.GeoDataFrame: GeoDataFrame
            - dict: GeoJSON dictionary
            - list: List of GeoJSON feature dictionaries
        lat_col (str): Name of latitude column for CSV/DataFrame (default 'lat')
        lon_col (str): Name of longitude column for CSV/DataFrame (default 'lon')
        delimiter (str, optional): Delimiter for text files (default: infer from extension)
        **kwargs: Additional arguments for pandas/geopandas read functions
    Returns:
        pd.DataFrame or gpd.GeoDataFrame: DataFrame with Point geometry column
    Raises:
        ValueError: If input data type is not supported or conversion fails
    """
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
        # Accept .csv, .txt, .tsv, or any delimited text file
        if ext in [".csv", ".txt", ".tsv"]:
            # Infer delimiter if not provided
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


def s2_bin(data, resolution, stats, category=None, numeric_field=None, lat_col="lat", lon_col="lon", **kwargs):
    """
    Bin point data into S2 grid cells and compute statistics.
    Args:
        data: Input data in various formats (DataFrame, GeoDataFrame, file path, etc.)
        resolution (int): S2 resolution level [0..30]
        stats (str): Statistic to compute
        category (str, optional): Category field for grouping
        numeric_field (str, optional): Numeric field to compute statistics (required if stats != 'count')
        lat_col (str): Name of latitude column for CSV/DataFrame (default 'lat')
        lon_col (str): Name of longitude column for CSV/DataFrame (default 'lon')
        **kwargs: Additional arguments for pandas/geopandas read functions
    Returns:
        pd.DataFrame: DataFrame with S2 cell stats and geometry
    """
    # Process input data to GeoDataFrame
    gdf = process_input_data(data, lat_col=lat_col, lon_col=lon_col, **kwargs)
    s2_bins = defaultdict(lambda: defaultdict(get_default_stats_structure))

    for _, row in tqdm(gdf.iterrows(), total=len(gdf), desc="Binning points"):
        geom = row.geometry
        props = row.to_dict()
        if geom is None:
            continue
        if geom.geom_type == "Point":
            s2_token = latlon2s2(geom.y, geom.x, resolution)
            append_stats_value(s2_bins, s2_token, props, stats, category, numeric_field)
        elif geom.geom_type == "MultiPoint":
            for p in geom.geoms:
                s2_token = latlon2s2(p.y, p.x, resolution)
                append_stats_value(s2_bins, s2_token, props, stats, category, numeric_field)

    records = []
    for s2_token, categories in s2_bins.items():
        s2_id = s2.CellId.from_token(s2_token)
        s2_cell = s2.Cell(s2_id)
        vertices = [s2_cell.get_vertex(i) for i in range(4)]
        shapely_vertices = []
        for vertex in vertices:
            lat_lng = s2.LatLng.from_point(vertex)
            longitude = lat_lng.lng().degrees
            latitude = lat_lng.lat().degrees
            shapely_vertices.append((longitude, latitude))
        shapely_vertices.append(shapely_vertices[0])
        cell_polygon = fix_polygon(Polygon(shapely_vertices))
        if not cell_polygon.is_valid:
            continue
        row_data = {
            "s2": s2_token,
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
    """
    Convert GeoDataFrame to various output formats.

    Args:
        result (gpd.GeoDataFrame): GeoDataFrame with S2 cell stats and geometry
        output_format (str): Output output_format ('geojson', 'gpkg', 'parquet', 'csv', 'shapefile')
        output_path (str, optional): Output file path. If None, uses default naming

    Returns:
        gpd.GeoDataFrame or str: Output in the specified output_format or file path

    Raises:
        ValueError: If output output_format is not supported
    """
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

    # Set default output_path if not provided
    def get_default_path(ext):
        res = None
        if 'resolution' in result.columns:
            res = result['resolution'].iloc[0]
        else:
            res = 'unknown'
        return f"s2bin_{res}.{ext}"

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


def s2bin(
    data,
    resolution,
    stats,
    category=None,
    numeric_field=None,
    output_format=None,
    output_path=None,
    **kwargs,
):
    """
    Bin point data into S2 grid cells and compute statistics from various input formats.

    This is the main function that handles binning of point data to S2 grid cells.
    It supports multiple input formats including file paths, URLs, DataFrames, GeoDataFrames,
    GeoJSON dictionaries, and lists of features.

    Args:
        data: Input data in one of the following formats:
            - File path (str): Path to vector file (shapefile, GeoJSON, etc.)
            - URL (str): URL to vector data
            - pandas.DataFrame: DataFrame with geometry column
            - geopandas.GeoDataFrame: GeoDataFrame
            - dict: GeoJSON dictionary
            - list: List of GeoJSON feature dictionaries
        resolution (int): S2 resolution level [0..30] (0=coarsest, 30=finest)
        stats (str): Statistic to compute:      
            - 'count': Count of points in each cell
            - 'sum': Sum of field values
            - 'min': Minimum field value
            - 'max': Maximum field value
            - 'mean': Mean field value
            - 'median': Median field value
            - 'std': Standard deviation of field values
            - 'var': Variance of field values
            - 'range': Range of field values
            - 'minority': Least frequent value
            - 'majority': Most frequent value
            - 'variety': Number of unique values
        category (str, optional): Category field for grouping statistics
        numeric_field (str, optional): Numeric field to compute statistics (required if stats != 'count')
        output_format (str, optional): Output output_format ('geojson', 'gpkg', 'parquet', 'csv', 'shapefile')
        output_path (str, optional): Output file path. If None, uses default naming
        **kwargs: Additional arguments passed to geopandas read functions

    Returns:
        dict or str: Output in the specified output_format. Returns file path if output_path is specified,
        otherwise returns the data directly.

    Raises:
        ValueError: If input data type is not supported or conversion fails
        TypeError: If resolution is not an integer

    Example:
        >>> # Bin from file
        >>> result = s2bin("cities.shp", 10, "count")
        
        >>> # Bin from GeoDataFrame
        >>> import geopandas as gpd
        >>> gdf = gpd.read_file("cities.shp")
        >>> result = s2bin(gdf, 10, "mean", numeric_field="population")
        
        >>> # Bin from GeoJSON dict
        >>> geojson = {"type": "FeatureCollection", "features": [...]}
        >>> result = s2bin(geojson, 10, "sum", numeric_field="value")
    """
    if not isinstance(resolution, int):
        raise TypeError(f"Resolution must be an integer, got {type(resolution).__name__}")

    if resolution < 0 or resolution > 30:
        raise ValueError(f"Resolution must be in range [0..30], got {resolution}")

    if stats != "count" and not numeric_field:
        raise ValueError("A numeric_field is required for statistics other than 'count'")

    # Process input data and bin
    result_gdf = s2_bin(data, resolution, stats, category, numeric_field, **kwargs)
    
    # Convert to output output_format if specified
    return convert_to_output_format(result_gdf, output_format, output_path)


def s2bin_cli():
    """
    Command-line interface for s2bin conversion.

    This function provides a command-line interface for binning point data to S2 grid cells.
    It parses command-line arguments and calls the main s2bin function.

    Usage:
        python s2bin.py -i input.shp -r 10 -stats count -f geojson -o output.geojson

    Arguments:
        -i, --input: Input file path, URL, or other vector file formats
        -r, --resolution: S2 resolution [0..30]
        -stats, --statistics: Statistic to compute (count, min, max, sum, mean, median, std, var, range, minority, majority, variety)
        -category, --category: Optional category field for grouping
        -field, --field: Numeric field to compute statistics (required if stats != 'count')
        -o, --output: Output file path (optional, will auto-generate if not provided)
        -f, --output_format: Output output_format (geojson, gpkg, parquet, csv, shapefile)

    Example:
        >>> # Bin shapefile to S2 cells at resolution 10 with count statistics
        >>> # python s2bin.py -i cities.shp -r 10 -stats count -f geojson
    """
    parser = argparse.ArgumentParser(description="Binning point data to S2 DGGS")
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
        default=13,
        help="Resolution of the grid [0..30]",
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
        # Use the s2bin function
        result = s2bin(
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
    s2bin_cli()
