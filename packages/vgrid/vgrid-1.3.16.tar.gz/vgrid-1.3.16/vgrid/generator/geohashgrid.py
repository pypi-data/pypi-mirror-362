"""
GEOHASH DGGS Grid Generator Module
Reference: https://geohash.softeng.co/uekkn, https://github.com/vinsci/geohash, https://www.movable-type.co.uk/scripts/geohash.html?geohash=dp3

"""

import argparse
import json
from shapely.geometry import Polygon, shape
from shapely.ops import unary_union
from tqdm import tqdm
from vgrid.generator.settings import MAX_CELLS, graticule_dggs_to_feature
from vgrid.dggs import geohash
import geopandas as gpd

initial_geohashes = [
    "b",
    "c",
    "f",
    "g",
    "u",
    "v",
    "y",
    "z",
    "8",
    "9",
    "d",
    "e",
    "s",
    "t",
    "w",
    "x",
    "0",
    "1",
    "2",
    "3",
    "p",
    "q",
    "r",
    "k",
    "m",
    "n",
    "h",
    "j",
    "4",
    "5",
    "6",
    "7",
]


def geohash_to_polygon(gh):
    """Convert geohash to a Shapely Polygon."""
    lat, lon = geohash.decode(gh)
    lat_err, lon_err = geohash.decode_exactly(gh)[2:]

    bbox = {
        "w": max(lon - lon_err, -180),
        "e": min(lon + lon_err, 180),
        "s": max(lat - lat_err, -85.051129),
        "n": min(lat + lat_err, 85.051129),
    }

    return Polygon(
        [
            (bbox["w"], bbox["s"]),
            (bbox["w"], bbox["n"]),
            (bbox["e"], bbox["n"]),
            (bbox["e"], bbox["s"]),
            (bbox["w"], bbox["s"]),
        ]
    )


def expand_geohash(gh, target_length, geohashes):
    if len(gh) == target_length:
        geohashes.add(gh)
        return
    for char in "0123456789bcdefghjkmnpqrstuvwxyz":
        expand_geohash(gh + char, target_length, geohashes)


def generate_grid(resolution):
    """Generate GeoJSON for the entire world at the given geohash resolution."""

    geohashes = set()
    for gh in initial_geohashes:
        expand_geohash(gh, resolution, geohashes)

    geohash_features = []
    for gh in tqdm(geohashes, desc="Generating Geohash DGGS", unit=" cells"):
        cell_polygon = geohash_to_polygon(gh)
        geohash_feature = graticule_dggs_to_feature(
            "geohash", gh, resolution, cell_polygon
        )
        geohash_features.append(geohash_feature)

    return {"type": "FeatureCollection", "features": geohash_features}


def expand_geohash_bbox(gh, target_length, geohashes, bbox_polygon):
    """Expand geohash only if it intersects the bounding box."""
    polygon = geohash_to_polygon(gh)
    if not polygon.intersects(bbox_polygon):
        return

    if len(gh) == target_length:
        geohashes.add(gh)  # Add to the set if it reaches the target resolution
        return

    for char in "0123456789bcdefghjkmnpqrstuvwxyz":
        expand_geohash_bbox(gh + char, target_length, geohashes, bbox_polygon)


def generate_grid_within_bbox(resolution, bbox):
    """Generate GeoJSON for geohashes within a bounding box at the given resolution."""
    geohash_features = []
    bbox_polygon = Polygon.from_bounds(*bbox)

    # Compute intersected geohashes using set comprehension
    intersected_geohashes = {
        gh
        for gh in initial_geohashes
        if geohash_to_polygon(gh).intersects(bbox_polygon)
    }

    # Expand geohash bounding box
    geohashes_bbox = set()
    for gh in intersected_geohashes:
        expand_geohash_bbox(gh, resolution, geohashes_bbox, bbox_polygon)

    # Generate GeoJSON features
    geohash_features.extend(
        graticule_dggs_to_feature("geohash", gh, resolution, geohash_to_polygon(gh))
        for gh in tqdm(geohashes_bbox, desc="Generating Geohash DGGS", unit=" cells")
    )

    return {"type": "FeatureCollection", "features": geohash_features}


def generate_grid_resample(resolution, geojson_features):
    """Generate GeoJSON for geohashes within a GeoJSON feature collection at the given resolution."""
    geohash_features = []

    # Union of all input geometries
    geometries = [
        shape(feature["geometry"]) for feature in geojson_features["features"]
    ]
    unified_geom = unary_union(geometries)

    # Compute intersected geohashes from the initial set
    intersected_geohashes = {
        gh
        for gh in initial_geohashes
        if geohash_to_polygon(gh).intersects(unified_geom)
    }

    # Expand geohash coverage within the unified geometry
    geohashes_geom = set()
    for gh in intersected_geohashes:
        expand_geohash_bbox(gh, resolution, geohashes_geom, unified_geom)

    # Generate GeoJSON features
    geohash_features.extend(
        graticule_dggs_to_feature("geohash", gh, resolution, geohash_to_polygon(gh))
        for gh in tqdm(geohashes_geom, desc="Generating Geohash DGGS", unit="cells")
    )

    return {"type": "FeatureCollection", "features": geohash_features}


def convert_geohashgrid_output_format(geohash_features, output_format=None, output_path=None, resolution=None):
    if not geohash_features:
        return []
    def default_path(ext):
        return f"geohash_grid_{resolution}.{ext}" if resolution is not None else f"geohash_grid.{ext}"
    if output_format is None:
        return [f["properties"]["geohash"] for f in geohash_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in geohash_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(geohash_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(geohash_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(geohash_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(geohash_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(geohash_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(geohash_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def geohashgrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate Geohash grid for pure Python usage.

    Args:
        resolution (int): Geohash resolution [1..10]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output format ('geojson', 'csv', 'geo', 'gpd', 'shapefile', 'gpkg', 'parquet', or None for list of Geohash IDs).
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict, list, or str: Output in the requested format or file path.
    """
    if not (1 <= resolution <= 10):
        raise ValueError("Resolution must be between 1 and 10.")
    if bbox is None:
        bbox = [-180, -90, 180, 90]
        total_cells = 32 ** resolution
        if total_cells > MAX_CELLS:
            raise ValueError(f"Resolution {resolution} will generate {total_cells} cells which exceeds the limit of {MAX_CELLS}")
        geohash_features = generate_grid(resolution)
    else:
        geohash_features = generate_grid_within_bbox(resolution, bbox)
    return convert_geohashgrid_output_format(geohash_features, output_format, output_path, resolution)


def geohashgrid_cli():
    parser = argparse.ArgumentParser(description="Generate Geohash DGGS.")
    parser.add_argument(
        "-r", "--resolution", type=int, required=True, help="Resolution [1..10]"
    )
    parser.add_argument(
        "-b",
        "--bbox",
        type=float,
        nargs=4,
        help="Bounding box in the format: min_lon min_lat max_lon max_lat (default is the whole world)",
    )
    parser.add_argument(
        "-f",
        "--output_format",
        type=str,
        choices=["geojson", "csv", "geo", "gpd", "shapefile", "gpkg", "parquet", None],
        default=None,
        help="Output format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of Geohash IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    if args.output_format == "None":
        args.output_format = None
    try:
        result = geohashgrid(args.resolution, args.bbox, args.output_format, args.output)
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
    geohashgrid_cli()
