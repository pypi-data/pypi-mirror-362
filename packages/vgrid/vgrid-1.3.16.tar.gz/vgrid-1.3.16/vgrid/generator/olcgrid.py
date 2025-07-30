import json
import argparse
from vgrid.dggs import olc
from tqdm import tqdm
from shapely.geometry import shape, box, Polygon
from vgrid.generator.settings import MAX_CELLS, graticule_dggs_to_feature
from shapely.ops import unary_union


def calculate_total_cells(resolution, bbox):
    """Calculate the total number of cells within the bounding box for a given resolution."""
    area = olc.decode(
        olc.encode(bbox[1], bbox[0], resolution)
    )  # Use bbox min lat, min lon for the area
    lat_step = area.latitudeHi - area.latitudeLo
    lng_step = area.longitudeHi - area.longitudeLo

    sw_lng, sw_lat, ne_lng, ne_lat = bbox
    total_lat_steps = int((ne_lat - sw_lat) / lat_step)
    total_lng_steps = int((ne_lng - sw_lng) / lng_step)

    return total_lat_steps * total_lng_steps


def generate_grid(resolution, verbose=True):
    """
    Generate a global grid of Open Location Codes (Plus Codes) at the specified precision
    as a GeoJSON-like feature collection.
    """
    # Define the boundaries of the world
    sw_lat, sw_lng = -90, -180
    ne_lat, ne_lng = 90, 180

    # Get the precision step size
    area = olc.decode(olc.encode(sw_lat, sw_lng, resolution))
    lat_step = area.latitudeHi - area.latitudeLo
    lng_step = area.longitudeHi - area.longitudeLo

    olc_features = []

    # Calculate the total number of steps for progress tracking
    total_lat_steps = int((ne_lat - sw_lat) / lat_step)
    total_lng_steps = int((ne_lng - sw_lng) / lng_step)
    total_steps = total_lat_steps * total_lng_steps

    with tqdm(
        total=total_steps,
        desc="Generating OLC DGGS",
        unit=" cells",
        disable=not verbose,
    ) as pbar:
        lat = sw_lat
        while lat < ne_lat:
            lng = sw_lng
            while lng < ne_lng:
                # Generate the Plus Code for the center of the cell
                center_lat = lat + lat_step / 2
                center_lon = lng + lng_step / 2
                olc_id = olc.encode(center_lat, center_lon, resolution)
                resolution = olc.decode(olc_id).codeLength
                cell_polygon = Polygon(
                    [
                        [lng, lat],  # SW
                        [lng, lat + lat_step],  # NW
                        [lng + lng_step, lat + lat_step],  # NE
                        [lng + lng_step, lat],  # SE
                        [lng, lat],  # Close the polygon
                    ]
                )
                olc_feature = graticule_dggs_to_feature(
                    "olc", olc_id, resolution, cell_polygon
                )
                olc_features.append(olc_feature)
                lng += lng_step
                pbar.update(1)  # Update progress bar
            lat += lat_step

    # Return the feature collection
    return {"type": "FeatureCollection", "features": olc_features}


def generate_grid_within_bbox(resolution, bbox):
    """
    Generate a grid of Open Location Codes (Plus Codes) within the specified bounding box.
    """
    min_lon, min_lat, max_lon, max_lat = bbox
    bbox_poly = box(min_lon, min_lat, max_lon, max_lat)

    # Step 1: Generate base cells at the lowest resolution (e.g., resolution 2)
    base_resolution = 2
    base_cells = generate_grid(base_resolution, verbose=False)

    # Step 2: Identify seed cells that intersect with the bounding box
    seed_cells = []
    for base_cell in base_cells["features"]:
        base_cell_poly = Polygon(base_cell["geometry"]["coordinates"][0])
        if bbox_poly.intersects(base_cell_poly):
            seed_cells.append(base_cell)

    refined_features = []

    # Step 3: Iterate over seed cells and refine to the output resolution
    for seed_cell in seed_cells:
        seed_cell_poly = Polygon(seed_cell["geometry"]["coordinates"][0])

        if seed_cell_poly.contains(bbox_poly) and resolution == base_resolution:
            # Append the seed cell directly if fully contained and resolution matches
            refined_features.append(seed_cell)
        else:
            # Refine the seed cell to the output resolution and add it to the output
            refined_features.extend(
                refine_cell(
                    seed_cell_poly.bounds, base_resolution, resolution, bbox_poly
                )
            )

    resolution_features = [
        feature
        for feature in refined_features
        if feature["properties"]["resolution"] == resolution
    ]

    final_features = []
    seen_olc_ids = set()  # Reset the set for final feature filtering

    for feature in resolution_features:
        olc_id = feature["properties"]["olc"]
        if olc_id not in seen_olc_ids:  # Check if OLC code is already in the set
            final_features.append(feature)
            seen_olc_ids.add(olc_id)

    return {"type": "FeatureCollection", "features": final_features}


