"""
ISEA4T DGGS Grid Generator Module

This module provides functionality for generating ISEA4T DGGS at various resolutions.

Key Features:
- Generate complete global ISEA4T grids at specified resolutions (0-25)
- Generate ISEA4T grids within specified bounding boxes
- Generate ISEA4T grids that intersect with provided geometries (resampling)
- Export grids in multiple formats (GeoJSON, CSV, Shapefile, GeoPackage, Parquet)
- Handle antimeridian crossing cells appropriately
- Support for Windows platform using EAGGR library
"""

import argparse
import json
from shapely.ops import unary_union
from tqdm import tqdm
from shapely.geometry import Polygon, box, shape
import platform
if platform.system() == "Windows":
    from vgrid.dggs.eaggr.eaggr import Eaggr
    from vgrid.dggs.eaggr.shapes.dggs_cell import DggsCell
    from vgrid.dggs.eaggr.enums.model import Model
    from vgrid.dggs.eaggr.enums.shape_string_format import ShapeStringFormat
    from vgrid.generator.settings import isea4t_res_accuracy_dict
    isea4t_dggs = Eaggr(Model.ISEA4T)

from vgrid.utils.antimeridian import fix_polygon
from vgrid.generator.settings import (
    MAX_CELLS,
    isea4t_base_cells,
    geodesic_dggs_to_feature,
    fix_isea4t_wkt,
    fix_isea4t_antimeridian_cells,
    isea4t_cell_to_polygon
)


def get_isea4t_children_cells(base_cells, target_resolution):
    """
    Recursively generate DGGS cells for the desired resolution.
    """
    current_cells = base_cells
    for res in range(target_resolution):
        next_cells = []
        for cell in current_cells:
            children = isea4t_dggs.get_dggs_cell_children(DggsCell(cell))
            next_cells.extend([child._cell_id for child in children])
        current_cells = next_cells
    return current_cells


def get_isea4t_children_cells_within_bbox(
    bounding_cell, bbox, target_resolution
):
    current_cells = [
        bounding_cell
    ]  # Start with a list containing the single bounding cell
    bounding_resolution = len(bounding_cell) - 2

    for res in range(bounding_resolution, target_resolution):
        next_cells = []
        for cell in current_cells:
            # Get the child cells for the current cell
            children = isea4t_dggs.get_dggs_cell_children(DggsCell(cell))
            for child in children:
                # Convert child cell to geometry
                child_shape = isea4t_cell_to_polygon(child)
                if child_shape.intersects(bbox):
                    # Add the child cell ID to the next_cells list
                    next_cells.append(child._cell_id)
        if not next_cells:  # Break early if no cells remain
            break
        current_cells = (
            next_cells  # Update current_cells to process the next level of children
        )

    return current_cells


def generate_grid(resolution):
    # accuracy = isea4t_res_accuracy_dict.get(resolution)
    children = get_isea4t_children_cells(isea4t_base_cells, resolution)
    isea4t_features = []
    for child in tqdm(children, desc="Generating ISEA4T DGGS", unit=" cells"):
        isea4t_cell = DggsCell(child)
        cell_polygon = isea4t_cell_to_polygon(isea4t_cell)
        isea4t_id = isea4t_cell.get_cell_id()
        num_edges = 3
        if resolution == 0:
            cell_polygon = fix_polygon(cell_polygon)
        elif (
            isea4t_id.startswith("00")
            or isea4t_id.startswith("09")
            or isea4t_id.startswith("14")
            or isea4t_id.startswith("04")
            or isea4t_id.startswith("19")
        ):
            cell_polygon = fix_isea4t_antimeridian_cells(cell_polygon)

        isea4t_feature = geodesic_dggs_to_feature(
            "isea4t", isea4t_id, resolution, cell_polygon, num_edges
        )
        isea4t_features.append(isea4t_feature)

    return {"type": "FeatureCollection", "features": isea4t_features}


def generate_grid_within_bbox(resolution, bbox):
    accuracy = isea4t_res_accuracy_dict.get(resolution)
    bounding_box = box(*bbox)
    bounding_box_wkt = bounding_box.wkt  # Create a bounding box polygon
    isea4t_shapes = isea4t_dggs.convert_shape_string_to_dggs_shapes(
        bounding_box_wkt, ShapeStringFormat.WKT, accuracy
    )
    isea4t_shape = isea4t_shapes[0]
    bbox_cells = isea4t_shape.get_shape().get_outer_ring().get_cells()
    bounding_cell = isea4t_dggs.get_bounding_dggs_cell(bbox_cells)
    bounding_children = get_isea4t_children_cells_within_bbox(
        bounding_cell.get_cell_id(), bounding_box, resolution
    )
    isea4t_features = []
    for child in tqdm(bounding_children, desc="Generating ISEA4T DGGS", unit=" cells"):
        isea4t_cell = DggsCell(child)
        cell_polygon = isea4t_cell_to_polygon(isea4t_cell)
        isea4t_id = isea4t_cell.get_cell_id()
        if resolution == 0:
            cell_polygon = fix_polygon(cell_polygon)

        elif (
            isea4t_id.startswith("00")
            or isea4t_id.startswith("09")
            or isea4t_id.startswith("14")
            or isea4t_id.startswith("04")
            or isea4t_id.startswith("19")
        ):
            cell_polygon = fix_isea4t_antimeridian_cells(cell_polygon)
        num_edges = 3

        # if cell_polygon.intersects(bounding_box):
        isea4t_feature = geodesic_dggs_to_feature(
            "isea4t", isea4t_id, resolution, cell_polygon, num_edges
        )
        isea4t_features.append(isea4t_feature)

    return {"type": "FeatureCollection", "features": isea4t_features}


