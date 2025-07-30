import sys
import argparse
import json
import platform
from tqdm import tqdm
from shapely.geometry import box
import pandas as pd
import geopandas as gpd
from vgrid.utils.geometry import check_predicate, shortest_point_distance, shortest_polyline_distance, shortest_polygon_distance
import math
# Import isea4t_metrics locally to avoid circular import

def is_windows():
    return platform.system() == "Windows"

if is_windows():
    from vgrid.dggs.eaggr.eaggr import Eaggr
    from vgrid.dggs.eaggr.shapes.dggs_cell import DggsCell
    from vgrid.dggs.eaggr.enums.model import Model
    from vgrid.dggs.eaggr.enums.shape_string_format import ShapeStringFormat
    from vgrid.dggs.eaggr.shapes.lat_long_point import LatLongPoint
    from vgrid.generator.isea4tgrid import (
        isea4t_res_accuracy_dict,
        fix_isea4t_antimeridian_cells,
        get_isea4t_children_cells_within_bbox,
    )
    from vgrid.conversion.dggscompact import isea4t_compact
    from vgrid.generator.settings import geodesic_dggs_to_feature,isea4t_cell_to_polygon
    isea4t_dggs = Eaggr(Model.ISEA4T)

def validate_isea4t_resolution(resolution):
    """
    Validate that ISEA4T resolution is in the valid range [0..25].

    Args:
        resolution: Resolution value to validate

    Returns:
        int: Validated resolution value

    Raises:
        ValueError: If resolution is not in range [0..25]
        TypeError: If resolution is not an integer
    """
    if not isinstance(resolution, int):
        raise TypeError(
            f"Resolution must be an integer, got {type(resolution).__name__}"
        )

    if resolution < 0 or resolution > 25:
        raise ValueError(f"Resolution must be in range [0..25], got {resolution}")

    return resolution


def point2isea4t(
    resolution,
    point,
    feature_properties=None,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
    all_points=None,
):
    if topology:
        if all_points is None:
            raise ValueError("all_points parameter is required when topology=True")
        shortest_distance = shortest_point_distance(all_points)
        if shortest_distance > 0:
            # Import locally to avoid circular import
            from vgrid.stats.isea4tstats import isea4t_metrics
            for res in range(26):
                _, avg_edge_length, _ = isea4t_metrics(res)
                cell_diameter = avg_edge_length * 2
                if cell_diameter < shortest_distance:
                    resolution = res
                    break
            else:
                resolution = 25
    isea4t_features = []
    accuracy = isea4t_res_accuracy_dict.get(resolution)
    lat_long_point = LatLongPoint(point.y, point.x, accuracy)
    isea4t_cell = isea4t_dggs.convert_point_to_dggs_cell(lat_long_point)
    isea4t_id = isea4t_cell.get_cell_id()
    cell_polygon = isea4t_cell_to_polygon(isea4t_cell)
    if isea4t_id.startswith(("00", "09", "14", "04", "19")):
        cell_polygon = fix_isea4t_antimeridian_cells(cell_polygon)
    if cell_polygon:
        num_edges = 3
        isea4t_feature = geodesic_dggs_to_feature(
            "isea4t", isea4t_id, resolution, cell_polygon, num_edges
        )
        if include_properties and feature_properties:
            isea4t_feature["properties"].update(feature_properties)
        isea4t_features.append(isea4t_feature)
    return isea4t_features


