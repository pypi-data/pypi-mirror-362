from shapely.geometry import shape, Polygon
import argparse
import json
from vgrid.dggs import qtm
from vgrid.generator.settings import geodesic_dggs_to_feature
from shapely.ops import unary_union
from tqdm import tqdm
from vgrid.generator.settings import MAX_CELLS

p90_n180, p90_n90, p90_p0, p90_p90, p90_p180 = (
    (90.0, -180.0),
    (90.0, -90.0),
    (90.0, 0.0),
    (90.0, 90.0),
    (90.0, 180.0),
)
p0_n180, p0_n90, p0_p0, p0_p90, p0_p180 = (
    (0.0, -180.0),
    (0.0, -90.0),
    (0.0, 0.0),
    (0.0, 90.0),
    (0.0, 180.0),
)
n90_n180, n90_n90, n90_p0, n90_p90, n90_p180 = (
    (-90.0, -180.0),
    (-90.0, -90.0),
    (-90.0, 0.0),
    (-90.0, 90.0),
    (-90.0, 180.0),
)


def generate_grid(resolution):
    levelFacets = {}
    QTMID = {}

    for lvl in tqdm(range(resolution), desc="Generating QTM DGGS"):
        levelFacets[lvl] = []
        QTMID[lvl] = []
        qtm_features = []  # Store GeoJSON features separately

        if lvl == 0:
            initial_facets = [
                [p0_n180, p0_n90, p90_n90, p90_n180, p0_n180, True],
                [p0_n90, p0_p0, p90_p0, p90_n90, p0_n90, True],
                [p0_p0, p0_p90, p90_p90, p90_p0, p0_p0, True],
                [p0_p90, p0_p180, p90_p180, p90_p90, p0_p90, True],
                [n90_n180, n90_n90, p0_n90, p0_n180, n90_n180, False],
                [n90_n90, n90_p0, p0_p0, p0_n90, n90_n90, False],
                [n90_p0, n90_p90, p0_p90, p0_p0, n90_p0, False],
                [n90_p90, n90_p180, p0_p180, p0_p90, n90_p90, False],
            ]

            for i, facet in enumerate(initial_facets):
                facet_geom = qtm.constructGeometry(facet)
                QTMID[0].append(str(i + 1))
                levelFacets[0].append(facet)
                qtm_id = QTMID[0][i]
                num_edges = 3
                qtm_feature = geodesic_dggs_to_feature(
                    "qtm", qtm_id, resolution, facet_geom, num_edges
                )
                qtm_features.append(qtm_feature)

        else:
            for i, pf in enumerate(levelFacets[lvl - 1]):
                subdivided_facets = qtm.divideFacet(pf)
                for j, subfacet in enumerate(subdivided_facets):
                    new_id = QTMID[lvl - 1][i] + str(j)
                    QTMID[lvl].append(new_id)
                    levelFacets[lvl].append(subfacet)
                    if lvl == resolution - 1:
                        subfacet_geom = qtm.constructGeometry(subfacet)
                        qtm_id = new_id
                        num_edges = 3
                        qtm_feature = geodesic_dggs_to_feature(
                            "qtm", qtm_id, resolution, subfacet_geom, num_edges
                        )
                        qtm_features.append(qtm_feature)
    return {"type": "FeatureCollection", "features": qtm_features}


