import argparse
import json
import os
from shapely.geometry import Polygon
from tqdm import tqdm
from shapely.geometry import shape, box, Point, LineString
from pyproj import Geod
import platform
import geopandas as gpd
import pandas as pd

if platform.system() == "Linux":
    from vgrid.utils.dggrid4py import DGGRIDv7, dggs_types
    from vgrid.utils.dggrid4py.dggrid_runner import output_address_types

geod = Geod(ellps="WGS84")


# Function to generate grid for Point
def point_to_grid(dggrid_instance, dggs_type, res, address_type, geometry):
    """
    Generate DGGRID cell(s) for a Point or MultiPoint geometry.

    Args:
        dggrid_instance: DGGRIDv7 instance for grid operations.
        dggs_type (str): Type of DGGS (e.g., ISEA4H, FULLER, etc.).
        res (int): Resolution for the DGGRID.
        address_type (str): Address type for the output grid cells.
        geometry (shapely.geometry.Point or MultiPoint): Input geometry.

    Returns:
        str: GeoJSON FeatureCollection as a string containing the grid cell(s).
    """
    # Initialize an empty list to store filtered grid cells
    merged_grids = []

    # Check the geometry type
    if geometry.geom_type == "Point":
        # Handle single Point
        points = [geometry]
    elif geometry.geom_type == "MultiPoint":
        # Handle MultiPoint: process each point separately
        points = list(geometry)

    # Process each point
    for point in points:
        # Create a GeoDataFrame for the point in EPSG:4326 CRS
        geodf_points_wgs84 = gpd.GeoDataFrame([{"geometry": point}], crs="EPSG:4326")

        # Get DGGRID cell ID for the point
        dggrid_cell = dggrid_instance.cells_for_geo_points(
            geodf_points_wgs84=geodf_points_wgs84,
            cell_ids_only=True,
            dggs_type=dggs_type,
            resolution=res,
        )

        dggrid_seqnum = dggrid_cell.loc[0, "seqnums"]  # Use 'seqnums' column by default
        # Get the polygon representation of the cell using the cell ID
        dggrid_cell = dggrid_instance.grid_cell_polygons_from_cellids(
            [dggrid_seqnum],
            dggs_type=dggs_type,
            resolution=res,
            split_dateline=True,
            clip_cell_res=1,
            input_address_type="SEQNUM",
            # output_address_type=address_type
        )

        # Ensure the geometry column is set
        gdf = dggrid_cell.set_geometry("geometry")

        # Ensure the CRS is set to EPSG:4326
        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)
        elif not gdf.crs.equals("EPSG:4326"):
            gdf = gdf.to_crs(epsg=4326)

        try:
            if address_type != "SEQNUM":
                address_type_transform = dggrid_instance.address_transform(
                    [dggrid_seqnum],
                    dggs_type=dggs_type,
                    resolution=res,
                    mixed_aperture_level=None,
                    input_address_type="SEQNUM",
                    output_address_type=address_type,
                )
                gdf["name"] = gdf["name"].astype(
                    str
                )  # Convert the column to string type
                gdf.loc[0, "name"] = address_type_transform.loc[0, address_type]
                gdf = gdf.rename(columns={"name": address_type.lower()})
            else:
                gdf = gdf.rename(columns={"name": "seqnum"})
        except Exception:
            pass

        # Append the filtered GeoDataFrame to the list
        merged_grids.append(gdf)

    # Merge all filtered grids into one GeoDataFrame
    if merged_grids:
        final_grid = gpd.GeoDataFrame(
            pd.concat(merged_grids, ignore_index=True), crs=merged_grids[0].crs
        )
    else:
        final_grid = gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")

    # Convert the GeoDataFrame to a GeoJSON feature collection
    feature_collection = final_grid.to_json()
    return feature_collection


