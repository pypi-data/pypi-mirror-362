"""
ISEA3H DGGS Grid Generator Module
"""

import argparse
import json
import platform
from shapely.geometry import box, mapping, Polygon
from tqdm import tqdm

if platform.system() == "Windows":
    from vgrid.dggs.eaggr.eaggr import Eaggr
    from vgrid.dggs.eaggr.shapes.dggs_cell import DggsCell
    from vgrid.dggs.eaggr.enums.model import Model
    from vgrid.dggs.eaggr.enums.shape_string_format import ShapeStringFormat
    isea3h_dggs = Eaggr(Model.ISEA3H)

from vgrid.utils.antimeridian import fix_polygon
from vgrid.generator.settings import (
    MAX_CELLS,
    isea3h_base_cells,
    isea3h_accuracy_res_dict,
    isea3h_res_accuracy_dict,
    isea3h_cell_to_polygon,
)

from pyproj import Geod

geod = Geod(ellps="WGS84")


def get_isea3h_children_cells(base_cells, target_resolution):
    """
    Recursively generate DGGS cells for the desired resolution, avoiding duplicates.
    """
    if platform.system() == "Windows":
        current_cells = base_cells
        seen_cells = set(base_cells)  # Track already processed cells

        for res in range(target_resolution):
            next_cells = []
            for cell in current_cells:
                children = isea3h_dggs.get_dggs_cell_children(DggsCell(cell))
                for child in children:
                    if child._cell_id not in seen_cells:
                        seen_cells.add(child._cell_id)  # Mark as seen
                        next_cells.append(child._cell_id)
            current_cells = next_cells
        return current_cells


def get_isea3h_children_cells_within_bbox(
    bounding_cell, bbox, target_resolution
):
    """
    Recursively generate DGGS cells within a bounding box, avoiding duplicates.
    """
    if platform.system() == "Windows":
        current_cells = [
            bounding_cell
        ]  # Start with a list containing the single bounding cell
        seen_cells = set(current_cells)  # Track already processed cells
        bounding_cell2point = isea3h_dggs.convert_dggs_cell_to_point(
            DggsCell(bounding_cell)
        )
        accuracy = bounding_cell2point._accuracy
        bounding_resolution = isea3h_accuracy_res_dict.get(accuracy)

        if bounding_resolution <= target_resolution:
            for res in range(bounding_resolution, target_resolution):
                next_cells = []
                for cell in current_cells:
                    # Get the child cells for the current cell
                    children = isea3h_dggs.get_dggs_cell_children(DggsCell(cell))
                    for child in children:
                        if (
                            child._cell_id not in seen_cells
                        ):  # Check if the child is already processed
                            child_shape = isea3h_cell_to_polygon(child)
                            if child_shape.intersects(bbox):
                                seen_cells.add(child._cell_id)  # Mark as seen
                                next_cells.append(child._cell_id)
                if not next_cells:  # Break early if no cells remain
                    break
                current_cells = next_cells  # Update current_cells to process the next level of children

            return current_cells
        else:
            # print('Bounding box area is < 0.028 square meters. Please select a bigger bounding box')
            return None


def generate_grid(resolution):
    """
    Generate DGGS cells and convert them to GeoJSON features.
    """
    if platform.system() == "Windows":
        children = get_isea3h_children_cells(isea3h_base_cells, resolution)
        features = []
        for child in tqdm(children, desc="Generating ISEA3H DGGS", unit=" cells"):
            isea3h_cell = DggsCell(child)
            cell_polygon = isea3h_cell_to_polygon(isea3h_cell)
            isea3h_id = isea3h_cell.get_cell_id()

            cell_centroid = cell_polygon.centroid
            center_lat = round(cell_centroid.y, 7)
            center_lon = round(cell_centroid.x, 7)
            cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]), 3)
            cell_perimeter = abs(geod.geometry_area_perimeter(cell_polygon)[1])
            avg_edge_len = round(cell_perimeter / 6, 3)
            if resolution == 0:
                avg_edge_len = round(cell_perimeter / 3, 3)  # icosahedron faces

            features.append(
                {
                    "type": "Feature",
                    "geometry": mapping(cell_polygon),
                    "properties": {
                        "isea3h": isea3h_id,
                        "resolution": resolution,
                        "center_lat": center_lat,
                        "center_lon": center_lon,
                        "cell_area": cell_area,
                        "avg_edge_len": avg_edge_len,
                    },
                }
            )

        return {"type": "FeatureCollection", "features": features}


