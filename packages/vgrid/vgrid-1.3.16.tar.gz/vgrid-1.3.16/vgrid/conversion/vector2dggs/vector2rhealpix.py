"""
Vector to rHEALPix DGGS Grid Conversion Module
"""

import sys
import argparse
import math
from shapely.geometry import Polygon, box, MultiPoint, MultiLineString, MultiPolygon
import pandas as pd
import geopandas as gpd
from tqdm import tqdm
from vgrid.dggs.rhealpixdggs.dggs import RHEALPixDGGS
from vgrid.dggs.rhealpixdggs.utils import my_round
from vgrid.generator.rhealpixgrid import fix_rhealpix_antimeridian_cells
from vgrid.generator.settings import geodesic_dggs_to_feature
from vgrid.conversion.dggscompact import rhealpix_compact
from vgrid.utils.geometry import check_predicate
from vgrid.stats.rhealpixstats import rhealpix_metrics
from vgrid.utils.geometry import (
    shortest_point_distance,
    shortest_polyline_distance,
    shortest_polygon_distance,
)


def validate_rhealpix_resolution(resolution):
    """
    Validate that rHEALPix resolution is in the valid range [0..15].

    Args:
        resolution: Resolution value to validate

    Returns:
        int: Validated resolution value

    Raises:
        ValueError: If resolution is not in range [0..15]
        TypeError: If resolution is not an integer
    """
    if not isinstance(resolution, int):
        raise TypeError(
            f"Resolution must be an integer, got {type(resolution).__name__}"
        )

    if resolution < 0 or resolution > 15:
        raise ValueError(f"Resolution must be in range [0..15], got {resolution}")

    return resolution


def rhealpix_cell_to_polygon(cell):
    """Convert rHEALPix cell to Shapely polygon.
    
    Args:
        cell: rHEALPix cell object
        
    Returns:
        Polygon: Shapely polygon representation of the cell
    """
    vertices = [
        tuple(my_round(coord, 14) for coord in vertex)
        for vertex in cell.vertices(plane=False)
    ]
    if vertices[0] != vertices[-1]:
        vertices.append(vertices[0])
    vertices = fix_rhealpix_antimeridian_cells(vertices)
    return Polygon(vertices)


def point2rhealpix(
    rhealpix_dggs,
    resolution,
    point,
    feature_properties=None,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
    all_points=None,
):
    """Convert point geometry to rHEALPix grid cells.
    
    Args:
        rhealpix_dggs: RHEALPixDGGS instance
        resolution: rHEALPix resolution level
        point: Point geometry
        feature_properties: Optional properties to include
        predicate: Spatial predicate for filtering
        compact: Enable compact mode
        topology: Enable topology preserving mode
        include_properties: Whether to include properties
        all_points: All points for topology preservation
        
    Returns:
        list: List of rHEALPix feature dictionaries
    """
    # If topology preservation is enabled, calculate appropriate resolution
    if topology:
        if all_points is None:
            raise ValueError("all_points parameter is required when topology=True")
        shortest_distance = shortest_point_distance(all_points)
        # print(shortest_distance)
        if shortest_distance > 0:
            for res in range(16):
                _, avg_edge_length, _ = rhealpix_metrics(res)
                cell_diameter = avg_edge_length * 2
                if cell_diameter < shortest_distance:
                    resolution = res
                    break
            else:
                resolution = 15
    
    rhealpix_features = []
    seed_cell = rhealpix_dggs.cell_from_point(
        resolution, (point.x, point.y), plane=False
    )

    seed_cell_polygon = rhealpix_cell_to_polygon(seed_cell)
    if seed_cell_polygon:
        seed_cell_id = str(seed_cell)
        num_edges = 4
        if seed_cell.ellipsoidal_shape() == "dart":
            num_edges = 3
        rhealpix_feature = geodesic_dggs_to_feature(
            "rhealpix", seed_cell_id, resolution, seed_cell_polygon, num_edges
        )
        if feature_properties:
            rhealpix_feature["properties"].update(feature_properties)
        rhealpix_features.append(rhealpix_feature)
    return rhealpix_features