# Function to generate grid for Polyline
def polyline_to_grid(dggrid_instance, dggs_type, res, address_type, geometry):
    """
    Generate DGGRID cells intersecting with a LineString or MultiLineString geometry.

    Args:
        dggrid_instance: DGGRIDv7 instance for grid operations.
        dggs_type (str): Type of DGGS (e.g., ISEA4H, FULLER, etc.).
        res (int): Resolution for the DGGRID.
        address_type (str): Address type for the output grid cells.
        geometry (shapely.geometry.LineString or MultiLineString): Input geometry.

    Returns:
        geopandas.GeoDataFrame: GeoDataFrame containing DGGRID cells intersecting with the input geometry.
    """
    # Initialize an empty list to store filtered grid cells
    merged_grids = []

    # Check the geometry type
    if geometry.geom_type == "LineString":
        # Handle single LineString
        polylines = [geometry]
    elif geometry.geom_type == "MultiLineString":
        # Handle MultiLineString: process each line separately
        polylines = list(geometry.geoms)

    # Process each polyline
    for polyline in polylines:
        # Get bounding box for the current polyline
        bounding_box = box(*polyline.bounds)

        # Generate grid cells for the bounding box
        dggrid_gdf = dggrid_instance.grid_cell_polygons_for_extent(
            dggs_type,
            res,
            clip_geom=bounding_box,
            split_dateline=True,
            output_address_type=address_type,
        )

        # Keep only grid cells that intersect the polyline
        dggrid_gdf = dggrid_gdf[dggrid_gdf.intersects(polyline)]

        try:
            if address_type != "SEQNUM":

                def address_transform(
                    dggrid_seqnum, dggs_type, resolution, address_type
                ):
                    address_type_transform = dggrid_instance.address_transform(
                        [dggrid_seqnum],
                        dggs_type=dggs_type,
                        resolution=resolution,
                        mixed_aperture_level=None,
                        input_address_type="SEQNUM",
                        output_address_type=address_type,
                    )
                    return address_type_transform.loc[0, address_type]

                dggrid_gdf["name"] = dggrid_gdf["name"].astype(str)
                dggrid_gdf["name"] = dggrid_gdf["name"].apply(
                    lambda val: address_transform(val, dggs_type, res, address_type)
                )
                dggrid_gdf = dggrid_gdf.rename(columns={"name": address_type.lower()})
            else:
                dggrid_gdf = dggrid_gdf.rename(columns={"name": "seqnum"})

        except Exception:
            pass
        # Append the filtered GeoDataFrame to the list
        merged_grids.append(dggrid_gdf)

    # Merge all filtered grids into one GeoDataFrame
    if merged_grids:
        final_grid = gpd.GeoDataFrame(
            pd.concat(merged_grids, ignore_index=True), crs=merged_grids[0].crs
        )
    else:
        final_grid = gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")

    return final_grid


def polygon_to_grid(dggrid_instance, dggs_type, res, address_type, geometry):
    """
    Generate DGGRID cells intersecting with a given polygon or multipolygon geometry.

    Args:
        dggrid_instance: DGGRIDv7 instance for grid operations.
        dggs_type (str): Type of DGGS (e.g., ISEA4H, FULLER, etc.).
        res (int): Resolution for the DGGRID.
        address_type (str): Address type for the output grid cells.
        geometry (shapely.geometry.Polygon or MultiPolygon): Input geometry.

    Returns:
        geopandas.GeoDataFrame: GeoDataFrame containing DGGRID cells intersecting with the input geometry.
    """
    # Initialize an empty list to store filtered grid cells
    merged_grids = []

    # Check the geometry type
    if geometry.geom_type == "Polygon":
        # Handle single Polygon
        polygons = [geometry]
    elif geometry.geom_type == "MultiPolygon":
        # Handle MultiPolygon: process each polygon separately
        polygons = list(geometry.geoms)  # Use .geoms to get components of MultiPolygon

    # Process each polygon
    for polygon in polygons:
        # Get bounding box for the current polygon
        bounding_box = box(*polygon.bounds)

        # Generate grid cells for the bounding box
        dggrid_gdf = dggrid_instance.grid_cell_polygons_for_extent(
            dggs_type,
            res,
            clip_geom=bounding_box,
            split_dateline=True,
            output_address_type=address_type,
        )

        # Keep only grid cells that intersect the polygon
        dggrid_gdf = dggrid_gdf[dggrid_gdf.intersects(polygon)]
        try:
            if address_type != "SEQNUM":

                def address_transform(
                    dggrid_seqnum, dggs_type, resolution, address_type
                ):
                    address_type_transform = dggrid_instance.address_transform(
                        [dggrid_seqnum],
                        dggs_type=dggs_type,
                        resolution=resolution,
                        mixed_aperture_level=None,
                        input_address_type="SEQNUM",
                        output_address_type=address_type,
                    )
                    return address_type_transform.loc[0, address_type]

                dggrid_gdf["name"] = dggrid_gdf["name"].astype(str)
                dggrid_gdf["name"] = dggrid_gdf["name"].apply(
                    lambda val: address_transform(val, dggs_type, res, address_type)
                )
                dggrid_gdf = dggrid_gdf.rename(columns={"name": address_type.lower()})
            else:
                dggrid_gdf = dggrid_gdf.rename(columns={"name": "seqnum"})

        except Exception:
            pass

        # Append the filtered GeoDataFrame to the list
        merged_grids.append(dggrid_gdf)

    # Merge all filtered grids into one GeoDataFrame
    if merged_grids:
        final_grid = gpd.GeoDataFrame(
            pd.concat(merged_grids, ignore_index=True), crs=merged_grids[0].crs
        )
    else:
        final_grid = gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")

    return final_grid