def refine_cell(bounds, current_resolution, target_resolution, bbox_poly):
    """
    Refine a cell defined by bounds to the target resolution, recursively refining intersecting cells.
    """
    min_lon, min_lat, max_lon, max_lat = bounds
    if current_resolution < 10:
        valid_resolution = current_resolution + 2
    else:
        valid_resolution = current_resolution + 1

    area = olc.decode(olc.encode(min_lat, min_lon, valid_resolution))
    lat_step = area.latitudeHi - area.latitudeLo
    lng_step = area.longitudeHi - area.longitudeLo

    olc_features = []
    lat = min_lat
    while lat < max_lat:
        lng = min_lon
        while lng < max_lon:
            # Define the bounds of the finer cell
            finer_cell_bounds = (lng, lat, lng + lng_step, lat + lat_step)
            finer_cell_poly = box(*finer_cell_bounds)

            if bbox_poly.intersects(finer_cell_poly):
                # Generate the Plus Code for the center of the finer cell
                center_lat = lat + lat_step / 2
                center_lon = lng + lng_step / 2
                olc_id = olc.encode(center_lat, center_lon, valid_resolution)
                resolution = olc.decode(olc_id).codeLength

                cell_polygon = Polygon(
                    [
                        [lng, lat],  # SW
                        [lng, lat + lat_step],  # NW
                        [lng + lng_step, lat + lat_step],  # NE
                        [lng + lng_step, lat],  # SE
                        [lng, lat],  # Close the polygon
                    ]
                )

                olc_feature = graticule_dggs_to_feature(
                    "olc", olc_id, resolution, cell_polygon
                )
                olc_features.append(olc_feature)

                # Recursively refine the cell if not at target resolution
                if valid_resolution < target_resolution:
                    olc_features.extend(
                        refine_cell(
                            finer_cell_bounds,
                            valid_resolution,
                            target_resolution,
                            bbox_poly,
                        )
                    )

            lng += lng_step
            # pbar.update(1)
        lat += lat_step

    return olc_features


def generate_grid_resample(resolution, geojson_features):
    """
    Generate a grid of Open Location Codes (Plus Codes) within the specified GeoJSON features.
    """
    # Step 1: Union all input geometries
    geometries = [
        shape(feature["geometry"]) for feature in geojson_features["features"]
    ]
    unified_geom = unary_union(geometries)

    # Step 2: Generate base cells at the lowest resolution (e.g., resolution 2)
    base_resolution = 2
    base_cells = generate_grid(base_resolution, verbose=True)

    # Step 3: Identify seed cells that intersect with the unified geometry
    seed_cells = []
    for base_cell in base_cells["features"]:
        base_cell_poly = Polygon(base_cell["geometry"]["coordinates"][0])
        if unified_geom.intersects(base_cell_poly):
            seed_cells.append(base_cell)

    refined_features = []

    # Step 4: Refine seed cells to the desired resolution
    for seed_cell in seed_cells:
        seed_cell_poly = Polygon(seed_cell["geometry"]["coordinates"][0])

        if seed_cell_poly.contains(unified_geom) and resolution == base_resolution:
            refined_features.append(seed_cell)
        else:
            refined_features.extend(
                refine_cell(
                    seed_cell_poly.bounds, base_resolution, resolution, unified_geom
                )
            )

    # Step 5: Filter features to keep only those at the desired resolution and remove duplicates
    resolution_features = [
        feature
        for feature in refined_features
        if feature["properties"]["resolution"] == resolution
    ]

    final_features = []
    seen_olc_ids = set()

    for feature in resolution_features:
        olc_id = feature["properties"]["olc"]
        if olc_id not in seen_olc_ids:
            final_features.append(feature)
            seen_olc_ids.add(olc_id)

    return {"type": "FeatureCollection", "features": final_features}


def convert_olcgrid_output_format(olc_features, output_format=None, output_path=None, resolution=None):
    if not olc_features:
        return []
    def default_path(ext):
        return f"olc_grid_{resolution}.{ext}" if resolution is not None else f"olc_grid.{ext}"
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import shape
    if output_format is None:
        return [f["properties"]["olc"] for f in olc_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in olc_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(olc_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(olc_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(olc_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(olc_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(olc_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(olc_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")

def olcgrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate OLC grid for pure Python usage.

    Args:
        resolution (int): OLC resolution [2..15]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output format ('geojson', 'csv', 'geo', 'gpd', 'shapefile', 'gpkg', 'parquet', or None for list of OLC IDs).
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict, list, or str: Output in the requested format or file path.
    """
    if resolution < 2 or resolution > 15:
        raise ValueError("Resolution must be in range [2..15]")

    if bbox is None:
        bbox = [-180, -90, 180, 90]
        olc_features = generate_grid(resolution)
    else:
        olc_features = generate_grid_within_bbox(resolution, bbox)

    return convert_olcgrid_output_format(olc_features, output_format, output_path, resolution)

def olcgrid_cli():
    parser = argparse.ArgumentParser(description="Generate OLC DGGS.")
    parser.add_argument(
        "-r", "--resolution", type=int, required=True, help="Resolution [2..15]"
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
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of OLC IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    if args.output_format == "None":
        args.output_format = None
    resolution = args.resolution
    bbox = args.bbox if args.bbox else [-180, -90, 180, 90]
    if resolution < 2 or resolution > 15:
        print("Please select a resolution in [2..15] range and try again ")
        return
    olc_features = generate_grid(resolution)
    try:
        result = convert_olcgrid_output_format(olc_features, args.output_format, args.output, resolution)
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
    olcgrid_cli()
