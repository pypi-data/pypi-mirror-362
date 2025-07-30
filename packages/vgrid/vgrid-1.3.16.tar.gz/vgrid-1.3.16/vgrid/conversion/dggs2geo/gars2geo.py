from vgrid.dggs import s2, olc, geohash, georef, mgrs, mercantile, maidenhead
from vgrid.dggs.gars import garsgrid
from vgrid.dggs.qtm import constructGeometry, qtm_id_to_facet

from shapely.wkt import loads
from shapely.geometry import shape, Polygon, mapping

import json
import re
import os
import argparse

from vgrid.generator.settings import (
    graticule_dggs_to_feature,
    geodesic_dggs_to_feature
)

from pyproj import Geod

geod = Geod(ellps="WGS84")




def gars2geo(gars_ids):
    """
    Convert a list of GARS cell IDs to Shapely geometry objects.
    Accepts a single gars_id (string) or a list of gars_ids.
    Skips invalid or error-prone cells.
    Returns a list of Shapely Polygon objects.
    """
    if isinstance(gars_ids, str):
        gars_ids = [gars_ids]
    gars_polygons = []
    for gars_id in gars_ids:
        try:
            gars_grid = garsgrid.GARSGrid(gars_id)
            wkt_polygon = gars_grid.polygon
            if wkt_polygon:
                cell_polygon = Polygon(list(wkt_polygon.exterior.coords))
                gars_polygons.append(cell_polygon)
        except Exception:
            continue
    return gars_polygons


def gars2geo_cli():
    """
    Command-line interface for gars2geo supporting multiple GARS cell IDs.
    """
    parser = argparse.ArgumentParser(
        description="Convert GARS cell ID(s) to Shapely Polygons"
    )
    parser.add_argument(
        "gars",
        nargs="+",
        help="Input GARS cell ID(s), e.g., gars2geo 574JK1918 ...",
    )
    args = parser.parse_args()
    polys = gars2geo(args.gars)
    return polys
    
def gars2geojson(gars_ids):
    if isinstance(gars_ids, str):
        gars_ids = [gars_ids]
    gars_features = []
    for gars_id in gars_ids:
        try:
            gars_grid = garsgrid.GARSGrid(gars_id)
            wkt_polygon = gars_grid.polygon
            if wkt_polygon:
                resolution_minute = gars_grid.resolution
                resolution = 1
                if resolution_minute == 30:
                    resolution = 1
                elif resolution_minute == 15:
                    resolution = 2
                elif resolution_minute == 5:
                    resolution = 3
                elif resolution_minute == 1:
                    resolution = 4
                cell_polygon = Polygon(list(wkt_polygon.exterior.coords))
                gars_feature = graticule_dggs_to_feature(
                    "gars", gars_id, resolution, cell_polygon
                )
                gars_features.append(gars_feature)
        except Exception:
            continue
    return {"type": "FeatureCollection", "features": gars_features}


def gars2geojson_cli():
    """
    Command-line interface for gars2geojson supporting multiple GARS cell IDs.
    """
    parser = argparse.ArgumentParser(description="Convert GARS cell ID(s) to GeoJSON")
    parser.add_argument(
        "gars",
        nargs="+",
        help="Input GARS cell ID(s), e.g., gars2geojson 574JK1918 ...",
    )
    args = parser.parse_args()
    geojson_data = json.dumps(gars2geojson(args.gars))
    print(geojson_data)
