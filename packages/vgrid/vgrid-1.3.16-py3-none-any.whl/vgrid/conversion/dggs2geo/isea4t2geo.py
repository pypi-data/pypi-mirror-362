import json
import argparse
from shapely.wkt import loads
from shapely.geometry import Polygon
import platform

if platform.system() == "Windows":
    from vgrid.dggs.eaggr.enums.shape_string_format import ShapeStringFormat
    from vgrid.dggs.eaggr.eaggr import Eaggr
    from vgrid.dggs.eaggr.shapes.dggs_cell import DggsCell
    from vgrid.dggs.eaggr.enums.model import Model
    from vgrid.generator.settings import fix_isea4t_wkt, fix_isea4t_antimeridian_cells
    isea4t_dggs = Eaggr(Model.ISEA4T)

from vgrid.generator.settings import (
    geodesic_dggs_to_feature,
    fix_isea4t_antimeridian_cells,
)


def isea4t2geo(isea4t_ids):
    """
    Convert a list of ISEA4T cell IDs to Shapely geometry objects.
    Accepts a single isea4t_id (string) or a list of isea4t_ids.
    Skips invalid or error-prone cells.
    Returns a list of Shapely Polygon objects.
    """
    if isinstance(isea4t_ids, str):
        isea4t_ids = [isea4t_ids]
    isea4t_polygons = []
    if platform.system() == "Windows":
        for isea4t_id in isea4t_ids:
            try:
                cell_to_shape = isea4t_dggs.convert_dggs_cell_outline_to_shape_string(
                    DggsCell(isea4t_id), ShapeStringFormat.WKT
                )
                cell_to_shape_fixed = loads(fix_isea4t_wkt(cell_to_shape))
                if (
                    isea4t_id.startswith("00")
                    or isea4t_id.startswith("09")
                    or isea4t_id.startswith("14")
                    or isea4t_id.startswith("04")
                    or isea4t_id.startswith("19")
                ):
                    cell_to_shape_fixed = fix_isea4t_antimeridian_cells(
                        cell_to_shape_fixed
                    )
                if cell_to_shape_fixed:
                    cell_polygon = Polygon(list(cell_to_shape_fixed.exterior.coords))
                    isea4t_polygons.append(cell_polygon)
            except Exception:
                continue
    return isea4t_polygons


def isea4t2geo_cli():
    """
    Command-line interface for isea4t2geo supporting multiple ISEA4T cell IDs.
    """
    parser = argparse.ArgumentParser(
        description="Convert ISEA4T cell ID(s) to Shapely Polygons"
    )
    parser.add_argument(
        "isea4t",
        nargs="+",
        help="Input isea4t code(s), e.g., isea4t2geo 131023133313201333311333 ...",
    )
    args = parser.parse_args()
    polys = isea4t2geo(args.isea4t)
    return polys


def isea4t2geojson(isea4t_ids):
    if isinstance(isea4t_ids, str):
        isea4t_ids = [isea4t_ids]
    isea4t_features = []
    if platform.system() == "Windows":
        for isea4t_id in isea4t_ids:
            try:
                
                cell_to_shape = isea4t_dggs.convert_dggs_cell_outline_to_shape_string(
                    DggsCell(isea4t_id), ShapeStringFormat.WKT
                )
                cell_to_shape_fixed = loads(fix_isea4t_wkt(cell_to_shape))
                if (
                    isea4t_id.startswith("00")
                    or isea4t_id.startswith("09")
                    or isea4t_id.startswith("14")
                    or isea4t_id.startswith("04")
                    or isea4t_id.startswith("19")
                ):
                    cell_to_shape_fixed = fix_isea4t_antimeridian_cells(
                        cell_to_shape_fixed
                    )
                if cell_to_shape_fixed:
                    resolution = len(isea4t_id) - 2
                    num_edges = 3
                    cell_polygon = Polygon(list(cell_to_shape_fixed.exterior.coords))
                    isea4t_feature = geodesic_dggs_to_feature(
                        "isea4t", isea4t_id, resolution, cell_polygon, num_edges
                    )
                    isea4t_features.append(isea4t_feature)
            except Exception:
                continue
        return {"type": "FeatureCollection", "features": isea4t_features}


def isea4t2geojson_cli():
    """
    Command-line interface for isea4t2geojson supporting multiple ISEA4T cell IDs.
    """
    parser = argparse.ArgumentParser(
        description="Convert Open-Eaggr ISEA4T cell ID(s) to GeoJSON"
    )
    parser.add_argument(
        "isea4t",
        nargs="+",
        help="Input isea4t code(s), e.g., isea4t2geojson 131023133313201333311333 ...",
    )
    args = parser.parse_args()
    geojson_data = json.dumps(isea4t2geojson(args.isea4t))
    print(geojson_data)