def polyline2rhealpix(
    rhealpix_dggs,
    resolution,
    feature,
    feature_properties=None,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
    all_polylines=None,
):
    """Convert polyline geometry to rHEALPix grid cells.
    
    Args:
        rhealpix_dggs: RHEALPixDGGS instance
        resolution: rHEALPix resolution level
        feature: LineString or MultiLineString geometry
        feature_properties: Optional properties to include
        predicate: Spatial predicate for filtering
        compact: Enable compact mode
        topology: Enable topology preserving mode
        include_properties: Whether to include properties
        all_polylines: All polylines for topology preservation
        
    Returns:
        list: List of rHEALPix feature dictionaries
    """
       # If topology preservation is enabled, calculate appropriate resolution
    if topology:
        if all_polylines is None:
            raise ValueError("all_polylines parameter is required when topology=True")
        shortest_distance = shortest_polyline_distance(all_polylines)
        if shortest_distance > 0:
            for res in range(16):
                _, avg_edge_length, _ = rhealpix_metrics(res)
                cell_diameter = avg_edge_length * 2
                if cell_diameter < shortest_distance:
                    resolution = res
                    break
            else:
                resolution = 15
    rhealpix_features = []
    polylines = []
    if feature.geom_type in ("LineString"):
        polylines = [feature]
    elif feature.geom_type in ("MultiLineString"):
        polylines = list(feature.geoms)

    for polyline in polylines:
        minx, miny, maxx, maxy = polyline.bounds
        bbox_polygon = box(minx, miny, maxx, maxy)
        bbox_center_lon = bbox_polygon.centroid.x
        bbox_center_lat = bbox_polygon.centroid.y
        seed_point = (bbox_center_lon, bbox_center_lat)
        seed_cell = rhealpix_dggs.cell_from_point(resolution, seed_point, plane=False)
        seed_cell_id = str(seed_cell)
        seed_cell_polygon = rhealpix_cell_to_polygon(seed_cell)
        if seed_cell_polygon.contains(bbox_polygon):
            num_edges = 4
            if seed_cell.ellipsoidal_shape() == "dart":
                num_edges = 3
            cell_resolution = resolution
            rhealpix_feature = geodesic_dggs_to_feature(
                "rhealpix", seed_cell_id, cell_resolution, seed_cell_polygon, num_edges
            )
            if feature_properties:
                rhealpix_feature["properties"].update(feature_properties)
            rhealpix_features.append(rhealpix_feature)
            return rhealpix_features
        else:
            covered_cells = set()
            queue = [seed_cell]
            while queue:
                current_cell = queue.pop()
                current_cell_id = str(current_cell)
                if current_cell_id in covered_cells:
                    continue
                covered_cells.add(current_cell_id)
                cell_polygon = rhealpix_cell_to_polygon(current_cell)
                if not cell_polygon.intersects(bbox_polygon):
                    continue
                neighbors = current_cell.neighbors(plane=False)
                for _, neighbor in neighbors.items():
                    neighbor_id = str(neighbor)
                    if neighbor_id not in covered_cells:
                        queue.append(neighbor)
            if compact:
                covered_cells = rhealpix_compact(rhealpix_dggs, covered_cells)
            for cell_id in covered_cells:
                rhealpix_uids = (cell_id[0],) + tuple(map(int, cell_id[1:]))
                rhelpix_cell = rhealpix_dggs.cell(rhealpix_uids)
                cell_resolution = rhelpix_cell.resolution
                cell_polygon = rhealpix_cell_to_polygon(rhelpix_cell)
                if not cell_polygon.intersects(polyline):
                    continue
                num_edges = 4
                if seed_cell.ellipsoidal_shape() == "dart":
                    num_edges = 3
                rhealpix_feature = geodesic_dggs_to_feature(
                    "rhealpix", str(cell_id), cell_resolution, cell_polygon, num_edges
                )
                if feature_properties:
                    rhealpix_feature["properties"].update(feature_properties)
                rhealpix_features.append(rhealpix_feature)

 

    return rhealpix_features