def generate_grid_within_bbox(resolution, bbox):
    """Generates a Dutton QTM grid at a specific resolution within a bounding box and saves it as GeoJSON."""
    levelFacets = {}
    QTMID = {}
    qtm_features = []

    # Convert bbox to Polygon
    bbox_poly = Polygon(
        [
            (bbox[0], bbox[1]),  # min_lon, min_lat
            (bbox[2], bbox[1]),  # max_lon, min_lat
            (bbox[2], bbox[3]),  # max_lon, max_lat
            (bbox[0], bbox[3]),  # min_lon, max_lat
            (bbox[0], bbox[1]),  # Close the polygon
        ]
    )

    for lvl in tqdm(range(resolution), desc="Generating QTM DGGS"):
        levelFacets[lvl] = []
        QTMID[lvl] = []

        if lvl == 0:
            initial_facets = [
                [p0_n180, p0_n90, p90_n90, p90_n180, p0_n180, True],
                [p0_n90, p0_p0, p90_p0, p90_n90, p0_n90, True],
                [p0_p0, p0_p90, p90_p90, p90_p0, p0_p0, True],
                [p0_p90, p0_p180, p90_p180, p90_p90, p0_p90, True],
                [n90_n180, n90_n90, p0_n90, p0_n180, n90_n180, False],
                [n90_n90, n90_p0, p0_p0, p0_n90, n90_n90, False],
                [n90_p0, n90_p90, p0_p90, p0_p0, n90_p0, False],
                [n90_p90, n90_p180, p0_p180, p0_p90, n90_p90, False],
            ]

            for i, facet in enumerate(initial_facets):
                QTMID[0].append(str(i + 1))
                facet_geom = qtm.constructGeometry(facet)
                levelFacets[0].append(facet)
                if shape(facet_geom).intersects(bbox_poly) and resolution == 1:
                    qtm_id = QTMID[0][i]
                    num_edges = 3
                    qtm_feature = geodesic_dggs_to_feature(
                        "qtm", qtm_id, resolution, facet_geom, num_edges
                    )
                    qtm_features.append(qtm_feature)
        else:
            for i, pf in enumerate(levelFacets[lvl - 1]):
                subdivided_facets = qtm.divideFacet(pf)
                for j, subfacet in enumerate(subdivided_facets):
                    subfacet_geom = qtm.constructGeometry(subfacet)
                    if shape(subfacet_geom).intersects(
                        bbox_poly
                    ):  # Only keep intersecting facets
                        new_id = QTMID[lvl - 1][i] + str(j)
                        QTMID[lvl].append(new_id)
                        levelFacets[lvl].append(subfacet)
                        if (
                            lvl == resolution - 1
                        ):  # Only store final resolution in GeoJSON
                            qtm_id = new_id
                            num_edges = 3
                            qtm_feature = geodesic_dggs_to_feature(
                                "qtm", qtm_id, resolution, subfacet_geom, num_edges
                            )
                            qtm_features.append(qtm_feature)
    return {"type": "FeatureCollection", "features": qtm_features}


def generate_grid_resample(resolution, geojson_features):
    """Generates a Dutton QTM grid at a specific resolution within geojson_features and returns it as GeoJSON."""
    levelFacets = {}
    QTMID = {}
    qtm_features = []

    # Step 1: Union all input GeoJSON geometries
    geometries = [
        shape(feature["geometry"]) for feature in geojson_features["features"]
    ]
    unified_geom = unary_union(geometries)

    for lvl in tqdm(range(resolution), desc="Generating QTM DGGS"):
        levelFacets[lvl] = []
        QTMID[lvl] = []

        if lvl == 0:
            initial_facets = [
                [p0_n180, p0_n90, p90_n90, p90_n180, p0_n180, True],
                [p0_n90, p0_p0, p90_p0, p90_n90, p0_n90, True],
                [p0_p0, p0_p90, p90_p90, p90_p0, p0_p0, True],
                [p0_p90, p0_p180, p90_p180, p90_p90, p0_p90, True],
                [n90_n180, n90_n90, p0_n90, p0_n180, n90_n180, False],
                [n90_n90, n90_p0, p0_p0, p0_n90, n90_n90, False],
                [n90_p0, n90_p90, p0_p90, p0_p0, n90_p0, False],
                [n90_p90, n90_p180, p0_p180, p0_p90, n90_p90, False],
            ]

            for i, facet in enumerate(initial_facets):
                QTMID[0].append(str(i + 1))
                facet_geom = qtm.constructGeometry(facet)
                levelFacets[0].append(facet)

                if shape(facet_geom).intersects(unified_geom) and resolution == 1:
                    qtm_id = QTMID[0][i]
                    num_edges = 3
                    qtm_feature = geodesic_dggs_to_feature(
                        "qtm", qtm_id, resolution, facet_geom, num_edges
                    )
                    qtm_features.append(qtm_feature)

        else:
            for i, pf in enumerate(levelFacets[lvl - 1]):
                subdivided_facets = qtm.divideFacet(pf)
                for j, subfacet in enumerate(subdivided_facets):
                    subfacet_geom = qtm.constructGeometry(subfacet)
                    if shape(subfacet_geom).intersects(unified_geom):
                        new_id = QTMID[lvl - 1][i] + str(j)
                        QTMID[lvl].append(new_id)
                        levelFacets[lvl].append(subfacet)

                        if lvl == resolution - 1:
                            qtm_id = new_id
                            num_edges = 3
                            qtm_feature = geodesic_dggs_to_feature(
                                "qtm", qtm_id, resolution, subfacet_geom, num_edges
                            )
                            qtm_features.append(qtm_feature)

    return {"type": "FeatureCollection", "features": qtm_features}


