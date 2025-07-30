"""
rHEALPix DGGS Grid Generator Module
"""
import argparse
import json
from vgrid.dggs.rhealpixdggs.dggs import RHEALPixDGGS
from vgrid.dggs.rhealpixdggs.utils import my_round
from shapely.geometry import Polygon, box, shape
from tqdm import tqdm
from vgrid.generator.settings import (
    MAX_CELLS,
    geodesic_dggs_to_feature,
    fix_rhealpix_antimeridian_cells,
    rhealpix_cell_to_polygon,
)

from pyproj import Geod

geod = Geod(ellps="WGS84")
rhealpix_dggs = RHEALPixDGGS()


def generate_grid(resolution):
    rhealpix_features = []
    total_cells = rhealpix_dggs.num_cells(resolution)
    rhealpix_grid = rhealpix_dggs.grid(resolution)

    with tqdm(
        total=total_cells, desc="Generating rHEALPix DGGS", unit=" cells"
    ) as pbar:
        for rhealpix_cell in rhealpix_grid:
            cell_polygon = rhealpix_cell_to_polygon(rhealpix_cell)
            rhealpix_id = str(rhealpix_cell)
            num_edges = 4
            if rhealpix_cell.ellipsoidal_shape() == "dart":
                num_edges = 3
            rhealpix_feature = geodesic_dggs_to_feature(
                "rhealpix", rhealpix_id, resolution, cell_polygon, num_edges
            )
            rhealpix_features.append(rhealpix_feature)
            pbar.update(1)

        return {
            "type": "FeatureCollection",
            "features": rhealpix_features,
        }


def generate_grid_within_bbox(resolution, bbox):
    bbox_polygon = box(*bbox)  # Create a bounding box polygon
    bbox_center_lon = bbox_polygon.centroid.x
    bbox_center_lat = bbox_polygon.centroid.y
    seed_point = (bbox_center_lon, bbox_center_lat)

    rhealpix_features = []
    seed_cell = rhealpix_dggs.cell_from_point(resolution, seed_point, plane=False)
    seed_cell_id = str(seed_cell)  # Unique identifier for the current cell
    seed_cell_polygon = rhealpix_cell_to_polygon(seed_cell)

    if seed_cell_polygon.contains(bbox_polygon):
        num_edges = 4
        if seed_cell.ellipsoidal_shape() == "dart":
            num_edges = 3

        rhealpix_feature = geodesic_dggs_to_feature(
            "rhealpix", seed_cell_id, resolution, seed_cell_polygon, num_edges
        )
        rhealpix_features.append(rhealpix_feature)
        return {
            "type": "FeatureCollection",
            "features": rhealpix_features,
        }

    else:
        # Initialize sets and queue
        covered_cells = set()  # Cells that have been processed (by their unique ID)
        queue = [seed_cell]  # Queue for BFS exploration
        while queue:
            current_cell = queue.pop()
            current_cell_id = str(
                current_cell
            )  # Unique identifier for the current cell

            if current_cell_id in covered_cells:
                continue

            # Add current cell to the covered set
            covered_cells.add(current_cell_id)

            # Convert current cell to polygon
            cell_polygon = rhealpix_cell_to_polygon(current_cell)

            # Skip cells that do not intersect the bounding box
            if not cell_polygon.intersects(bbox_polygon):
                continue

            # Get neighbors and add to queue
            neighbors = current_cell.neighbors(plane=False)
            for _, neighbor in neighbors.items():
                neighbor_id = str(neighbor)  # Unique identifier for the neighbor
                if neighbor_id not in covered_cells:
                    queue.append(neighbor)

        for cell_id in tqdm(
            covered_cells, desc="Generating rHEALPix DGGS", unit=" cells"
        ):
            rhealpix_uids = (cell_id[0],) + tuple(map(int, cell_id[1:]))
            cell = rhealpix_dggs.cell(rhealpix_uids)
            cell_polygon = rhealpix_cell_to_polygon(cell)
            if cell_polygon.intersects(bbox_polygon):
                num_edges = 4
                if seed_cell.ellipsoidal_shape() == "dart":
                    num_edges = 3
                rhealpix_feature = geodesic_dggs_to_feature(
                    "rhealpix", cell_id, resolution, cell_polygon, num_edges
                )
                rhealpix_features.append(rhealpix_feature)

        return {
            "type": "FeatureCollection",
            "features": rhealpix_features,
        }