def polygon2rhealpix(
    rhealpix_dggs,
    resolution,
    feature,
    feature_properties=None,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
    all_polygons=None,
):
    """Convert polygon geometry to rHEALPix grid cells.
    
    Args:
        rhealpix_dggs: RHEALPixDGGS instance
        resolution: rHEALPix resolution level
        feature: Polygon or MultiPolygon geometry
        feature_properties: Optional properties to include
        predicate: Spatial predicate for filtering
        compact: Enable compact mode
        topology: Enable topology preserving mode
        include_properties: Whether to include properties
        all_polygons: All polygons for topology preservation
        
    Returns:
        list: List of rHEALPix feature dictionaries
    """
     # If topology preservation is enabled, calculate appropriate resolution
    if topology:
        if all_polygons is None:
            raise ValueError("all_polygons parameter is required when topology=True")
        shortest_distance = shortest_polygon_distance(all_polygons)
        if shortest_distance > 0:
            for res in range(16):
                _, avg_edge_length, _ = rhealpix_metrics(res)
                cell_diameter = avg_edge_length * 2
                if cell_diameter < shortest_distance:
                    resolution = res
                    break
            else:
                resolution = 15
    rhealpix_features = []
    polygons = []
    if feature.geom_type in ("Polygon"):
        polygons = [feature]
    elif feature.geom_type in ("MultiPolygon"):
        polygons = list(feature.geoms)

    for polygon in polygons:
        minx, miny, maxx, maxy = polygon.bounds
        bbox_polygon = box(minx, miny, maxx, maxy)
        bbox_center_lon = bbox_polygon.centroid.x
        bbox_center_lat = bbox_polygon.centroid.y
        seed_point = (bbox_center_lon, bbox_center_lat)
        seed_cell = rhealpix_dggs.cell_from_point(resolution, seed_point, plane=False)
        seed_cell_id = str(seed_cell)
        seed_cell_polygon = rhealpix_cell_to_polygon(seed_cell)
        if seed_cell_polygon.contains(bbox_polygon):
            num_edges = 4
            if seed_cell.ellipsoidal_shape() == "dart":
                num_edges = 3
            cell_resolution = resolution
            rhealpix_feature = geodesic_dggs_to_feature(
                "rhealpix", seed_cell_id, cell_resolution, seed_cell_polygon, num_edges
            )
            if feature_properties:
                rhealpix_feature["properties"].update(feature_properties)
            rhealpix_features.append(rhealpix_feature)
            return rhealpix_features
        else:
            covered_cells = set()
            queue = [seed_cell]
            while queue:
                current_cell = queue.pop()
                current_cell_id = str(current_cell)
                if current_cell_id in covered_cells:
                    continue
                covered_cells.add(current_cell_id)
                cell_polygon = rhealpix_cell_to_polygon(current_cell)
                if not cell_polygon.intersects(bbox_polygon):
                    continue
                neighbors = current_cell.neighbors(plane=False)
                for _, neighbor in neighbors.items():
                    neighbor_id = str(neighbor)
                    if neighbor_id not in covered_cells:
                        queue.append(neighbor)
            if compact:
                covered_cells = rhealpix_compact(rhealpix_dggs, covered_cells)
            for cell_id in covered_cells:
                rhealpix_uids = (cell_id[0],) + tuple(map(int, cell_id[1:]))
                rhelpix_cell = rhealpix_dggs.cell(rhealpix_uids)
                cell_resolution = rhelpix_cell.resolution
                cell_polygon = rhealpix_cell_to_polygon(rhelpix_cell)
                if not check_predicate(cell_polygon, polygon, predicate):
                    continue
                num_edges = 4
                if seed_cell.ellipsoidal_shape() == "dart":
                    num_edges = 3
                rhealpix_feature = geodesic_dggs_to_feature(
                    "rhealpix", str(cell_id), cell_resolution, cell_polygon, num_edges
                )
                if feature_properties:
                    rhealpix_feature["properties"].update(feature_properties)
                rhealpix_features.append(rhealpix_feature)

    return rhealpix_features