def generate_grid_within_bbox(resolution, bbox):
    if platform.system() == "Windows":
        accuracy = isea3h_res_accuracy_dict.get(resolution)
        # print(accuracy)
        bounding_box = box(*bbox)
        bounding_box_wkt = bounding_box.wkt  # Create a bounding box polygon
        # print (bounding_box_wkt)
        shapes = isea3h_dggs.convert_shape_string_to_dggs_shapes(
            bounding_box_wkt, ShapeStringFormat.WKT, accuracy
        )
        shape = shapes[0]
        # for shape in shapes:
        bbox_cells = shape.get_shape().get_outer_ring().get_cells()
        bounding_cell = isea3h_dggs.get_bounding_dggs_cell(bbox_cells)
        # print("boudingcell: ", bounding_cell.get_cell_id())
        bounding_children_cells = get_isea3h_children_cells_within_bbox(
            bounding_cell.get_cell_id(), bounding_box, resolution
        )
        # print (bounding_children_cells)
        if bounding_children_cells:
            features = []
            for child in bounding_children_cells:
                isea3h_cell = DggsCell(child)
                cell_polygon = isea3h_cell_to_polygon(isea3h_cell)
                isea3h_id = isea3h_cell.get_cell_id()

                cell_centroid = cell_polygon.centroid
                center_lat = round(cell_centroid.y, 7)
                center_lon = round(cell_centroid.x, 7)
                cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]), 3)
                cell_perimeter = abs(geod.geometry_area_perimeter(cell_polygon)[1])
                avg_edge_len = round(cell_perimeter / 6, 3)
                if resolution == 0:
                    avg_edge_len = round(cell_perimeter / 3, 3)  # icosahedron faces

                # if cell_polygon.intersects(bounding_box):
                features.append(
                    {
                        "type": "Feature",
                        "geometry": mapping(cell_polygon),
                        "properties": {
                            "isea3h": isea3h_id,
                            "resolution": resolution,
                            "center_lat": center_lat,
                            "center_lon": center_lon,
                            "cell_area": cell_area,
                            "avg_edge_len": avg_edge_len,
                        },
                    }
                )

            return {"type": "FeatureCollection", "features": features}


def convert_isea3hgrid_output_format(isea3h_features, output_format=None, output_path=None, resolution=None):
    if not isea3h_features:
        return []
    def default_path(ext):
        return f"isea3h_grid_{resolution}.{ext}" if resolution is not None else f"isea3h_grid.{ext}"
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import shape
    if output_format is None:
        return [f["properties"]["isea3h"] for f in isea3h_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in isea3h_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(isea3h_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(isea3h_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(isea3h_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(isea3h_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(isea3h_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(isea3h_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def isea3hgrid_cli():
    parser = argparse.ArgumentParser(description="Generate Open-Eaggr ISEA3H DGGS.")
    parser.add_argument(
        "-r", "--resolution", type=int, required=True, help="Resolution [0..32]"
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
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of ISEA3H IDs)",
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
        if resolution < 0 or resolution > 32:
            print("Please select a resolution in [0..32] range and try again ")
            return
        if bbox == [-180, -90, 180, 90]:
            total_cells = 20 * (7**resolution)
            print(f"Resolution {resolution} within bounding box {bbox} will generate {total_cells} cells ")
            if total_cells > MAX_CELLS:
                print(f"which exceeds the limit of {MAX_CELLS}. ")
                print("Please select a smaller resolution and try again.")
                return
            isea3h_features = generate_grid(resolution)
        else:
            isea3h_features = generate_grid_within_bbox(resolution, bbox)
        try:
            result = convert_isea3hgrid_output_format(isea3h_features, args.output_format, args.output, resolution)
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


def isea3hgrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate ISEA3H grid for pure Python usage.

    Args:
        resolution (int): ISEA3H resolution [0..32]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output output_format ('geojson', 'csv', etc). Defaults to None (list of IDs).
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict or list: GeoJSON FeatureCollection, file path, or list of IDs depending on output_format
    """
    if resolution < 0 or resolution > 32:
        raise ValueError("Resolution must be in range [0..32]")

    if bbox is None:
        bbox = [-180, -90, 180, 90]
        total_cells = 20 * (7 ** resolution)
        if total_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution {resolution} will generate {total_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
        isea3h_features = generate_grid(resolution)
    else:
        isea3h_features = generate_grid_within_bbox(resolution, bbox)

    return convert_isea3hgrid_output_format(isea3h_features, output_format, output_path, resolution)


if __name__ == "__main__":
    isea3hgrid_cli()