def generate_grid_resample(resolution, geojson_features):
    # Step 1: Extract and unify all geometries from input features
    geometries = [
        shape(feature["geometry"]) for feature in geojson_features["features"]
    ]
    unified_geom = unary_union(geometries)

    # Step 2: Use centroid of unified geometry as seed point
    seed_point = (unified_geom.centroid.x, unified_geom.centroid.y)

    rhealpix_features = []
    seed_cell = rhealpix_dggs.cell_from_point(resolution, seed_point, plane=False)
    seed_cell_id = str(seed_cell)
    seed_cell_polygon = rhealpix_cell_to_polygon(seed_cell)

    # Step 3: If seed cell fully contains geometry
    if seed_cell_polygon.contains(unified_geom):
        num_edges = 4
        if seed_cell.ellipsoidal_shape() == "dart":
            num_edges = 3

        rhealpix_feature = geodesic_dggs_to_feature(
            "rhealpix", seed_cell_id, resolution, seed_cell_polygon, num_edges
        )
        rhealpix_features.append(rhealpix_feature)
        return {
            "type": "FeatureCollection",
            "features": rhealpix_features,
        }

    # Step 4: Explore neighbors if more cells needed
    covered_cells = set()
    queue = [seed_cell]

    while queue:
        current_cell = queue.pop()
        current_cell_id = str(current_cell)

        if current_cell_id in covered_cells:
            continue

        covered_cells.add(current_cell_id)
        cell_polygon = rhealpix_cell_to_polygon(current_cell)

        if not cell_polygon.intersects(unified_geom):
            continue

        neighbors = current_cell.neighbors(plane=False)
        for _, neighbor in neighbors.items():
            neighbor_id = str(neighbor)
            if neighbor_id not in covered_cells:
                queue.append(neighbor)

    for cell_id in tqdm(covered_cells, desc="Generating rHEALPix DGGS", unit=" cells"):
        rhealpix_uids = (cell_id[0],) + tuple(map(int, cell_id[1:]))
        cell = rhealpix_dggs.cell(rhealpix_uids)
        cell_polygon = rhealpix_cell_to_polygon(cell)

        if cell_polygon.intersects(unified_geom):
            num_edges = 4
            if seed_cell.ellipsoidal_shape() == "dart":
                num_edges = 3
            rhealpix_feature = geodesic_dggs_to_feature(
                "rhealpix", cell_id, resolution, cell_polygon, num_edges
            )
            rhealpix_features.append(rhealpix_feature)

    return {
        "type": "FeatureCollection",
        "features": rhealpix_features,
    }


def convert_rhealpixgrid_output_format(rhealpix_features, output_format=None, output_path=None, resolution=None):
    if not rhealpix_features:
        return []
    def default_path(ext):
        return f"rhealpix_grid_{resolution}.{ext}" if resolution is not None else f"rhealpix_grid.{ext}"
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import shape
    if output_format is None:
        return [f["properties"]["rhealpix"] for f in rhealpix_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in rhealpix_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(rhealpix_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(rhealpix_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(rhealpix_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(rhealpix_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(rhealpix_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(rhealpix_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def rhealpixgrid_cli():
    parser = argparse.ArgumentParser(description="Generate rHEALPix DGGS.")
    parser.add_argument(
        "-r", "--resolution", type=int, required=True, help="Resolution [0..15]"
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
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of rHEALPix IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    if args.output_format == "None":
        args.output_format = None
    resolution = args.resolution
    if resolution < 0 or resolution > 15:
        print("Please select a resolution in [0..15] range and try again ")
        return
    bbox = args.bbox if args.bbox else [-180, -90, 180, 90]
    if bbox == [-180, -90, 180, 90]:
        num_cells = rhealpix_dggs.num_cells(resolution)
        print(f"Resolution {resolution} will generate {num_cells} cells ")
        if num_cells > MAX_CELLS:
            print(f"which exceeds the limit of {MAX_CELLS}.")
            print("Please select a smaller resolution and try again.")
            return
        rhealpix_features = generate_grid(resolution)
    else:
        rhealpix_features = generate_grid_within_bbox(resolution, bbox)
    try:
        result = convert_rhealpixgrid_output_format(rhealpix_features, args.output_format, args.output, resolution)
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


def rhealpixgrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate rHEALPix grid for pure Python usage.

    Args:
        resolution (int): rHEALPix resolution [0..15]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output output_format ('geojson', 'csv', 'geo', 'gpd', 'shapefile', 'gpkg', 'parquet', or None for list of rHEALPix IDs). Defaults to None.
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict, list, or str: Output in the requested output_format (GeoJSON FeatureCollection, list of IDs, file path, etc.)
    """
    if resolution < 0 or resolution > 15:
        raise ValueError("Resolution must be in range [0..15]")

    if bbox is None:
        bbox = [-180, -90, 180, 90]
        num_cells = rhealpix_dggs.num_cells(resolution)
        if num_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution {resolution} will generate {num_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
        rhealpix_features = generate_grid(resolution)
    else:
        rhealpix_features = generate_grid_within_bbox(resolution, bbox)
    return convert_rhealpixgrid_output_format(rhealpix_features, output_format, output_path, resolution)


if __name__ == "__main__":
    rhealpixgrid_cli()

