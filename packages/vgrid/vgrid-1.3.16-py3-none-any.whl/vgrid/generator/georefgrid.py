"""
GEOREF DGGS Grid Generator Module
"""
import json
import argparse
from tqdm import tqdm
from shapely.geometry import Polygon, box
import numpy as np
from vgrid.dggs import georef
from vgrid.generator.settings import MAX_CELLS, graticule_dggs_to_feature
import geopandas as gpd
from shapely.geometry import shape

RESOLUTION_DEGREES = {
    0: 15.0,  # 15° x 15°
    1: 1.0,  # 1° x 1°
    2: 1 / 60,  # 1-minute
    3: 1 / 600,  # 0.1-minute
    4: 1 / 6000,  # 0.01-minute
}

# RESOLUTION_DEGREES = {
#     0: 15.0,       # 15° x 15°
#     1: 1.0,        # 1° x 1°
#     2: 1 / 60,     # 1-minute
#     3: 1 / 600,    # 0.1-minute
#     5: 1 / 6000,   # 0.01-minute
#     5: 1 / 60_000,  # 0.001-minute
#     # 5: 1 / 600_000  # 0.0001-minute
# }


def generate_grid(bbox, resolution):
    lon_min, lat_min, lon_max, lat_max = bbox
    resolution_degrees = RESOLUTION_DEGREES[resolution]
    longitudes = np.arange(lon_min, lon_max, resolution_degrees)
    latitudes = np.arange(lat_min, lat_max, resolution_degrees)
    num_cells = len(longitudes) * len(latitudes)

    print(f"Resolution {resolution} will generate {num_cells} cells ")
    if num_cells > MAX_CELLS:
        print(f"which exceeds the limit of {MAX_CELLS}.")
        print("Please select a smaller resolution and try again.")
        return
    georef_features = []

    with tqdm(total=num_cells, desc="Generating GEOREF DGGS", unit=" cells") as pbar:
        for lon in longitudes:
            for lat in latitudes:
                cell_polygon = Polygon(
                    box(lon, lat, lon + resolution_degrees, lat + resolution_degrees)
                )
                georef_id = georef.encode(lat, lon, resolution)
                georef_feature = graticule_dggs_to_feature(
                    "georef", georef_id, resolution, cell_polygon
                )
                georef_features.append(georef_feature)
                pbar.update(1)

    return {
        "type": "FeatureCollection",
        "features": georef_features,
    }


def convert_georefgrid_output_format(georef_features, output_format=None, output_path=None, resolution=None):
    if not georef_features:
        return []
    def default_path(ext):
        return f"georef_grid_{resolution}.{ext}" if resolution is not None else f"georef_grid.{ext}"
    if output_format is None:
        return [f["properties"]["georef"] for f in georef_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in georef_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(georef_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(georef_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(georef_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(georef_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(georef_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(georef_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def georefgrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate GEOREF grid for pure Python usage.

    Args:
        resolution (int): GEOREF resolution [0..4]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output format ('geojson', 'csv', 'geo', 'gpd', 'shapefile', 'gpkg', 'parquet', or None for list of GEOREF IDs).
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict, list, or str: Output in the requested format or file path.
    """
    if resolution < 0 or resolution > 4:
        raise ValueError("Resolution must be in range [0..4]")
    if bbox is None:
        bbox = [-180, -90, 180, 90]
    georef_features = generate_grid(bbox, resolution)
    return convert_georefgrid_output_format(georef_features, output_format, output_path, resolution)


def georefgrid_cli():
    parser = argparse.ArgumentParser(description="Generate GEOREF DGGS")
    parser.add_argument(
        "-r", "--resolution", type=int, required=True, help="Resolution [0..4]"
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
        help="Output format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of GEOREF IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    if args.output_format == "None":
        args.output_format = None
    try:
        result = georefgrid(args.resolution, args.bbox, args.output_format, args.output)
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
    georefgrid_cli()
