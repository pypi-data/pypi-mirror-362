"""
Quadkey DGGS Grid Generator Module
"""

import argparse
import json
from shapely.geometry import shape, Polygon
from shapely.ops import unary_union
from tqdm import tqdm
from vgrid.dggs import mercantile
from vgrid.generator.settings import MAX_CELLS, graticule_dggs_to_feature
from pyproj import Geod
geod = Geod(ellps="WGS84")


def generate_grid(resolution, bbox):
    quadkey_features = []
    min_lon, min_lat, max_lon, max_lat = bbox
    tiles = mercantile.tiles(min_lon, min_lat, max_lon, max_lat, resolution)
    for tile in tqdm(tiles, desc="Generating Quadkey DGGS", unit=" cells"):
        z, x, y = tile.z, tile.x, tile.y
        bounds = mercantile.bounds(x, y, z)
        if bounds:
            # Create the bounding box coordinates for the polygon
            min_lat, min_lon = bounds.south, bounds.west
            max_lat, max_lon = bounds.north, bounds.east

            quadkey_id = mercantile.quadkey(tile)

            cell_polygon = Polygon(
                [
                    [min_lon, min_lat],  # Bottom-left corner
                    [max_lon, min_lat],  # Bottom-right corner
                    [max_lon, max_lat],  # Top-right corner
                    [min_lon, max_lat],  # Top-left corner
                    [min_lon, min_lat],  # Closing the polygon (same as the first point)
                ]
            )
            quadkey_feature = graticule_dggs_to_feature(
                "quadkey", quadkey_id, resolution, cell_polygon
            )
            quadkey_features.append(quadkey_feature)

    return {"type": "FeatureCollection", "features": quadkey_features}


def generate_grid_resample(resolution, geojson_features):
    quadkey_features = []

    geometries = [
        shape(feature["geometry"]) for feature in geojson_features["features"]
    ]
    unified_geom = unary_union(geometries)

    min_lon, min_lat, max_lon, max_lat = unified_geom.bounds

    tiles = mercantile.tiles(min_lon, min_lat, max_lon, max_lat, resolution)

    for tile in tqdm(tiles, desc="Generating Quadkey DGGS", unit=" cells"):
        z, x, y = tile.z, tile.x, tile.y
        bounds = mercantile.bounds(x, y, z)

        # Construct tile polygon
        tile_polygon = Polygon(
            [
                [bounds.west, bounds.south],
                [bounds.east, bounds.south],
                [bounds.east, bounds.north],
                [bounds.west, bounds.north],
                [bounds.west, bounds.south],
            ]
        )

        if tile_polygon.intersects(unified_geom):
            quadkey_id = mercantile.quadkey(tile)
            quadkey_feature = graticule_dggs_to_feature(
                "quadkey", quadkey_id, resolution, tile_polygon
            )
            quadkey_features.append(quadkey_feature)

    return {"type": "FeatureCollection", "features": quadkey_features}


def convert_quadkeygrid_output_format(quadkey_features, output_format=None, output_path=None, resolution=None):
    if not quadkey_features:
        return []
    def default_path(ext):
        return f"quadkey_grid_{resolution}.{ext}" if resolution is not None else f"quadkey_grid.{ext}"
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import shape
    if output_format is None:
        return [f["properties"]["quadkey"] for f in quadkey_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in quadkey_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(quadkey_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(quadkey_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(quadkey_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(quadkey_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(quadkey_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(quadkey_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def quadkeygrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate Quadkey grid for pure Python usage.

    Args:
        resolution (int): Quadkey resolution [0..26]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output format ('geojson', 'csv', etc.). Defaults to None (list of Quadkey IDs).
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict, list, or str: Output depending on output_format
    """
    if resolution < 0 or resolution > 26:
        raise ValueError("Resolution must be in range [0..26]")

    if bbox is None:
        bbox = [-180.0, -85.05112878, 180.0, 85.05112878]
        num_cells = 4 ** resolution
        if num_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution {resolution} will generate {num_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
        quadkey_features = generate_grid(resolution, bbox)
    else:
        quadkey_features = generate_grid(resolution, bbox)

    return convert_quadkeygrid_output_format(quadkey_features, output_format, output_path, resolution)


def quadkeygrid_cli():
    parser = argparse.ArgumentParser(description="Generate Quadkey DGGS.")
    parser.add_argument(
        "-r", "--resolution", type=int, required=True, help="resolution [0..26]"
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
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of Quadkey IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    if args.output_format == "None":
        args.output_format = None
    resolution = args.resolution
    bbox = args.bbox if args.bbox else [-180.0, -85.05112878, 180.0, 85.05112878]
    if resolution < 0 or resolution > 26:
        print("Please select a resolution in [0..26] range and try again ")
        return
    if bbox == [-180.0, -85.05112878, 180.0, 85.05112878]:
        num_cells = 4**resolution
        if num_cells > MAX_CELLS:
            print(f"Resolution {resolution} will generate {num_cells} cells "
                  f"which exceeds the limit of {MAX_CELLS}.")
            print("Please select a smaller resolution and try again.")
            return
    quadkey_features = generate_grid(resolution, bbox)
    try:
        result = convert_quadkeygrid_output_format(quadkey_features, args.output_format, args.output, resolution)
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
    quadkeygrid_cli()
