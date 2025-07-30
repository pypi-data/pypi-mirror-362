
"""
MGRS Grid Generator Module.

This module provides functionality to generate Military Grid Reference System (MGRS)
Discrete Global Grid System (DGGS) grids. MGRS is a geocoordinate standard used
by NATO militaries for locating points on Earth.

The module supports:
- Generation of MGRS grids for specific Grid Zone Designators (GZD)
- Multiple output formats (GeoJSON, CSV, Shapefile, GeoPackage, Parquet)
- Resolution levels from 0 to 5
- UTM coordinate system transformations

Key Functions:
- generate_grid(): Creates MGRS grid cells for a given GZD and resolution
- convert_mgrsgrid_output_format(): Converts grid data to various output formats
- mgrsgrid_cli(): Command-line interface for grid generation
"""

import argparse

import json
import re
import os
import numpy as np
import geopandas as gpd
from shapely.geometry import shape, Polygon
from shapely.ops import transform
from pyproj import CRS, Transformer
from tqdm import tqdm
from vgrid.generator.settings import graticule_dggs_to_feature
from vgrid.dggs import mgrs


def is_valid_gzd(gzd):
    """Check if a Grid Zone Designator (GZD) is valid."""
    pattern = r"^(?:0[1-9]|[1-5][0-9]|60)[C-HJ-NP-X]$"
    return bool(re.match(pattern, gzd))


def generate_grid(gzd, resolution):  # Define the UTM CRS
    # Reference: https://www.maptools.com/tutorials/utm/details
    cell_size = 100_000 // (10**resolution)
    north_bands = "NPQRSTUVWX"
    south_bands = "MLKJHGFEDC"
    band_distance = 111_132 * 8
    gzd_band = gzd[2]

    if gzd_band >= "N":  # North Hemesphere
        epsg_code = int("326" + gzd[:2])
        min_x, min_y, max_x, max_y = 100000, 0, 900000, 9500000  # for the North
        north_band_idx = north_bands.index(gzd_band)
        max_y = band_distance * (north_band_idx + 1)
        if gzd_band == "X":
            max_y += band_distance  # band X = 12 deggrees instead of 8 degrees

    else:  # South Hemesphere
        epsg_code = int("327" + gzd[:2])
        min_x, min_y, max_x, max_y = 100000, 0, 900000, 10000000  # for the South
        south_band_idx = south_bands.index(gzd_band)
        max_y = band_distance * (south_band_idx + 1)

    utm_crs = CRS.from_epsg(epsg_code)
    wgs84_crs = CRS.from_epsg(4326)
    transformer = Transformer.from_crs(utm_crs, wgs84_crs, always_xy=True).transform

    gzd_json_path = os.path.join(os.path.dirname(__file__), "gzd.geojson")
    with open(gzd_json_path, encoding="utf-8") as f:
        gzd_data = json.load(f)

    gzd_features = gzd_data["features"]
    gzd_feature = [
        feature for feature in gzd_features if feature["properties"].get("gzd") == gzd
    ][0]
    gzd_geom = shape(gzd_feature["geometry"])

    # Create grid polygons
    mgrs_features = []
    x_coords = np.arange(min_x, max_x, cell_size)
    y_coords = np.arange(min_y, max_y, cell_size)
    num_cells = len(x_coords) * len(y_coords)
    with tqdm(total=num_cells, desc="Generating MGRS DGGS", unit=" cells") as pbar:
        for x in x_coords:
            for y in y_coords:
                cell_polygon_utm = Polygon(
                    [
                        (x, y),
                        (x + cell_size, y),
                        (x + cell_size, y + cell_size),
                        (x, y + cell_size),
                        (x, y),  # Close the polygon
                    ]
                )
                cell_polygon = transform(transformer, cell_polygon_utm)

                if cell_polygon.intersects(gzd_geom):
                    centroid_lat, centroid_lon = (
                        cell_polygon.centroid.y,
                        cell_polygon.centroid.x,
                    )
                    mgrs_id = mgrs.toMgrs(centroid_lat, centroid_lon, resolution)
                    mgrs_feature = graticule_dggs_to_feature(
                        "mgrs", mgrs_id, resolution, cell_polygon
                    )
                    # clip inside GZD:
                    if not gzd_geom.contains(cell_polygon):
                        intersected_polygon = cell_polygon.intersection(gzd_geom)
                        if intersected_polygon:
                            intersected_centroid_lat, intersected_centroid_lon = (
                                intersected_polygon.centroid.y,
                                intersected_polygon.centroid.x,
                            )
                            interescted_mgrs_id = mgrs.toMgrs(
                                intersected_centroid_lat,
                                intersected_centroid_lon,
                                resolution,
                            )
                            mgrs_feature = graticule_dggs_to_feature(
                                "mgrs",
                                interescted_mgrs_id,
                                resolution,
                                intersected_polygon,
                            )
                    mgrs_features.append(mgrs_feature)
                pbar.update(1)
    return {"type": "FeatureCollection", "features": mgrs_features}


