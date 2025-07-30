"""
Maidenhead DGGS Grid Generator Module
Reference:
    https://github.com/ha8tks/Leaflet.Maidenhead
    https://ha8tks.github.io/Leaflet.Maidenhead/examples/
    https://www.sotamaps.org/
"""

import json
import math
import argparse
from vgrid.dggs import maidenhead
import geopandas as gpd
import pandas as pd
from tqdm import tqdm
from vgrid.generator.settings import MAX_CELLS, graticule_dggs_to_feature
from shapely.geometry import shape, Polygon
from vgrid.stats.maidenheadstats import maidenhead_metrics


def generate_grid(resolution):
    if resolution == 1:
        lon_width, lat_width = 20, 10
    elif resolution == 2:
        lon_width, lat_width = 2, 1
    elif resolution == 3:
        lon_width, lat_width = 0.083333, 0.041666  # 5 minutes x 2.5 minutes
    elif resolution == 4:
        lon_width, lat_width = 0.008333, 0.004167  # 30 seconds x 15 seconds
    else:
        raise ValueError("Unsupported resolution")

    # Determine the bounding box
    min_lon, min_lat, max_lon, max_lat = [-180, -90, 180, 90]
    x_cells = int((max_lon - min_lon) / lon_width)
    y_cells = int((max_lat - min_lat) / lat_width)
    total_cells = x_cells * y_cells

    maidenhead_features = []
    with tqdm(total=total_cells, desc="Generating Maidenhead DGGS", unit=" cells") as pbar:
        for i in range(x_cells):
            for j in range(y_cells):
                cell_min_lon = min_lon + i * lon_width
                cell_max_lon = cell_min_lon + lon_width
                cell_min_lat = min_lat + j * lat_width
                cell_max_lat = cell_min_lat + lat_width

                cell_center_lat = (cell_min_lat + cell_max_lat) / 2
                cell_center_lon = (cell_min_lon + cell_max_lon) / 2
                maidenhead_id = maidenhead.toMaiden(cell_center_lat, cell_center_lon, resolution)
                _, _, min_lat_maiden, min_lon_maiden, max_lat_maiden, max_lon_maiden, _ = maidenhead.maidenGrid(maidenhead_id)
                # Define the polygon based on the bounding box
                cell_polygon = Polygon([
                    [min_lon_maiden, min_lat_maiden],  # Bottom-left corner
                    [max_lon_maiden, min_lat_maiden],  # Bottom-right corner
                    [max_lon_maiden, max_lat_maiden],  # Top-right corner
                    [min_lon_maiden, max_lat_maiden],  # Top-left corner
                    [min_lon_maiden, min_lat_maiden]   # Closing the polygon (same as the first point)
                ])
                maidenhead_feature = graticule_dggs_to_feature('maidenhead',maidenhead_id,resolution,cell_polygon)
                maidenhead_features.append(maidenhead_feature)
                pbar.update(1)

    return {
        "type": "FeatureCollection",
        "features": maidenhead_features
    }

