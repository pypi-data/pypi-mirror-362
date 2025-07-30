"""
This module provides functions for generating statistics for ISEA3H DGGS cells.
"""
import locale
import argparse
import csv
from shapely.wkt import loads
from vgrid.conversion.latlon2dggs import latlon2isea3h
from vgrid.generator.settings import fix_eaggr_wkt
from texttable import Texttable
import platform
from pyproj import Geod
geod = Geod(ellps="WGS84")

locale.setlocale(locale.LC_ALL, "")

if platform.system() == "Windows":
    from vgrid.dggs.eaggr.enums.shape_string_format import ShapeStringFormat
    from vgrid.dggs.eaggr.eaggr import Eaggr
    from vgrid.dggs.eaggr.shapes.dggs_cell import DggsCell
    from vgrid.dggs.eaggr.enums.model import Model
    isea3h_dggs = Eaggr(Model.ISEA3H)


def isea3h_metrics(res):
    """
    Calculate metrics for ISEA3H DGGS cells.
    """
    num_cells = 20 * (7**res)
    lat, lon = 10.775275567242561, 106.70679737574993

    isea3h_cell = DggsCell(latlon2isea3h(lat, lon, res))

    cell_to_shp = isea3h_dggs.convert_dggs_cell_outline_to_shape_string(
        isea3h_cell, ShapeStringFormat.WKT
    )
    cell_to_shp_fixed = fix_eaggr_wkt(cell_to_shp)
    cell_polygon = loads(cell_to_shp_fixed)

    # isea3h2point = isea3h_dggs.convert_dggs_cell_to_point(isea3h_cell)
    # accuracy = isea3h2point.get_accuracy()

    avg_area = abs(
        geod.geometry_area_perimeter(cell_polygon)[0]
    )  # Area in square meters
    avg_edge_length = (
        abs(geod.geometry_area_perimeter(cell_polygon)[1]) / 6
    )  # Perimeter in meters/ 6
    if res == 0:
        avg_edge_length = (
            abs(geod.geometry_area_perimeter(cell_polygon)[1]) / 3
        )  # icosahedron faces

    return num_cells, avg_edge_length, avg_area


def isea3hstats(output_file=None):
    """
    Generate statistics for ISEA3H DGGS cells.
    """
    min_res = 0
    max_res = 40
    t = Texttable()
    # Add header to the table, including the new 'Cell Width' and 'Cell Area' columns
    t.add_row(
        [
            "Resolution",
            "Number of Cells",
            "Avg Edge Length (m)",
            "Avg Cell Area (sq m)",
            # "Accucracy",
        ]
    )

    # Check if an output file is specified (for CSV export)
    if output_file:
        # Open the output CSV file for writing
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Resolution",
                    "Number of Cells",
                    "Avg Edge Length (m)",
                    "Avg Cell Area (sq m)",
                    # "Accucracy",
                ]
            )

            for res in range(min_res, max_res + 1):
                num_cells, avg_edge_length, avg_area = isea3h_metrics(res)
                writer.writerow([res, num_cells, avg_edge_length, avg_area])
        print(f"OpenEAGGGR ISEA3H stats saved to {output_file}.")
    else:
        for res in range(min_res, max_res + 1):
            num_cells, avg_edge_length, avg_area = isea3h_metrics(res)
            formatted_num_cells = locale.format_string("%d", num_cells, grouping=True)
            formatted_edge_length = locale.format_string(
                "%.3f", avg_edge_length, grouping=True
            )
            formatted_area = locale.format_string("%.3f", avg_area, grouping=True)
            # formatted_accuracy = locale.format_string("%.3f", accuracy, grouping=True)
            # Add a row to the table
            t.add_row(
                [
                    res,
                    formatted_num_cells,
                    formatted_edge_length,
                    formatted_area,
                    #formatted_accuracy,
                ]
            )

        # Print the formatted table to the console
        print(t.draw())


def isea3hstats_cli():
    """
    Command-line interface for generating ISEA3H DGGS statistics.
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Export or display OpenEAGGR ISEA3H DGGS stats."
    )
    parser.add_argument("-o", "--output", help="Output CSV file name.")
    args = parser.parse_args()
    if platform.system() == "Windows":
        # Call the function with the provided output file (if any)
        isea3hstats(args.output)


if __name__ == "__main__":
    isea3hstats_cli()
