"""
GARS DGGS Grid Generator Module
"""

import json
import argparse
from tqdm import tqdm
from shapely.geometry import Polygon, box
import numpy as np
from vgrid.dggs.gars.garsgrid import GARSGrid  # Ensure the correct import path

from vgrid.generator.settings import MAX_CELLS, graticule_dggs_to_feature


def get_resolution_minutes(resolution):
    """Convert resolution level to minutes.

    Parameters
    ----------
    resolution : int
        Resolution level (1-4):
        1 = 30 minutes (minimum resolution)
        2 = 15 minutes
        3 = 5 minutes
        4 = 1 minute (maximum resolution)

    Returns
    -------
    int
        Resolution in minutes
    """
    minutes_map = {
        1: 30,  # 30 minutes
        2: 15,  # 15 minutes
        3: 5,  # 5 minutes
        4: 1,  # 1 minute
    }
    return minutes_map[resolution]


def generate_grid(resolution):
    # Default to the whole world if no bounding box is provided
    lon_min, lat_min, lon_max, lat_max = -180, -90, 180, 90

    resolution_minutes = get_resolution_minutes(resolution)
    resolution_degrees = resolution_minutes / 60.0

    # Generate ranges for longitudes and latitudes
    longitudes = np.arange(lon_min, lon_max, resolution_degrees)
    latitudes = np.arange(lat_min, lat_max, resolution_degrees)

    total_cells = len(longitudes) * len(latitudes)

    gars_features = []
    # Loop over longitudes and latitudes with tqdm progress bar
    with tqdm(total=total_cells, desc="Generating GARS DGGS", unit=" cells") as pbar:
        for lon in longitudes:
            for lat in latitudes:
                # Create the GARS grid code
                gars_cell = GARSGrid.from_latlon(lat, lon, resolution_minutes)
                wkt_polygon = gars_cell.polygon

                if wkt_polygon:
                    cell_polygon = Polygon(list(wkt_polygon.exterior.coords))
                    gars_id = gars_cell.gars_id
                    gars_feature = graticule_dggs_to_feature(
                        "gars", gars_id, resolution, cell_polygon
                    )
                    gars_features.append(gars_feature)
                    pbar.update(1)

    # Create a FeatureCollection
    return {
        "type": "FeatureCollection",
        "features": gars_features,
    }


def generate_grid_within_bbox(bbox, resolution):
    # Default to the whole world if no bounding box is provided
    bbox_polygon = box(*bbox)
    lon_min, lat_min, lon_max, lat_max = bbox

    resolution_minutes = get_resolution_minutes(resolution)
    resolution_degrees = resolution_minutes / 60.0

    longitudes = np.arange(
        lon_min - resolution_degrees, lon_max + resolution_degrees, resolution_degrees
    )
    latitudes = np.arange(
        lat_min - resolution_degrees, lat_max + resolution_degrees, resolution_degrees
    )

    gars_features = []
    # Loop over longitudes and latitudes with tqdm progress bar
    with tqdm(desc="Generating GARS DGGS", unit=" cells") as pbar:
        for lon in longitudes:
            for lat in latitudes:
                # Create the GARS grid code
                gars_cell = GARSGrid.from_latlon(lat, lon, resolution_minutes)
                wkt_polygon = gars_cell.polygon

                if wkt_polygon:
                    cell_polygon = Polygon(list(wkt_polygon.exterior.coords))

                    if bbox_polygon.intersects(cell_polygon):
                        gars_id = gars_cell.gars_id
                        gars_feature = graticule_dggs_to_feature(
                            "gars", gars_id, resolution, cell_polygon
                        )
                        gars_features.append(gars_feature)
                        pbar.update(1)

    # Create a FeatureCollection
    return {
        "type": "FeatureCollection",
        "features": gars_features,
    }


def convert_garsgrid_output_format(gars_features, output_format=None, output_path=None, resolution=None):
    if not gars_features:
        return []
    def default_path(ext):
        return f"gars_grid_{resolution}.{ext}" if resolution is not None else f"gars_grid.{ext}"
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import shape
    if output_format is None:
        return [f["properties"]["gars"] for f in gars_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in gars_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(gars_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(gars_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(gars_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(gars_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(gars_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(gars_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def garsgrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate GARS grid for pure Python usage.

    Args:
        resolution (int): GARS resolution [1..4]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output format ('geojson', 'csv', etc.). Defaults to None (list of GARS IDs).
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict, list, or str: Output depending on output_format
    """
    if resolution not in [1, 2, 3, 4]:
        raise ValueError("Resolution must be in [1, 2, 3, 4]")

    if bbox is None:
        lon_min, lat_min, lon_max, lat_max = -180, -90, 180, 90
        resolution_minutes = get_resolution_minutes(resolution)
        resolution_degrees = resolution_minutes / 60.0
        longitudes = np.arange(lon_min, lon_max, resolution_degrees)
        latitudes = np.arange(lat_min, lat_max, resolution_degrees)
        total_cells = len(longitudes) * len(latitudes)
        if total_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution level {resolution} ({resolution_minutes} minutes) will generate {total_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
        gars_features = generate_grid(resolution)
    else:
        gars_features = generate_grid_within_bbox(bbox, resolution)

    return convert_garsgrid_output_format(gars_features, output_format, output_path, resolution)


def garsgrid_cli():
    parser = argparse.ArgumentParser(description="Generate GARS DGGS")
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        choices=[1, 2, 3, 4],
        required=True,
        help="Resolution level (1=30min, 2=15min, 3=5min, 4=1min)",
    )
    parser.add_argument(
        "-b",
        "--bbox",
        type=float,
        nargs=4,
        help="Bounding box in the output_format: min_lon min_lat max_lon max_lat (default is the whole world)",
    )
    parser.add_argument(
        "-f",
        "--output_format",
        type=str,
        choices=["geojson", "csv", "geo", "gpd", "shapefile", "gpkg", "parquet", None],
        default=None,
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of GARS IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    if args.output_format == "None":
        args.output_format = None
    resolution = args.resolution
    bbox = args.bbox if args.bbox else [-180, -90, 180, 90]
    if bbox == [-180, -90, 180, 90]:
        lon_min, lat_min, lon_max, lat_max = -180, -90, 180, 90
        resolution_minutes = get_resolution_minutes(resolution)
        resolution_degrees = resolution_minutes / 60.0
        longitudes = np.arange(lon_min, lon_max, resolution_degrees)
        latitudes = np.arange(lat_min, lat_max, resolution_degrees)
        total_cells = len(longitudes) * len(latitudes)
        print(f"Resolution level {resolution} ({resolution_minutes} minutes) will generate {total_cells} cells ")
        if total_cells > MAX_CELLS:
            print(f"which exceeds the limit of {MAX_CELLS}.")
            print("Please select a smaller resolution and try again.")
            return
        gars_features = generate_grid(resolution)
    else:
        gars_features = generate_grid_within_bbox(bbox, resolution)
    try:
        result = convert_garsgrid_output_format(gars_features, args.output_format, args.output, resolution)
        if result is None:
            return
        if args.output_format is None:
            print(result)
        elif args.output_format in ["geo", "gpd"]:
            print(result)
        elif args.output_format in ["csv", "parquet", "gpkg", "shapefile", "geojson"] and isinstance(result, str):
            print(f"Output saved as {result}")
        elif args.output_format == "geojson" and isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print(f"Output saved as {args.output}")
    except ValueError as e:
        print(f"Error: {str(e)}")
        return


if __name__ == "__main__":
    garsgrid_cli()
