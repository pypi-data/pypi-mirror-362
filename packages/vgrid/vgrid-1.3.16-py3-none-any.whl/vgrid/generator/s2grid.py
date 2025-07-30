"""
S2 Grid Generator Module.
This module provides functionality to generate S2 DGGS grids.
Reference:
    https://github.com/aaliddell/s2cell,
    https://medium.com/@claude.ducharme/selecting-a-geo-representation-81afeaf3bf01
    https://github.com/sidewalklabs/s2
    https://github.com/google/s2geometry/tree/master/src/python
    https://github.com/google/s2geometry
    https://gis.stackexchange.com/questions/293716/creating-shapefile-of-s2-cells-for-given-level
    https://s2.readthedocs.io/en/latest/quickstart.html
"""

import json
import argparse
from shapely.geometry import shape, Polygon
from shapely.ops import unary_union
import geopandas as gpd
from tqdm import tqdm
from vgrid.utils.antimeridian import fix_polygon
from vgrid.generator.settings import geodesic_dggs_to_feature
from vgrid.dggs import s2
from vgrid.generator.settings import MAX_CELLS


def s2_cell_to_polygon(s2_id):
    """ 
    Convert an S2 cell ID to a Shapely Polygon.
    """
    cell = s2.Cell(s2_id)
    vertices = []
    for i in range(4):
        vertex = s2.LatLng.from_point(cell.get_vertex(i))
        vertices.append((vertex.lng().degrees, vertex.lat().degrees))

    vertices.append(vertices[0])  # Close the polygon

    # Create a Shapely Polygon
    polygon = Polygon(vertices)
    #  Fix Antimerididan:
    fixed_polygon = fix_polygon(polygon)
    return fixed_polygon


def generate_grid(resolution, bbox):
    """
    Generate an S2 DGGS grid for a given resolution and bounding box.
    """
    min_lng, min_lat, max_lng, max_lat = bbox
    # Define the cell level (S2 uses a level system for zoom, where level 30 is the highest resolution)
    level = resolution
    # Create a list to store the S2 cell IDs
    cell_ids = []
    # Define the cell covering
    coverer = s2.RegionCoverer()
    coverer.min_level = level
    coverer.max_level = level
    # coverer.max_cells = 1000_000  # Adjust as needed
    # coverer.max_cells = 0  # Adjust as needed

    # Define the region to cover (in this example, we'll use the entire world)
    region = s2.LatLngRect(
        s2.LatLng.from_degrees(min_lat, min_lng),
        s2.LatLng.from_degrees(max_lat, max_lng),
    )

    # Get the covering cells
    covering = coverer.get_covering(region)

    # Convert the covering cells to S2 cell IDs
    for cell_id in covering:
        cell_ids.append(cell_id)

    s2_features = []
    num_edges = 4

    for cell_id in tqdm(cell_ids, desc="Generating S2 DGGS", unit=" cells"):
        # Generate a Shapely Polygon
        cell_polygon = s2_cell_to_polygon(cell_id)
        s2_token = cell_id.to_token()
        s2_feature = geodesic_dggs_to_feature(
            "s2", s2_token, resolution, cell_polygon, num_edges
        )
        s2_features.append(s2_feature)

    return {"type": "FeatureCollection", "features": s2_features}


def generate_grid_resample(resolution, geojson_features):
    """
    Generate an S2 DGGS grid for a given resolution and GeoJSON features.
    """
    geometries = [
        shape(feature["geometry"]) for feature in geojson_features["features"]
    ]
    unified_geom = unary_union(geometries)

    # Step 2: Get bounding box from unified geometry
    min_lng, min_lat, max_lng, max_lat = unified_geom.bounds

    # Step 3: Configure the S2 coverer
    level = resolution
    coverer = s2.RegionCoverer()
    coverer.min_level = level
    coverer.max_level = level

    # Step 4: Create a LatLngRect from the bounding box
    region = s2.LatLngRect(
        s2.LatLng.from_degrees(min_lat, min_lng),
        s2.LatLng.from_degrees(max_lat, max_lng),
    )

    # Step 5: Get the covering cells
    covering = coverer.get_covering(region)

    s2_features = []
    for cell_id in tqdm(covering, desc="Generating S2 DGGS", unit=" cells"):
        # Convert S2 cell to polygon (must define `s2_cell_to_polygon`)
        cell_polygon = s2_cell_to_polygon(cell_id)

        # Check intersection with actual geometry
        if cell_polygon.intersects(unified_geom):
            s2_token = cell_id.to_token()
            num_edges = 4
            s2_feature = geodesic_dggs_to_feature(
                "s2", s2_token, resolution, cell_polygon, num_edges
            )
            s2_features.append(s2_feature)

    return {"type": "FeatureCollection", "features": s2_features}


def convert_s2grid_output_format(s2_features, output_format=None, output_path=None, resolution=None):
    """
    Convert S2 DGGS grid to various output formats.
    """ 
    if not s2_features:
        return []
    def default_path(ext):
        return f"s2_grid_{resolution}.{ext}" if resolution is not None else f"s2_grid.{ext}"
    if output_format is None:
        return [f["properties"]["s2"] for f in s2_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in s2_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(s2_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(s2_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(s2_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(s2_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(s2_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(s2_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def s2grid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate S2 grid for pure Python usage.

    Args:
        resolution (int): S2 resolution [0..30]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output output_format ('geojson', 'csv', etc.). Defaults to None (list of S2 tokens).
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict or list: GeoJSON FeatureCollection, list of S2 tokens, or file path depending on output_format
    """
    if resolution < 0 or resolution > 30:
        raise ValueError("Resolution must be in range [0..30]")

    if bbox is None:
        bbox = [-180, -90, 180, 90]
        # Estimate number of cells: S2 has 6 * 4**res cells at each level
        num_cells = 6 * (4 ** resolution)
        if num_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution {resolution} will generate {num_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
    s2_features = generate_grid(resolution, bbox)
    return convert_s2grid_output_format(s2_features, output_format, output_path, resolution)


def s2grid_cli():
    """
    Command-line interface for S2 DGGS grid generation.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Generate S2 DGGS.")
    parser.add_argument(
        "-r", "--resolution", type=int, required=True, help="Resolution [0..30]"
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
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of S2 IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    if args.output_format == "None":
        args.output_format = None
    resolution = args.resolution
    bbox = args.bbox if args.bbox else [-180, -90, 180, 90]
    if resolution < 0 or resolution > 30:
        print("Please select a resolution in [0..30] range and try again ")
        return
    s2_features = generate_grid(resolution, bbox)
    try:
        result = convert_s2grid_output_format(s2_features, args.output_format, args.output, resolution)
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
    s2grid_cli()