def convert_to_output_format(result, output_format, output_path=None):
    """
    Convert DGGRID result to specified output output_format.

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

        # Set CRS to WGS84 (EPSG:4326) since DGGRID uses WGS84 coordinates
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
            gdf.to_file("vector2dggrid.gpkg", driver="GPKG")
            return "vector2dggrid.gpkg"

    elif output_format.lower() == "parquet":
        if output_path:
            gdf.to_parquet(output_path, index=False)
            return output_path
        else:
            gdf.to_parquet("vector2dggrid.parquet", index=False)
            return "vector2dggrid.parquet"

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
            gdf.to_file("vector2dggrid.shp", driver="ESRI Shapefile")
            return "vector2dggrid.shp"

    else:
        raise ValueError(
            f"Unsupported output output_format: {output_format}. Supported formats: geojson, gpkg, parquet, csv, shapefile"
        )


def main():
    """
    Command-line interface for converting GeoJSON to DGGRID grid cells.

    Usage:
        python vector2dggrid.py -t <dggs_type> -r <resolution> -a <address_type> -geojson <geojson_file>

    Arguments:
        -t, --dggs_type: DGGS type (e.g., ISEA4H, FULLER, etc.)
        -r, --resolution: Resolution for the DGGRID
        -a, --address_type: Output address type (default: SEQNUM)
        -geojson, --geojson: Path to GeoJSON file with Point, Polyline, or Polygon

    The function reads the input GeoJSON, processes each feature, and writes the output as a new GeoJSON file with grid cells.
    """
    if platform.system() == "Linux":
        parser = argparse.ArgumentParser(description="Convert GeoJSON to DGGRID")
        parser.add_argument(
            "-t",
            "--dggs_type",
            choices=dggs_types,
            help="Select a DGGS type from the available options.",
        )
        parser.add_argument(
            "-r", "--resolution", type=int, required=True, help="resolution"
        )
        parser.add_argument(
            "-a",
            "--address_type",
            choices=output_address_types,
            default="SEQNUM",
            nargs="?",  # This makes the argument optional
            help="Select an output address type from the available options.",
        )

        parser.add_argument(
            "-geojson",
            "--geojson",
            type=str,
            required=True,
            help="GeoJSON string with Point, Polyline or Polygon",
        )
        dggrid_instance = DGGRIDv7(
            executable="/usr/local/bin/dggrid",
            working_dir=".",
            capture_logs=False,
            silent=True,
            tmp_geo_out_legacy=False,
            debug=False,
        )
        args = parser.parse_args()
        dggs_type = args.dggs_type
        resolution = args.resolution
        address_type = args.address_type
        geojson = args.geojson

        if not os.path.exists(geojson):
            print(f"Error: The file {geojson} does not exist.")
            return

        with open(geojson, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

            # Initialize a list to store all grid cells
        all_cells = []
        geojson_features = []
        for feature in tqdm(geojson_data["features"], desc="Processing features"):
            if feature["geometry"]["type"] in ["Point", "MultiPoint"]:
                coordinates = feature["geometry"]["coordinates"]

                if feature["geometry"]["type"] in ["Point", "MultiPoint"]:
                    coordinates = feature["geometry"]["coordinates"]

                    if feature["geometry"]["type"] == "Point":
                        # Create a Point geometry
                        point = Point(coordinates)
                        point_features_json = point_to_grid(
                            dggrid_instance, dggs_type, resolution, address_type, point
                        )

                        # Parse the GeoJSON string if it's returned as a string
                        point_features = json.loads(point_features_json)

                        # Assuming point_features is a GeoJSON with 'features'
                        geojson_features.extend(point_features["features"])

                    elif feature["geometry"]["type"] == "MultiPoint":
                        # Process each coordinate set in MultiPoint
                        for point_coords in coordinates:
                            point = Point(
                                point_coords
                            )  # Create Point for each coordinate set
                            point_features_json = point_to_grid(
                                dggrid_instance,
                                dggs_type,
                                resolution,
                                address_type,
                                point,
                            )

                            # Parse the GeoJSON string if it's returned as a string
                            point_features = json.loads(point_features_json)

                            # Append the point features to the list
                            geojson_features.extend(point_features["features"])

            elif feature["geometry"]["type"] in ["LineString", "MultiLineString"]:
                coordinates = feature["geometry"]["coordinates"]
                if feature["geometry"]["type"] == "LineString":
                    # Directly process LineString geometry
                    polyline = LineString(coordinates)
                    cells_gdf = polyline_to_grid(
                        dggrid_instance, dggs_type, resolution, address_type, polyline
                    )
                    all_cells.append(cells_gdf)
                elif feature["geometry"]["type"] == "MultiLineString":
                    # Process each LineString in MultiLineString
                    multilines = shape(feature["geometry"])
                    cells_gdf = polyline_to_grid(
                        dggrid_instance, dggs_type, resolution, address_type, multilines
                    )
                    all_cells.append(cells_gdf)

            if feature["geometry"]["type"] in ["Polygon", "MultiPolygon"]:
                coordinates = feature["geometry"]["coordinates"]
                if feature["geometry"]["type"] == "Polygon":
                    # Extract exterior and interior rings
                    exterior_ring = coordinates[
                        0
                    ]  # The first coordinate set is the exterior ring
                    interior_rings = coordinates[
                        1:
                    ]  # Remaining coordinate sets are interior rings (holes)
                    polygon = Polygon(exterior_ring, interior_rings)

                    # Process the polygon with interior rings
                    cells_gdf = polygon_to_grid(
                        dggrid_instance, dggs_type, resolution, address_type, polygon
                    )
                    all_cells.append(cells_gdf)

                elif feature["geometry"]["type"] == "MultiPolygon":
                    # Process each polygon in MultiPolygon
                    multipolygon = shape(
                        feature["geometry"]
                    )  # Convert MultiPolygon from GeoJSON to Shapely object

                    for (
                        polygon
                    ) in multipolygon.geoms:  # Iterate over individual polygons
                        # Extract exterior and interior rings
                        exterior_ring = polygon.exterior.coords
                        interior_rings = [ring.coords for ring in polygon.interiors]
                        polygon_with_holes = Polygon(exterior_ring, interior_rings)

                        # Process the polygon with interior rings
                        cells_gdf = polygon_to_grid(
                            dggrid_instance,
                            dggs_type,
                            resolution,
                            address_type,
                            polygon_with_holes,
                        )
                        all_cells.append(cells_gdf)

        # Merge all collected GeoDataFrames
        geojson_path = f"geojson2dggrid_{dggs_type}_{resolution}_{address_type}.geojson"

        if geojson_features:
            with open(geojson_path, "w") as f:
                json.dump(
                    {"type": "FeatureCollection", "features": geojson_features}, f
                )
        elif all_cells:
            final_gdf = gpd.GeoDataFrame(
                pd.concat(all_cells, ignore_index=True), crs=all_cells[0].crs
            )
            final_gdf.to_file(geojson_path, driver="GeoJSON")

        print(f"DGGRID GeoJSON saved as {geojson_path}")


if __name__ == "__main__":
    main()