def convert_mgrsgrid_output_format(
    mgrs_features, output_format=None, output_path=None, resolution=None, gzd=None
):
    if not mgrs_features:
        return []

    def default_path(ext):
        base = (
            f"mgrs_grid_{gzd}_{resolution}"
            if gzd is not None
            else f"mgrs_grid_{resolution}"
        )
        return f"{base}.{ext}"

    if output_format is None:
        return [f["properties"]["mgrs"] for f in mgrs_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in mgrs_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(mgrs_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(mgrs_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(mgrs_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(mgrs_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(mgrs_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(mgrs_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")

def mgrsgrid(gzd, resolution, output_format=None, output_path=None):
    """
    Generate MGRS grid for pure Python usage.

    Args:
        gzd (str): Grid Zone Designator, e.g. '48P'.
        resolution (int): MGRS resolution [0..5].
        output_format (str, optional): Output format ('geojson', 'csv', 'geo', 'gpd', 'shapefile', 'gpkg', 'parquet', or None for list of MGRS IDs). Defaults to None.
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        Depends on output_format: list, GeoDataFrame, file path, or GeoJSON FeatureCollection.
    """
    if not is_valid_gzd(gzd):
        raise ValueError("Invalid GZD. Please input a valid GZD.")
    if resolution < 0 or resolution > 5:
        raise ValueError("Resolution must be in range [0..5].")
    mgrs_features = generate_grid(gzd, resolution)
    return convert_mgrsgrid_output_format(
        mgrs_features, output_format, output_path, resolution, gzd
    )


def mgrsgrid_cli():
    parser = argparse.ArgumentParser(description="Generate MGRS DGGS.")
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        default=0,
        required=True,
        help="Resolution [0..5]",
    )
    parser.add_argument(
        "-gzd",
        type=str,
        default="48P",
        required=True,
        help="GZD - Grid Zone Designator, e.g. 48P",
    )
    parser.add_argument(
        "-f",
        "--output_format",
        type=str,
        choices=["geojson", "csv", "geo", "gpd", "shapefile", "gpkg", "parquet", None],
        default=None,
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of MGRS IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    gzd = args.gzd
    if not is_valid_gzd(gzd):
        print("Invalid GZD. Please input a valid GZD and try again.")
        return
    resolution = args.resolution
    if args.output_format == "None":
        args.output_format = None
    if resolution < 0 or resolution > 5:
        print("Please select a resolution in [0..5] range and try again ")
        return
    mgrs_features = generate_grid(gzd, resolution)
    try:
        result = convert_mgrsgrid_output_format(
            mgrs_features, args.output_format, args.output, resolution, gzd
        )
        if result is None:
            return
        if args.output_format is None:
            print(result)
        elif args.output_format in ["geo", "gpd"]:
            print(result)
        elif args.output_format in [
            "csv",
            "parquet",
            "gpkg",
            "shapefile",
            "geojson",
        ] and isinstance(result, str):
            print(f"Output saved as {result}")
        elif args.output_format == "geojson" and isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print(f"Output saved as {args.output}")
    except ValueError as e:
        print(f"Error: {str(e)}")
        return



if __name__ == "__main__":
    mgrsgrid_cli()