def generate_grid_resample(resolution, geojson_features):
    accuracy = isea4t_res_accuracy_dict.get(resolution)
    # Step 1: Unify all geometries into a single shape
    geometries = [
        shape(feature["geometry"]) for feature in geojson_features["features"]
    ]
    unified_geom = unary_union(geometries)
    unified_geom_wkt = unified_geom.wkt

    # Step 2: Generate DGGS shapes from WKT geometry
    isea4t_shapes = isea4t_dggs.convert_shape_string_to_dggs_shapes(
        unified_geom_wkt, ShapeStringFormat.WKT, accuracy
    )
    isea4t_shape = isea4t_shapes[0]
    bbox_cells = isea4t_shape.get_shape().get_outer_ring().get_cells()
    bounding_cell = isea4t_dggs.get_bounding_dggs_cell(bbox_cells)

    # Step 3: Generate children cells within geometry bounds
    bounding_children = get_isea4t_children_cells_within_bbox(
        bounding_cell.get_cell_id(), unified_geom, resolution
    )

    isea4t_features = []
    for child in tqdm(bounding_children, desc="Generating ISEA4T DGGS", unit=" cells"):
        isea4t_cell = DggsCell(child)
        cell_polygon = isea4t_cell_to_polygon(isea4t_cell)
        isea4t_id = isea4t_cell.get_cell_id()

        if resolution == 0:
            cell_polygon = fix_polygon(cell_polygon)
        elif isea4t_id.startswith(("00", "09", "14", "04", "19")):
            cell_polygon = fix_isea4t_antimeridian_cells(cell_polygon)

        num_edges = 3

        # Optional: only include cells intersecting original geometry
        if not cell_polygon.intersects(unified_geom):
            continue

        isea4t_feature = geodesic_dggs_to_feature(
            "isea4t", isea4t_id, resolution, cell_polygon, num_edges
        )
        isea4t_features.append(isea4t_feature)

    return {"type": "FeatureCollection", "features": isea4t_features}


def convert_isea4tgrid_output_format(isea4t_features, output_format=None, output_path=None, resolution=None):
    if not isea4t_features:
        return []
    def default_path(ext):
        return f"isea4t_grid_{resolution}.{ext}" if resolution is not None else f"isea4t_grid.{ext}"
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import shape
    if output_format is None:
        return [f["properties"]["isea4t"] for f in isea4t_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in isea4t_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(isea4t_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(isea4t_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(isea4t_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(isea4t_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(isea4t_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(isea4t_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def isea4tgrid_cli():
    parser = argparse.ArgumentParser(description="Generate Open-Eaggr ISEA4T DGGS.")
    parser.add_argument(
        "-r", "--resolution", type=int, required=True, help="Resolution [0..25]"
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
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of ISEA4T IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    if platform.system() == "Windows":
        args = parser.parse_args()
        if args.output_format == "None":
            args.output_format = None
        resolution = args.resolution
        bbox = args.bbox if args.bbox else [-180, -90, 180, 90]
        if resolution < 0 or resolution > 25:
            print("Please select a resolution in [0..25] range and try again ")
            return
        if bbox == [-180, -90, 180, 90]:
            total_cells = 20 * (4**resolution)
            print(f"Resolution {resolution} will generate {total_cells} cells ")
            if total_cells > MAX_CELLS:
                print(f"which exceeds the limit of {MAX_CELLS}.")
                print("Please select a smaller resolution and try again.")
                return
            isea4t_features = generate_grid(resolution)
        else:
            isea4t_features = generate_grid_within_bbox(resolution, bbox)
        try:
            result = convert_isea4tgrid_output_format(isea4t_features, args.output_format, args.output, resolution)
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


def isea4tgrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate ISEA4T grid for pure Python usage (Windows only).

    Args:
        resolution (int): ISEA4T resolution [0..25]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output output_format ('geojson', 'csv', etc). Defaults to None (list of IDs).
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict, str, list, or GeoDataFrame: Output in the requested output_format.
    """
    if platform.system() != "Windows":
        raise RuntimeError("ISEA4T grid generation is only supported on Windows due to EAGGR dependency")
    if not isinstance(resolution, int):
        raise TypeError(f"Resolution must be an integer, got {type(resolution).__name__}")
    if resolution < 0 or resolution > 25:
        raise ValueError("Resolution must be in range [0..25]")
    if bbox is None:
        bbox = [-180, -90, 180, 90]
        total_cells = 20 * (4 ** resolution)
        if total_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution {resolution} will generate {total_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
        isea4t_features = generate_grid(resolution)
    else:
        isea4t_features = generate_grid_within_bbox(resolution, bbox)
    return convert_isea4tgrid_output_format(isea4t_features, output_format, output_path, resolution)


if __name__ == "__main__":
    isea4tgrid_cli()