def geometry2rhealpix(
    geometries,
    resolution,
    properties_list=None,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
):
    """Convert list of geometries to rHEALPix grid cells.
    
    Args:
        geometries: Single geometry or list of geometries
        resolution: rHEALPix resolution level
        properties_list: Optional list of properties for each geometry
        predicate: Spatial predicate for filtering
        compact: Enable compact mode
        topology: Enable topology preserving mode
        include_properties: Whether to include properties
        
    Returns:
        dict: GeoJSON FeatureCollection with rHEALPix features
    """
    resolution = validate_rhealpix_resolution(resolution)
    # Handle single geometry or list of geometries
    if not isinstance(geometries, list):
        geometries = [geometries]

    # Handle properties
    if properties_list is None:
        properties_list = [{} for _ in geometries]
    elif not isinstance(properties_list, list):
        properties_list = [properties_list for _ in geometries]

    rhealpix_dggs = RHEALPixDGGS()
    rhealpix_features = []

    # Collect all points, polylines, and polygons for topology preservation if needed
    all_points = None
    all_polylines = None
    all_polygons = None
    if topology:
        points_list = []
        polylines_list = []
        polygons_list = []
        for i, geom in enumerate(geometries):
            if geom is None:
                continue
            if geom.geom_type == "Point":
                points_list.append(geom)
            elif geom.geom_type == "MultiPoint":
                points_list.extend(list(geom.geoms))
            elif geom.geom_type == "LineString":
                polylines_list.append(geom)
            elif geom.geom_type == "MultiLineString":
                polylines_list.extend(list(geom.geoms))
            elif geom.geom_type == "Polygon":
                polygons_list.append(geom)
            elif geom.geom_type == "MultiPolygon":
                polygons_list.extend(list(geom.geoms))
        if points_list:
            all_points = MultiPoint(points_list)
        if polylines_list:
            all_polylines = MultiLineString(polylines_list)
        if polygons_list:
            all_polygons = MultiPolygon(polygons_list)

    for idx, geom in enumerate(tqdm(geometries, desc="Processing features")):
        if geom is None:
            continue
        props = (
            properties_list[idx]
            if properties_list and idx < len(properties_list)
            else {}
        )
        if not include_properties:
            props = {}
        if geom.geom_type == "Point":
            rhealpix_features.extend(
                point2rhealpix(
                    rhealpix_dggs,
                    resolution,
                    geom,
                    props,
                    predicate,
                    compact,
                    topology,
                    include_properties,
                    all_points,
                )
            )
        elif geom.geom_type == "MultiPoint":
            for pt in geom.geoms:
                rhealpix_features.extend(
                    point2rhealpix(
                        rhealpix_dggs,
                        resolution,
                        pt,
                        props,
                        predicate,
                        compact,
                        topology,
                        include_properties,
                        all_points,
                    )
                )
        elif geom.geom_type in ("LineString", "MultiLineString"):
            rhealpix_features.extend(
                polyline2rhealpix(
                    rhealpix_dggs,
                    resolution,
                    geom,
                    props,
                    predicate,
                    compact,
                    topology,
                    include_properties,
                    all_polylines,
                )
            )
        elif geom.geom_type in ("Polygon", "MultiPolygon"):
            rhealpix_features.extend(
                polygon2rhealpix(
                    rhealpix_dggs,
                    resolution,
                    geom,
                    props,
                    predicate,
                    compact,
                    topology,
                    include_properties,
                    all_polygons,
                )
            )
    return {"type": "FeatureCollection", "features": rhealpix_features}


def dataframe2rhealpix(
    df,
    resolution,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
):
    """Convert pandas DataFrame with geometry column to rHEALPix grid cells.
    
    Args:
        df: pandas DataFrame with geometry column
        resolution: rHEALPix resolution level
        predicate: Spatial predicate for filtering
        compact: Enable compact mode
        topology: Enable topology preserving mode
        include_properties: Whether to include properties
        
    Returns:
        dict: GeoJSON FeatureCollection with rHEALPix features
    """
    geometries = []
    properties_list = []
    for idx, row in df.iterrows():
        geom = row.geometry if "geometry" in row else row["geometry"]
        if geom is not None:
            geometries.append(geom)
            props = row.to_dict()
            if "geometry" in props:
                del props["geometry"]
            properties_list.append(props)
    return geometry2rhealpix(
        geometries,
        resolution,
        properties_list,
        predicate,
        compact,
        topology,
        include_properties,
    )


