"""
EASE DGGS Grid Generator Module
"""
import argparse
import json
from shapely.geometry import Polygon, box
from tqdm import tqdm
from vgrid.dggs.easedggs.constants import grid_spec, ease_crs, geo_crs, levels_specs
from vgrid.dggs.easedggs.dggs.grid_addressing import (
    grid_ids_to_geos,
    geo_polygon_to_grid_ids,
)
from vgrid.generator.settings import MAX_CELLS, geodesic_dggs_to_feature

# Initialize the geodetic model

geo_bounds = grid_spec["geo"]
min_longitude = geo_bounds["min_x"]
min_lattitude = geo_bounds["min_y"]
max_longitude = geo_bounds["max_x"]
max_latitude = geo_bounds["max_y"]


def get_ease_cells(resolution):
    """
    Generate a list of cell IDs based on the resolution, row, and column.
    """
    n_row = levels_specs[resolution]["n_row"]
    n_col = levels_specs[resolution]["n_col"]

    # Generate list of cell IDs
    cell_ids = []

    # Loop through all rows and columns at the specified resolution
    for row in range(n_row):
        for col in range(n_col):
            # Generate base ID (e.g., L0.RRRCCC for res=0)
            base_id = f"L{resolution}.{row:03d}{col:03d}"

            # Add additional ".RC" for each higher resolution
            cell_id = base_id
            for i in range(1, resolution + 1):
                cell_id += f".{row:1d}{col:1d}"  # For res=1: L0.RRRCCC.RC, res=2: L0.RRRCCC.RC.RC, etc.

            # Append the generated cell ID to the list
            cell_ids.append(cell_id)

    return cell_ids


def get_ease_cells_bbox(resolution, bbox):
    bounding_box = box(*bbox)
    bounding_box_wkt = bounding_box.wkt
    cells_bbox = geo_polygon_to_grid_ids(
        bounding_box_wkt,
        level=resolution,
        source_crs=geo_crs,
        target_crs=ease_crs,
        levels_specs=levels_specs,
        return_centroids=True,
        wkt_geom=True,
    )
    return cells_bbox


def generate_grid(resolution):
    ease_features = []

    level_spec = levels_specs[resolution]
    n_row = level_spec["n_row"]
    n_col = level_spec["n_col"]

    cells = get_ease_cells(resolution)

    for cell in tqdm(
        cells, total=len(cells), desc="Generating EASE DGGS", unit=" cells"
    ):
        geo = grid_ids_to_geos([cell])
        center_lon, center_lat = geo["result"]["data"][0]
        cell_min_lat = center_lat - (180 / (2 * n_row))
        cell_max_lat = center_lat + (180 / (2 * n_row))
        cell_min_lon = center_lon - (360 / (2 * n_col))
        cell_max_lon = center_lon + (360 / (2 * n_col))

        cell_polygon = Polygon(
            [
                [cell_min_lon, cell_min_lat],
                [cell_max_lon, cell_min_lat],
                [cell_max_lon, cell_max_lat],
                [cell_min_lon, cell_max_lat],
                [cell_min_lon, cell_min_lat],
            ]
        )
        if cell_polygon:
            num_edges = 4
            ease_feature = geodesic_dggs_to_feature(
                "ease", str(cell), resolution, cell_polygon, num_edges
            )
            ease_features.append(ease_feature)

    return {"type": "FeatureCollection", "features": ease_features}


def generate_grid_within_bbox(resolution, bbox):
    ease_features = []
    level_spec = levels_specs[resolution]
    n_row = level_spec["n_row"]
    n_col = level_spec["n_col"]

    # Get all grid cells within the bounding box
    cells = get_ease_cells_bbox(resolution, bbox)["result"]["data"]

    if cells:
        for cell in tqdm(cells, desc="Generating EASE DGGS", unit=" cells"):
            geo = grid_ids_to_geos([cell])
            if geo:
                center_lon, center_lat = geo["result"]["data"][0]
                cell_min_lat = center_lat - (180 / (2 * n_row))
                cell_max_lat = center_lat + (180 / (2 * n_row))
                cell_min_lon = center_lon - (360 / (2 * n_col))
                cell_max_lon = center_lon + (360 / (2 * n_col))

                cell_polygon = Polygon(
                    [
                        [cell_min_lon, cell_min_lat],
                        [cell_max_lon, cell_min_lat],
                        [cell_max_lon, cell_max_lat],
                        [cell_min_lon, cell_max_lat],
                        [cell_min_lon, cell_min_lat],
                    ]
                )
                num_edges = 4
                ease_feature = geodesic_dggs_to_feature(
                    "ease", str(cell), resolution, cell_polygon, num_edges
                )
                ease_features.append(ease_feature)

        return {"type": "FeatureCollection", "features": ease_features}


def convert_easegrid_output_format(ease_features, output_format=None, output_path=None, resolution=None):
    if not ease_features:
        return []
    def default_path(ext):
        return f"ease_grid_{resolution}.{ext}" if resolution is not None else f"ease_grid.{ext}"
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import shape
    if output_format is None:
        return [f["properties"]["ease"] for f in ease_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in ease_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(ease_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(ease_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(ease_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(ease_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(ease_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(ease_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")

def easegrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate EASE grid for pure Python usage.

    Args:
        resolution (int): EASE grid resolution [0..6]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output output_format ('geojson', 'csv', 'geo', 'gpd', 'shapefile', 'gpkg', 'parquet', or None for list of EASE IDs). Defaults to None.
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict, list, or str: Output in the requested output_format (GeoJSON FeatureCollection, list of IDs, file path, etc.)
    """
    if resolution < 0 or resolution > 6:
        raise ValueError("Resolution must be in range [0..6]")

    if bbox is None:
        bbox = [min_longitude, min_lattitude, max_longitude, max_latitude]
        level_spec = levels_specs[resolution]
        n_row = level_spec["n_row"]
        n_col = level_spec["n_col"]
        total_cells = n_row * n_col
        if total_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution {resolution} will generate {total_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
        ease_features = generate_grid(resolution)
    else:
        ease_features = generate_grid_within_bbox(resolution, bbox)
    return convert_easegrid_output_format(ease_features, output_format, output_path, resolution)

def easegrid_cli():
    parser = argparse.ArgumentParser(description="Generate EASE-DGGS DGGS.")
    parser.add_argument(
        "-r", "--resolution", type=int, required=True, help="resolution [0..6]"
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
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of EASE IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    if args.output_format == "None":
        args.output_format = None
    resolution = args.resolution
    bbox = (
        args.bbox
        if args.bbox
        else [min_longitude, min_lattitude, max_longitude, max_latitude]
    )
    if resolution < 0 or resolution > 6:
        print("Please select a resolution in [0..6] range and try again")
        return
    if bbox == [min_longitude, min_lattitude, max_longitude, max_latitude]:
        level_spec = levels_specs[resolution]
        n_row = level_spec["n_row"]
        n_col = level_spec["n_col"]
        total_cells = n_row * n_col
        print(f"Resolution {resolution} will generate {total_cells} cells ")
        if total_cells > MAX_CELLS:
            print(f"which exceeds the limit of {MAX_CELLS}.")
            print("Please select a smaller resolution and try again.")
            return
        ease_features = generate_grid(resolution)
    else:
        ease_features = generate_grid_within_bbox(resolution, bbox)
    try:
        result = convert_easegrid_output_format(ease_features, args.output_format, args.output, resolution)
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
    easegrid_cli()