def polyline2isea4t(
    resolution,
    feature,
    feature_properties=None,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
    all_polylines=None,
):
    if topology:
        if all_polylines is None:
            raise ValueError("all_polylines parameter is required when topology=True")
        shortest_distance = shortest_polyline_distance(all_polylines)
        if shortest_distance > 0:
            # Import locally to avoid circular import
            from vgrid.stats.isea4tstats import isea4t_metrics
            for res in range(26):
                _, avg_edge_length, _ = isea4t_metrics(res)
                cell_diameter = avg_edge_length * 4
                if cell_diameter < shortest_distance:
                    resolution = res
                    break
            else:
                resolution = 25
    isea4t_features = []
    if feature.geom_type in ("LineString"):
        polylines = [feature]
    elif feature.geom_type in ("MultiLineString"):
        polylines = list(feature.geoms)
    else:
        return []
    for polyline in polylines:
        accuracy = isea4t_res_accuracy_dict.get(resolution)
        bounding_box = box(*polyline.bounds)
        bounding_box_wkt = bounding_box.wkt
        shapes = isea4t_dggs.convert_shape_string_to_dggs_shapes(
            bounding_box_wkt, ShapeStringFormat.WKT, accuracy
        )
        shape = shapes[0]
        bbox_cells = shape.get_shape().get_outer_ring().get_cells()
        bounding_cell = isea4t_dggs.get_bounding_dggs_cell(bbox_cells)
        bounding_child_cells = get_isea4t_children_cells_within_bbox(
            bounding_cell.get_cell_id(), bounding_box, resolution
        )
        if compact:
            bounding_child_cells = isea4t_compact(bounding_child_cells)
        for child in bounding_child_cells:
            isea4t_cell = DggsCell(child)
            cell_polygon = isea4t_cell_to_polygon(isea4t_cell)
            isea4t_id = isea4t_cell.get_cell_id()
            if isea4t_id.startswith(("00", "09", "14", "04", "19")):
                cell_polygon = fix_isea4t_antimeridian_cells(cell_polygon)
            if cell_polygon.intersects(polyline):
                num_edges = 3
                cell_resolution = len(isea4t_id) - 2
                isea4t_feature = geodesic_dggs_to_feature(
                    "isea4t", isea4t_id, cell_resolution, cell_polygon, num_edges
                )
                if include_properties and feature_properties:
                    isea4t_feature["properties"].update(feature_properties)
                isea4t_features.append(isea4t_feature)
    return isea4t_features


def polygon2isea4t(
    resolution,
    feature,
    feature_properties=None,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
    all_polygons=None,
):
    if topology:
        if all_polygons is None:
            raise ValueError("all_polygons parameter is required when topology=True")
        shortest_distance = shortest_polygon_distance(all_polygons)
        if shortest_distance > 0:
            # Import locally to avoid circular import
            from vgrid.stats.isea4tstats import isea4t_metrics
            for res in range(26):
                _, avg_edge_length, _ = isea4t_metrics(res)
                cell_diameter = avg_edge_length * 4
                if cell_diameter < shortest_distance:
                    resolution = res
                    break
            else:
                resolution = 25
    isea4t_features = []
    if feature.geom_type in ("Polygon"):
        polygons = [feature]
    elif feature.geom_type in ("MultiPolygon"):
        polygons = list(feature.geoms)
    else:
        return []
    for polygon in polygons:
        accuracy = isea4t_res_accuracy_dict.get(resolution)
        bounding_box = box(*polygon.bounds)
        bounding_box_wkt = bounding_box.wkt
        shapes = isea4t_dggs.convert_shape_string_to_dggs_shapes(
            bounding_box_wkt, ShapeStringFormat.WKT, accuracy
        )
        shape = shapes[0]
        bbox_cells = shape.get_shape().get_outer_ring().get_cells()
        bounding_cell = isea4t_dggs.get_bounding_dggs_cell(bbox_cells)
        bounding_child_cells = get_isea4t_children_cells_within_bbox(
            bounding_cell.get_cell_id(), bounding_box, resolution
        )
        if compact:
            bounding_child_cells = isea4t_compact(bounding_child_cells)
        for child in bounding_child_cells:
            isea4t_cell = DggsCell(child)
            cell_polygon = isea4t_cell_to_polygon(isea4t_cell)
            isea4t_id = isea4t_cell.get_cell_id()
            if isea4t_id.startswith(("00", "09", "14", "04", "19")):
                cell_polygon = fix_isea4t_antimeridian_cells(cell_polygon)
            if check_predicate(cell_polygon, polygon, predicate):
                num_edges = 3
                cell_resolution = len(isea4t_id) - 2
                isea4t_feature = geodesic_dggs_to_feature(
                    "isea4t", isea4t_id, cell_resolution, cell_polygon, num_edges
                )
                if include_properties and feature_properties:
                    isea4t_feature["properties"].update(feature_properties)
                isea4t_features.append(isea4t_feature)
    return isea4t_features