def generate_grid_within_bbox(resolution, bbox):
    # Define the grid parameters based on the resolution
    if resolution == 1:
        lon_width, lat_width = 20, 10
    elif resolution == 2:
        lon_width, lat_width = 2, 1
    elif resolution == 3:
        lon_width, lat_width = 0.083333, 0.041666  # 5 minutes x 2.5 minutes
    elif resolution == 4:
        lon_width, lat_width = 0.008333, 0.004167  # 30 seconds x 15 seconds
    else:
        raise ValueError("Unsupported resolution")

    min_lon, min_lat, max_lon, max_lat = bbox

    # Calculate grid cell indices for the bounding box
    base_lat, base_lon = -90, -180
    start_x = math.floor((min_lon - base_lon) / lon_width)
    end_x = math.floor((max_lon - base_lon) / lon_width)
    start_y = math.floor((min_lat - base_lat) / lat_width)
    end_y = math.floor((max_lat - base_lat) / lat_width)

    maidenhead_features = []

    total_cells = (end_x - start_x + 1) * (end_y - start_y + 1)

    # Loop through all intersecting grid cells with tqdm progress bar
    with tqdm(total=total_cells, desc="Generating Maidenhead DGGS") as pbar:
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                # Calculate the cell bounds
                cell_min_lon = base_lon + x * lon_width
                cell_max_lon = cell_min_lon + lon_width
                cell_min_lat = base_lat + y * lat_width
                cell_max_lat = cell_min_lat + lat_width

                # Ensure the cell intersects with the bounding box
                if not (cell_max_lon < min_lon or cell_min_lon > max_lon or
                        cell_max_lat < min_lat or cell_min_lat > max_lat):
                    # Center point for the Maidenhead code
                    cell_center_lat = (cell_min_lat + cell_max_lat) / 2
                    cell_center_lon = (cell_min_lon + cell_max_lon) / 2
                    
                    maidenhead_id = maidenhead.toMaiden(cell_center_lat, cell_center_lon, resolution)
                    _, _, min_lat_maiden, min_lon_maiden, max_lat_maiden, max_lon_maiden, _ = maidenhead.maidenGrid(maidenhead_id)
                    # Define the polygon based on the bounding box
                    cell_polygon = Polygon([
                        [min_lon_maiden, min_lat_maiden],  # Bottom-left corner
                        [max_lon_maiden, min_lat_maiden],  # Bottom-right corner
                        [max_lon_maiden, max_lat_maiden],  # Top-right corner
                        [min_lon_maiden, max_lat_maiden],  # Top-left corner
                        [min_lon_maiden, min_lat_maiden]   # Closing the polygon (same as the first point)
                    ])
                    
                    maidenhead_feature = graticule_dggs_to_feature('maidenhead',maidenhead_id,resolution,cell_polygon)            
                 
                    maidenhead_features.append(maidenhead_feature)

                pbar.update(1)

    return {
        "type": "FeatureCollection",
        "features": maidenhead_features
    }
   

def convert_maidenheadgrid_output_format(maidenhead_features, output_format=None, output_path=None, resolution=None):
    if not maidenhead_features:
        return []
    def default_path(ext):
        return f"maidenhead_grid_{resolution}.{ext}" if resolution is not None else f"maidenhead_grid.{ext}"
    if output_format is None:
        return [f["properties"]["maidenhead"] for f in maidenhead_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in maidenhead_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(maidenhead_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(maidenhead_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(maidenhead_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(maidenhead_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(maidenhead_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(maidenhead_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def maidenheadgrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate Maidenhead grid for pure Python usage.

    Args:
        resolution (int): Maidenhead resolution [1..4]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output format ('geojson', 'csv', etc.). Defaults to None (list of Maidenhead IDs).
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict, list, or str: Output depending on output_format
    """
    if resolution not in [1, 2, 3, 4]:
        raise ValueError("Resolution must be in [1, 2, 3, 4]")

    if bbox is None:
        bbox = [-180, -90, 180, 90]
        num_cells, _, _ = maidenhead_metrics(resolution)
        if num_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution {resolution} will generate {num_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
        maidenhead_features = generate_grid(resolution)
    else:
        maidenhead_features = generate_grid_within_bbox(resolution, bbox)

    return convert_maidenheadgrid_output_format(maidenhead_features, output_format, output_path, resolution)


def maidenheadgrid_cli():
    parser = argparse.ArgumentParser(description="Generate Maidenhead DGGS")
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        choices=[1, 2, 3, 4],
        default=1,
        help="resolution [1..4]",
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
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of Maidenhead IDs)",
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
        num_cells, _, _ = maidenhead_metrics(resolution)
        print(f"Resolution {resolution} will generate {num_cells} cells ")
        if num_cells > MAX_CELLS:
            print(f"which exceeds the limit of {MAX_CELLS}.")
            print("Please select a smaller resolution and try again.")
            return
        maidenhead_features = generate_grid(resolution)
    else:
        maidenhead_features = generate_grid_within_bbox(resolution, bbox)
    try:
        result = convert_maidenheadgrid_output_format(maidenhead_features, args.output_format, args.output, resolution)
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
    maidenheadgrid_cli()
