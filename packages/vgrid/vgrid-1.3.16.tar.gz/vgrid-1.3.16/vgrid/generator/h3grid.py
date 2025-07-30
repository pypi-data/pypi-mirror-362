# Reference: https://observablehq.com/@claude-ducharme/h3-map
# https://h3-snow.streamlit.app/

import json, argparse
from shapely.geometry import Polygon, box, shape
from shapely.ops import unary_union
from tqdm import tqdm
from pyproj import Geod
import geopandas as gpd
import h3
from vgrid.generator.settings import MAX_CELLS, geodesic_dggs_to_feature, fix_h3_antimeridian_cells
from vgrid.utils.geometry import geodesic_buffer

geod = Geod(ellps="WGS84")

def convert_h3grid_output_format(
    h3_features, output_format=None, output_path=None, resolution=None
):
    """
    Convert h3_features (list of GeoJSON features) to the requested output output_format.
    output_format: None (list of H3 IDs), 'geo' (list of Shapely Polygons),
                  'gpd' (GeoDataFrame), 'csv', 'geojson', 'shapefile', 'gpkg', 'parquet', or file formats.
    If output_path is None and output_format is a file-based output_format, use './h3grid_{resolution}.{ext}'.
    """
    if not h3_features:
        return []

    def default_path(ext):
        return (
            f"h3grid_{resolution}.{ext}" if resolution is not None else f"h3grid.{ext}"
        )

    if output_format is None:
        return [f["properties"]["h3"] for f in h3_features]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in h3_features]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(h3_features)
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(h3_features)
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        fc = {"type": "FeatureCollection", "features": h3_features}
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(fc, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(h3_features)
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(h3_features)
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(h3_features)
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def generate_grid(resolution, output_format=None, output_path=None):
    total_cells = h3.get_num_cells(resolution)
    if total_cells > MAX_CELLS:
        raise ValueError(
            f"Resolution {resolution} will generate {total_cells} cells which exceeds the limit of {MAX_CELLS}"
        )
    else:
        base_cells = h3.get_res0_cells()
        num_base_cells = len(base_cells)
        h3_features = []
        # Progress bar for base cells
        with tqdm(
            total=num_base_cells, desc="Processing base cells", unit=" cells"
        ) as pbar:
            for cell in base_cells:
                child_cells = h3.cell_to_children(cell, resolution)
                # Progress bar for child cells
                for child_cell in child_cells:
                    # Get the boundary of the cell
                    hex_boundary = h3.cell_to_boundary(child_cell)
                    # Wrap and filter the boundary
                    filtered_boundary = fix_h3_antimeridian_cells(hex_boundary)
                    # Reverse lat/lon to lon/lat for GeoJSON compatibility
                    reversed_boundary = [(lon, lat) for lat, lon in filtered_boundary]
                    cell_polygon = Polygon(reversed_boundary)
                    if cell_polygon.is_valid:
                        h3_id = str(child_cell)
                        num_edges = 6
                        if h3.is_pentagon(h3_id):
                            num_edges = 5
                        h3_feature = geodesic_dggs_to_feature(
                            "h3", h3_id, resolution, cell_polygon, num_edges
                        )
                        h3_features.append(h3_feature)
                        pbar.update(1)

        return convert_h3grid_output_format(
            h3_features, output_format, output_path, resolution
        )

def generate_grid_within_bbox(resolution, bbox, output_format=None, output_path=None):
    bbox_polygon = box(*bbox)  # Create a bounding box polygon
    distance = h3.average_hexagon_edge_length(resolution, unit="m") * 2
    bbox_buffer = geodesic_buffer(bbox_polygon, distance)
    bbox_buffer_cells = h3.geo_to_cells(bbox_buffer, resolution)
    total_cells = len(bbox_buffer_cells)
    if total_cells > MAX_CELLS:
        raise ValueError(
            f"Resolution {resolution} within bounding box {bbox} will generate {total_cells} cells which exceeds the limit of {MAX_CELLS}"
        )
    else:
        h3_features = []
        # Progress bar for base cells
        for bbox_buffer_cell in tqdm(bbox_buffer_cells, desc="Processing cells"):
            # Get the boundary of the cell
            hex_boundary = h3.cell_to_boundary(bbox_buffer_cell)
            # Wrap and filter the boundary
            filtered_boundary = fix_h3_antimeridian_cells(hex_boundary)
            # Reverse lat/lon to lon/lat for GeoJSON compatibility
            reversed_boundary = [(lon, lat) for lat, lon in filtered_boundary]
            cell_polygon = Polygon(reversed_boundary)
            if cell_polygon.intersects(bbox_polygon):
                h3_id = str(bbox_buffer_cell)
                num_edges = 6
                if h3.is_pentagon(h3_id):
                    num_edges = 5
                h3_feature = geodesic_dggs_to_feature(
                    "h3", h3_id, resolution, cell_polygon, num_edges
                )
                h3_features.append(h3_feature)

        return convert_h3grid_output_format(
            h3_features, output_format, output_path, resolution
        )


def generate_grid_resample(
    resolution, geojson_features, output_format="geojson", output_path=None
):
    # Create a unified geometry from all features
    geometries = [
        shape(feature["geometry"]) for feature in geojson_features["features"]
    ]

    unified_geom = unary_union(geometries)

    # Estimate buffer distance based on resolution
    distance = h3.average_hexagon_edge_length(resolution, unit="m") * 2
    buffered_geom = geodesic_buffer(unified_geom, distance)

    # Generate H3 cells that cover the buffered geometry
    h3_cells = h3.geo_to_cells(buffered_geom, resolution)

    h3_features = []
    for h3_cell in tqdm(h3_cells, desc="Generating H3 DGGS", unit=" cells"):
        hex_boundary = h3.cell_to_boundary(h3_cell)
        filtered_boundary = fix_h3_antimeridian_cells(hex_boundary)
        reversed_boundary = [(lon, lat) for lat, lon in filtered_boundary]
        cell_polygon = Polygon(reversed_boundary)

        # Only keep cells that intersect the unified input geometry
        if cell_polygon.intersects(unified_geom):
            h3_id = str(h3_cell)
            num_edges = 6 if not h3.is_pentagon(h3_id) else 5
            h3_feature = geodesic_dggs_to_feature(
                "h3", h3_id, resolution, cell_polygon, num_edges
            )
            h3_features.append(h3_feature)

    return convert_h3grid_output_format(
        h3_features, output_format, output_path, resolution
    )


def h3grid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate H3 grid for pure Python usage.

    Args:
        resolution (int): H3 resolution [0..15]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output output_format ('geojson' or 'csv'). Defaults to 'geojson'.

    Returns:
        dict or list: GeoJSON FeatureCollection or list of CSV rows depending on output_format
    """
    if resolution < 0 or resolution > 15:
        raise ValueError("Resolution must be in range [0..15]")

    if bbox is None:
        bbox = [-180, -90, 180, 90]
        num_cells = h3.get_num_cells(resolution)
        if num_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution {resolution} will generate {num_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
        return generate_grid(resolution, output_format, output_path)
    else:
        return generate_grid_within_bbox(resolution, bbox, output_format, output_path)


def h3grid_cli():
    """CLI interface for generating H3 grid."""
    parser = argparse.ArgumentParser(description="Generate H3 DGGS.")
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
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of H3 IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    # Ensure Python None, not string 'None'
    if args.output_format == "None":
        args.output_format = None
    try:
        result = h3grid(args.resolution, args.bbox, args.output_format, args.output)
        if result is None:
            return
        if args.output_format is None:
            # Print the entire Python list of H3 IDs at once
            print(result)
        elif args.output_format in ["geo", "gpd"]:
            print(result)
        elif args.output_format in [
            "csv",
            "parquet",
            "gpkg",
            "shapefile",
            "geojson",
        ] and isinstance(result, str):
            print(f"Output saved as {result}")
        elif args.output_format == "geojson" and isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print(f"Output saved as {args.output}")
    except ValueError as e:
        print(f"Error: {str(e)}")
        return