def geometry2isea4t(
    geometries,
    resolution,
    properties_list=None,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
):
    if not is_windows():
        raise NotImplementedError("ISEA4T DGGS conversion is only supported on Windows")

    resolution = validate_isea4t_resolution(resolution)
    # Handle single geometry or list of geometries
    if not isinstance(geometries, list):
        geometries = [geometries]

    # Handle properties
    if properties_list is None:
        properties_list = [{} for _ in geometries]
    elif not isinstance(properties_list, list):
        properties_list = [properties_list for _ in geometries]

    isea4t_features = []
    # Collect all points, polylines, and polygons for topology preservation if needed
    all_points = None
    all_polylines = None
    all_polygons = None
    if topology:
        from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon
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
            isea4t_features.extend(
                point2isea4t(
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
                isea4t_features.extend(
                    point2isea4t(
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
            isea4t_features.extend(
                polyline2isea4t(
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
            isea4t_features.extend(
                polygon2isea4t(
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
    return {"type": "FeatureCollection", "features": isea4t_features}


def dataframe2isea4t(
    df,
    resolution,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
):
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
    return geometry2isea4t(
        geometries,
        resolution,
        properties_list,
        predicate,
        compact,
        topology,
        include_properties,
    )


def geodataframe2isea4t(
    gdf,
    resolution,
    predicate=None,
    compact=False,
    topology=False,
    include_properties=True,
):
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
    return geometry2isea4t(
        geometries,
        resolution,
        properties_list,
        predicate,
        compact,
        topology,
        include_properties,
    )


def vector2isea4t(
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
    if not is_windows():
        raise NotImplementedError("ISEA4T DGGS conversion is only supported on Windows")

    if hasattr(data, "geometry") and hasattr(data, "columns"):
        result = geodataframe2isea4t(
            data, resolution, predicate, compact, topology, include_properties
        )
    elif isinstance(data, pd.DataFrame):
        result = dataframe2isea4t(
            data, resolution, predicate, compact, topology, include_properties
        )
    elif hasattr(data, "geom_type") or (
        isinstance(data, list) and len(data) > 0 and hasattr(data[0], "geom_type")
    ):
        result = geometry2isea4t(
            data, resolution, None, predicate, compact, topology, include_properties
        )
    elif isinstance(data, dict) and "type" in data:
        try:
            gdf = gpd.GeoDataFrame.from_features(data["features"])
            result = geodataframe2isea4t(
                gdf, resolution, predicate, compact, topology, include_properties
            )
        except Exception as e:
            raise ValueError(f"Failed to convert GeoJSON to GeoDataFrame: {str(e)}")
    elif isinstance(data, str):
        try:
            gdf = gpd.read_file(data, **kwargs)
            result = geodataframe2isea4t(
                gdf, resolution, predicate, compact, topology, include_properties
            )
        except Exception as e:
            raise ValueError(f"Failed to read file/URL {data}: {str(e)}")
    else:
        raise ValueError(f"Unsupported input type: {type(data)}")
    return convert_to_output_format(result, output_format, output_path)


def convert_to_output_format(result, output_format, output_path=None):
    """
    Convert ISEA4T result to specified output output_format.

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

        # Set CRS to WGS84 (EPSG:4326) since ISEA4T uses WGS84 coordinates
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
            gdf.to_file("vector2isea4t.gpkg", driver="GPKG")
            return "vector2isea4t.gpkg"

    elif output_format.lower() == "parquet":
        if output_path:
            gdf.to_parquet(output_path, index=False)
            return output_path
        else:
            gdf.to_parquet("vector2isea4t.parquet", index=False)
            return "vector2isea4t.parquet"

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
            gdf.to_file("vector2isea4t.shp", driver="ESRI Shapefile")
            return "vector2isea4t.shp"

    else:
        raise ValueError(
            f"Unsupported output output_format: {output_format}. Supported formats: geojson, gpkg, parquet, csv, shapefile"
        )


def vector2isea4t_cli():
    parser = argparse.ArgumentParser(
        description="Convert vector data to ISEA4T grid cells (Windows only)"
    )
    parser.add_argument("-i", "--input", help="Input file path, URL")
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        choices=range(26),
        metavar="[0-25]",
        help="ISEA4T resolution [0..25] (0=coarsest, 25=finest)",
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
        help="Enable ISEA4T compact mode for polygons",
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
    if not is_windows():
        print("ISEA4T DGGS conversion is only supported on Windows", file=sys.stderr)
        sys.exit(1)

    if args.resolution is not None:
        try:
            args.resolution = validate_isea4t_resolution(args.resolution)
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
        output_path = f"vector2isea4t{extensions.get(args.output_format, '')}"
    try:
        vector2isea4t(
            data,
            args.resolution,
            predicate=args.predicate,
            compact=args.compact,
            topology=args.topology,
            include_properties=args.include_properties,
            output_format=args.output_format,
            output_path=output_path,
        )
        if output_path:
            print(f"Output saved to {output_path}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    vector2isea4t_cli()