def geodataframe2rhealpix(
    gdf,
    resolution,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
):
    """Convert GeoDataFrame to rHEALPix grid cells.
    
    Args:
        gdf: GeoDataFrame with geometry column
        resolution: rHEALPix resolution level
        predicate: Spatial predicate for filtering
        compact: Enable compact mode
        topology: Enable topology preserving mode
        include_properties: Whether to include properties
        
    Returns:
        dict: GeoJSON FeatureCollection with rHEALPix features
    """
    geometries = []
    properties_list = []
    for idx, row in gdf.iterrows():
        geom = row.geometry
        if geom is not None:
            geometries.append(geom)
            props = row.to_dict()
            if "geometry" in props:
                del props["geometry"]
            properties_list.append(props)
    return geometry2rhealpix(
        geometries,
        resolution,
        properties_list,
        predicate,
        compact,
        topology,
        include_properties,
    )


def vector2rhealpix(
    data,
    resolution,
    predicate=None,
    compact=False,
    topology=False,
    output_format="geojson",
    output_path=None,
    include_properties=True,
    **kwargs,
):
    """Convert vector data to rHEALPix grid cells.
    
    Args:
        data: Input data (GeoDataFrame, DataFrame, geometry, GeoJSON dict, or file path)
        resolution: rHEALPix resolution level
        predicate: Spatial predicate for filtering
        compact: Enable compact mode
        topology: Enable topology preserving mode
        output_format: Output output_format (geojson, gpkg, parquet, csv, shapefile)
        output_path: Output file path
        include_properties: Whether to include properties
        **kwargs: Additional arguments for file reading
        
    Returns:
        str or dict: Output file path or GeoJSON FeatureCollection
    """
    if hasattr(data, "geometry") and hasattr(data, "columns"):
        result = geodataframe2rhealpix(
            data, resolution, predicate, compact, topology, include_properties
        )
    elif isinstance(data, pd.DataFrame):
        result = dataframe2rhealpix(
            data, resolution, predicate, compact, topology, include_properties
        )
    elif hasattr(data, "geom_type") or (
        isinstance(data, list) and len(data) > 0 and hasattr(data[0], "geom_type")
    ):
        result = geometry2rhealpix(
            data, resolution, None, predicate, compact, topology, include_properties
        )
    elif isinstance(data, dict) and "type" in data:
        try:
            gdf = gpd.GeoDataFrame.from_features(data["features"])
            result = geodataframe2rhealpix(
                gdf, resolution, predicate, compact, topology, include_properties
            )
        except Exception as e:
            raise ValueError(f"Failed to convert GeoJSON to GeoDataFrame: {str(e)}")
    elif isinstance(data, str):
        try:
            gdf = gpd.read_file(data, **kwargs)
            result = geodataframe2rhealpix(
                gdf, resolution, predicate, compact, topology, include_properties
            )
        except Exception as e:
            raise ValueError(f"Failed to read file/URL {data}: {str(e)}")
    else:
        raise ValueError(f"Unsupported input type: {type(data)}")
    return convert_to_output_format(result, output_format, output_path)