def convert_qtmgrid_output_format(qtm_features, output_format=None, output_path=None, resolution=None):
    if not qtm_features:
        return []
    def default_path(ext):
        return f"qtm_grid_{resolution}.{ext}" if resolution is not None else f"qtm_grid.{ext}"
    import geopandas as gpd
    import pandas as pd
    from shapely.geometry import shape
    if output_format is None:
        return [f["properties"]["qtm"] for f in qtm_features["features"]]
    elif output_format == "geo":
        return [shape(f["geometry"]) for f in qtm_features["features"]]
    elif output_format == "gpd":
        gdf = gpd.GeoDataFrame.from_features(qtm_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        return gdf
    elif output_format == "csv":
        gdf = gpd.GeoDataFrame.from_features(qtm_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("csv")
        gdf.to_csv(output_path, index=False)
        return output_path
    elif output_format == "geojson":
        if output_path is None:
            output_path = default_path("geojson")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(qtm_features, f)
        return output_path
    elif output_format == "shapefile":
        gdf = gpd.GeoDataFrame.from_features(qtm_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("shp")
        gdf.to_file(output_path, driver="ESRI Shapefile")
        return output_path
    elif output_format == "gpkg":
        gdf = gpd.GeoDataFrame.from_features(qtm_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("gpkg")
        gdf.to_file(output_path, driver="GPKG")
        return output_path
    elif output_format == "parquet":
        gdf = gpd.GeoDataFrame.from_features(qtm_features["features"])
        gdf.set_crs(epsg=4326, inplace=True)
        if output_path is None:
            output_path = default_path("parquet")
        gdf.to_parquet(output_path, index=False)
        return output_path
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")


def qtmgrid(resolution, bbox=None, output_format=None, output_path=None):
    """
    Generate QTM grid for pure Python usage.

    Args:
        resolution (int): QTM resolution [1..24]
        bbox (list, optional): Bounding box [min_lon, min_lat, max_lon, max_lat]. Defaults to None (whole world).
        output_format (str, optional): Output format ('geojson', 'csv', etc.). Defaults to None (list of QTM IDs).
        output_path (str, optional): Output file path. Defaults to None.

    Returns:
        dict or list: GeoJSON FeatureCollection, list of QTM IDs, or file path depending on output_format
    """
    if resolution < 1 or resolution > 24:
        raise ValueError("Resolution must be in range [1..24]")

    if bbox is None:
        bbox = [-180, -90, 180, 90]
        # Estimate number of cells by generating the grid and counting features
        qtm_features = generate_grid(resolution)
        num_cells = len(qtm_features["features"])
        if num_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution {resolution} will generate {num_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
        return convert_qtmgrid_output_format(qtm_features, output_format, output_path, resolution)
    else:
        qtm_features = generate_grid_within_bbox(resolution, bbox)
        num_cells = len(qtm_features["features"])
        if num_cells > MAX_CELLS:
            raise ValueError(
                f"Resolution {resolution} within bbox {bbox} will generate {num_cells} cells which exceeds the limit of {MAX_CELLS}"
            )
        return convert_qtmgrid_output_format(qtm_features, output_format, output_path, resolution)

def qtmgrid_cli():
    parser = argparse.ArgumentParser(description="Generate QTM DGGS.")
    parser.add_argument(
        "-r", "--resolution", required=True, type=int, help="Resolution [1..24]."
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
        help="Output output_format (geojson, csv, geo, gpd, shapefile, gpkg, parquet, or None for list of QTM IDs)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (optional)", default=None
    )
    args = parser.parse_args()
    if args.output_format == "None":
        args.output_format = None
    resolution = args.resolution
    bbox = args.bbox if args.bbox else [-180, -90, 180, 90]
    if resolution < 1 or resolution > 24:
        print("Please select a resolution in [1..24] range and try again ")
        return
    if bbox == [-180, -90, 180, 90]:
        qtm_features = generate_grid(resolution)
    else:
        qtm_features = generate_grid_within_bbox(resolution, bbox)
    try:
        result = convert_qtmgrid_output_format(qtm_features, args.output_format, args.output, resolution)
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
    qtmgrid_cli()
