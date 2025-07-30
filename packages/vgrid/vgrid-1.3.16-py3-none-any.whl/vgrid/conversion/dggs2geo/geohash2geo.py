"""
Geohash to Geometry Conversion Module

This module provides functions to convert Geohash cell identifiers to geometric representations.
It supports conversion to Shapely Polygon objects and GeoJSON FeatureCollections.

Main functions:
- geohash2geo: Convert Geohash IDs to Shapely Polygon objects
- geohash2geojson: Convert Geohash IDs to GeoJSON FeatureCollection
- Command-line interfaces for both functions
"""

import json
import argparse
from shapely.geometry import Polygon
from vgrid.dggs import geohash
from vgrid.generator.settings import graticule_dggs_to_feature

def geohash2geo(geohash_ids):
    """
    Convert a list of Geohash cell IDs to Shapely geometry objects.
    Accepts a single geohash_id (string) or a list of geohash_ids.
    Skips invalid or error-prone cells.
    Returns a list of Shapely Polygon objects.
    """
    if isinstance(geohash_ids, str):
        geohash_ids = [geohash_ids]
    geohash_polygons = []
    for geohash_id in geohash_ids:
        try:
            bbox = geohash.bbox(geohash_id)
            if bbox:
                min_lat, min_lon = bbox["s"], bbox["w"]
                max_lat, max_lon = bbox["n"], bbox["e"]
                cell_polygon = Polygon(
                    [
                        [min_lon, min_lat],
                        [max_lon, min_lat],
                        [max_lon, max_lat],
                        [min_lon, max_lat],
                        [min_lon, min_lat],
                    ]
                )
                geohash_polygons.append(cell_polygon)
        except Exception:
            continue
    return geohash_polygons


def geohash2geo_cli():
    """
    Command-line interface for geohash2geo supporting multiple Geohash cell IDs.
    """
    parser = argparse.ArgumentParser(
        description="Convert Geohash cell ID(s) to Shapely Polygons"
    )
    parser.add_argument(
        "geohash",
        nargs="+",
        help="Input Geohash cell ID(s), e.g., geohash2geo w3gvk1td8 ...",
    )
    args = parser.parse_args()
    polys = geohash2geo(args.geohash)
    return polys


def geohash2geojson(geohash_ids):
    """
    Convert a list of Geohash cell IDs to GeoJSON FeatureCollection.
    Accepts a single geohash_id (string) or a list of geohash_ids.
    Skips invalid or error-prone cells.
    Returns a GeoJSON FeatureCollection.
    """
    if isinstance(geohash_ids, str):
        geohash_ids = [geohash_ids]
    geohash_features = []
    for geohash_id in geohash_ids:
        try:
            bbox = geohash.bbox(geohash_id)
            if bbox:
                min_lat, min_lon = bbox["s"], bbox["w"]
                max_lat, max_lon = bbox["n"], bbox["e"]
                resolution = len(geohash_id)
                cell_polygon = Polygon(
                    [
                        [min_lon, min_lat],
                        [max_lon, min_lat],
                        [max_lon, max_lat],
                        [min_lon, max_lat],
                        [min_lon, min_lat],
                    ]
                )
                geohash_feature = graticule_dggs_to_feature(
                    "geohash", geohash_id, resolution, cell_polygon
                )
                geohash_features.append(geohash_feature)
        except Exception:
            continue
    return {"type": "FeatureCollection", "features": geohash_features}

def geohash2geojson_cli():
    """
    Command-line interface for geohash2geojson supporting multiple Geohash cell IDs.
    """
    parser = argparse.ArgumentParser(
        description="Convert Geohash cell ID(s) to GeoJSON"
    )
    parser.add_argument(
        "geohash",
        nargs="+",
        help="Input Geohash cell ID(s), e.g., geohash2geojson w3gvk1td8 ...",
    )
    args = parser.parse_args()
    geojson_data = json.dumps(geohash2geojson(args.geohash))
    print(geojson_data)