def convert_to_output_format(result, output_format, output_path=None):
    """
    Convert rHEALPix result to specified output output_format.

    Args:
        result (dict): GeoJSON FeatureCollection result
        output_format (str): Desired output output_format
        output_path (str): Output file path (optional)

    Returns:
        dict or str: Output in the specified output_format
    """
    # Check if result has features
    if not result or "features" not in result or not result["features"]:
        print("Warning: No features found in result. This may happen when:")
        print("  - Using 'within' predicate with coarse resolution (cells too large)")
        print("  - Using 'largest_overlap' predicate with no cells having >50% overlap")
        print("  - Input geometry is invalid or empty")
        print("Suggestions:")
        print("  - Try a finer resolution (higher number)")
        print("  - Use 'intersect' or 'centroid_within' predicate instead")
        print("  - Check that input geometry is valid")
        raise ValueError("No features found in result")
    
    # First convert GeoJSON result to GeoDataFrame
    try:
        gdf = gpd.GeoDataFrame.from_features(result["features"])

        # Set CRS to WGS84 (EPSG:4326) since rHEALPix uses WGS84 coordinates
        gdf.set_crs(epsg=4326, inplace=True)
        
        # Ensure the geometry column is set as the active geometry column
        if 'geometry' in gdf.columns:
            gdf.set_geometry('geometry', inplace=True)
        else:
            # If no geometry column found, try to identify it
            geom_cols = [col for col in gdf.columns if hasattr(gdf[col].iloc[0], 'geom_type')]
            if geom_cols:
                gdf.set_geometry(geom_cols[0], inplace=True)
            else:
                raise ValueError("No geometry column found in GeoDataFrame")
        
        # Verify the GeoDataFrame has valid geometry
        if gdf.empty:
            raise ValueError("GeoDataFrame is empty")
        
        if not gdf.geometry.is_valid.all():
            print("Warning: Some geometries are invalid")
    
    except Exception as e:
        print(f"Error creating GeoDataFrame: {str(e)}")
        print(f"Result features count: {len(result['features']) if 'features' in result else 0}")
        if 'features' in result and result['features']:
            print(f"First feature: {result['features'][0]}")
        raise

    if output_format.lower() == "geojson":
        if output_path:
            import json

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f)
            return output_path
        else:
            return result  # Already in GeoJSON output_format

    elif output_format.lower() == "gpkg":
        if output_path:
            gdf.to_file(output_path, driver="GPKG")
            return output_path
        else:
            gdf.to_file("vector2rhealpix.gpkg", driver="GPKG")
            return "vector2rhealpix.gpkg"

    elif output_format.lower() == "parquet":
        if output_path:
            gdf.to_parquet(output_path, index=False)
            return output_path
        else:
            gdf.to_parquet("vector2rhealpix.parquet", index=False)
            return "vector2rhealpix.parquet"

    elif output_format.lower() == "csv":
        if output_path:
            gdf.to_csv(output_path, index=False)
            return output_path
        else:
            return gdf.to_csv(index=False)

    elif output_format.lower() == "shapefile":
        if output_path:
            gdf.to_file(output_path, driver="ESRI Shapefile")
            return output_path
        else:
            gdf.to_file("vector2rhealpix.shp", driver="ESRI Shapefile")
            return "vector2rhealpix.shp"

    else:
        raise ValueError(
            f"Unsupported output output_format: {output_format}. Supported formats: geojson, gpkg, parquet, csv, shapefile"
        )


def vector2rhealpix_cli():
    """Command-line interface for vector2rhealpix conversion."""
    parser = argparse.ArgumentParser(
        description="Convert vector data to rHEALPix grid cells"
    )
    parser.add_argument("-i", "--input", help="Input file path, URL")
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        choices=range(16),
        metavar="[0-15]",
        help="rHEALPix resolution [0..15] (0=coarsest, 15=finest)",
    )
    parser.add_argument(
        "-p",
        "--predicate",
        choices=["intersect", "within", "centroid_within", "largest_overlap"],
        help="Spatial predicate: intersect, within, centroid_within, largest_overlap for polygons",
    )
    parser.add_argument(
        "-c",
        "--compact",
        action="store_true",
        help="Enable rHEALPix compact mode for polygons",
    )
    parser.add_argument(
        "-t", "--topology", action="store_true", help="Enable topology preserving mode"
    )
    parser.add_argument(
        "-np",
        "-no-props",
        dest="include_properties",
        action="store_false",
        help="Do not include original feature properties.",
    )
    parser.add_argument(
        "-f",
        "--output_format",
        default="geojson",
        choices=["geojson", "gpkg", "parquet", "csv", "shapefile"],
        help="Output output_format (default: geojson)",
    )
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    args = parser.parse_args()
    if args.resolution is not None:
        try:
            args.resolution = validate_rhealpix_resolution(args.resolution)
        except (ValueError, TypeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    data = args.input
    output_path = args.output
    if not output_path and args.output_format in [
        "geojson",
        "gpkg",
        "parquet",
        "csv",
        "shapefile",
    ]:
        extensions = {
            "geojson": ".geojson",
            "gpkg": ".gpkg",
            "parquet": ".parquet",
            "csv": ".csv",
            "shapefile": ".shp",
        }
        output_path = f"vector2rhealpix{extensions.get(args.output_format, '')}"
    try:
        vector2rhealpix(
            data,
            args.resolution,
            predicate=args.predicate,
            compact=args.compact,
            topology=args.topology,
            output_format=args.output_format,
            output_path=output_path,
            include_properties=args.include_properties,
        )
        if output_path:
            print(f"Output saved to {output_path}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    vector2rhealpix_cli()
