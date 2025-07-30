"""
Settings Module.

This module provides settings for the DGGS Generator Module.
"""

from shapely.geometry import mapping
from shapely.wkt import loads
import platform 
from shapely.geometry import Polygon
from vgrid.utils.antimeridian import fix_polygon
from vgrid.dggs.rhealpixdggs.utils import my_round

if platform.system() == "Windows":
    from vgrid.dggs.eaggr.enums.shape_string_format import ShapeStringFormat
    from vgrid.dggs.eaggr.eaggr import Eaggr
    from vgrid.dggs.eaggr.enums.model import Model
    isea4t_dggs = Eaggr(Model.ISEA4T)
    isea3h_dggs = Eaggr(Model.ISEA3H)

from pyproj import Geod
geod = Geod(ellps="WGS84")


MAX_CELLS = 10_000_000
CHUNK_SIZE = 100_000

isea4t_base_cells = [
    "00",
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
]


isea3h_base_cells = [
    "00000,0",
    "01000,0",
    "02000,0",
    "03000,0",
    "04000,0",
    "05000,0",
    "06000,0",
    "07000,0",
    "08000,0",
    "09000,0",
    "10000,0",
    "11000,0",
    "12000,0",
    "13000,0",
    "14000,0",
    "15000,0",
    "16000,0",
    "17000,0",
    "18000,0",
    "19000,0",
]

def fix_h3_antimeridian_cells(hex_boundary, threshold=-128):
    if any(lon < threshold for _, lon in hex_boundary):
        # Adjust all longitudes accordingly
        return [(lat, lon - 360 if lon > 0 else lon) for lat, lon in hex_boundary]
    return hex_boundary


# Function to filter cells crossing the antimeridian
def fix_rhealpix_antimeridian_cells(boundary, threshold=-128):
    if any(lon < threshold for lon, _ in boundary):
        return [(lon - 360 if lon > 0 else lon, lat) for lon, lat in boundary]
    return boundary

def rhealpix_cell_to_polygon(cell):
    vertices = [
        tuple(my_round(coord, 14) for coord in vertex)
        for vertex in cell.vertices(plane=False)
    ]
    if vertices[0] != vertices[-1]:
        vertices.append(vertices[0])
    vertices = fix_rhealpix_antimeridian_cells(vertices)
    return Polygon(vertices)


def fix_isea4t_wkt(isea4t_wkt):
    # Extract the coordinate section
    coords_section = isea4t_wkt[isea4t_wkt.index("((") + 2 : isea4t_wkt.index("))")]
    coords = coords_section.split(",")
    # Append the first point to the end if not already closed
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    fixed_coords = ", ".join(coords)
    return f"POLYGON (({fixed_coords}))"


def fix_isea4t_antimeridian_cells(isea4t_boundary, threshold=-100):
    """
    Adjusts polygon coordinates to handle antimeridian crossings.
    """
    lon_lat = [(float(lon), float(lat)) for lon, lat in isea4t_boundary.exterior.coords]

    if any(lon < threshold for lon, _ in lon_lat):
        adjusted_coords = [(lon - 360 if lon > 0 else lon, lat) for lon, lat in lon_lat]
    else:
        adjusted_coords = lon_lat

    return Polygon(adjusted_coords)

def isea4t_cell_to_polygon(isea4t_cell):
    cell_to_shp = isea4t_dggs.convert_dggs_cell_outline_to_shape_string(
        isea4t_cell, ShapeStringFormat.WKT
    )
    cell_to_shp_fixed = fix_isea4t_wkt(cell_to_shp)
    cell_polygon = loads(cell_to_shp_fixed)
    return cell_polygon


def isea3h_cell_to_polygon(isea3h_id):
    if platform.system() == "Windows":
        cell_to_shape = isea3h_dggs.convert_dggs_cell_outline_to_shape_string(
            isea3h_id, ShapeStringFormat.WKT
        )
        if cell_to_shape:
            coordinates_part = cell_to_shape.replace("POLYGON ((", "").replace("))", "")
            coordinates = []
            for coord_pair in coordinates_part.split(","):
                lon, lat = map(float, coord_pair.strip().split())
                coordinates.append([lon, lat])

            # Ensure the polygon is closed (first and last point must be the same)
            if coordinates[0] != coordinates[-1]:
                coordinates.append(coordinates[0])

        cell_polygon = Polygon(coordinates)
        fixed_polygon = fix_polygon(cell_polygon)
        return fixed_polygon

def fix_eaggr_wkt(eaggr_wkt):
    # Extract the coordinate section
    coords_section = eaggr_wkt[eaggr_wkt.index("((") + 2 : eaggr_wkt.index("))")]
    coords = coords_section.split(",")
    # Append the first point to the end if not already closed
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    fixed_coords = ", ".join(coords)
    return f"POLYGON (({fixed_coords}))"

def graticule_dggs_metrics(cell_polygon):
    min_lon, min_lat, max_lon, max_lat = cell_polygon.bounds
    center_lat = round((min_lat + max_lat) / 2, 7)
    center_lon = round((min_lon + max_lon) / 2, 7)
    cell_width = round(geod.line_length([min_lon, max_lon], [min_lat, min_lat]), 3)
    cell_height = round(geod.line_length([min_lon, min_lon], [min_lat, max_lat]), 3)
    cell_area = round(
        abs(geod.geometry_area_perimeter(cell_polygon)[0]), 3
    )  # Area in square meters
    return center_lat, center_lon, cell_width, cell_height, cell_area


def geodesic_dggs_metrics(cell_polygon, num_edges):
    cell_centroid = cell_polygon.centroid
    center_lat = round(cell_centroid.y, 7)
    center_lon = round(cell_centroid.x, 7)
    cell_area = round(
        abs(geod.geometry_area_perimeter(cell_polygon)[0]), 3
    )  # Area in square meters
    cell_perimeter = abs(geod.geometry_area_perimeter(cell_polygon)[1])
    avg_edge_len = round(cell_perimeter / num_edges, 3)
    return center_lat, center_lon, avg_edge_len, cell_area


# Convert Graticule DGGS cell to GeoJSON feature
def graticule_dggs_to_feature(dggs_name, cell_id, resolution, cell_polygon):
    center_lat, center_lon, cell_width, cell_height, cell_area = graticule_dggs_metrics(
        cell_polygon
    )
    feature = {
        "type": "Feature",
        "geometry": mapping(cell_polygon),
        "properties": {
            f"{dggs_name}": str(cell_id),
            "resolution": resolution,
            "center_lat": center_lat,
            "center_lon": center_lon,
            "cell_width": cell_width,
            "cell_height": cell_height,
            "cell_area": cell_area,
        },
    }
    return feature

# Convert Geodesic DGGS cell to GeoJSON feature
def geodesic_dggs_to_feature(dggs_name, cell_id, resolution, cell_polygon, num_edges):
    center_lat, center_lon, avg_edge_len, cell_area = geodesic_dggs_metrics(
        cell_polygon, num_edges
    )
    feature = {
        "type": "Feature",
        "geometry": mapping(cell_polygon),
        "properties": {
            f"{dggs_name}": str(cell_id),
            "resolution": resolution,
            "center_lat": center_lat,
            "center_lon": center_lon,
            "avg_edge_len": avg_edge_len,
            "cell_area": cell_area,
        },
    }
    return feature


mgrs_gzd_lon_dict = {
    "01": 1,
    "02": 2,
}

mgrs_gzd_lat_dict = {"C": 1, "D": 2, "E": 3, "F": 4, "G": 5, "H": 6}


isea4t_res_accuracy_dict = {
    0: 25_503_281_086_204.43,
    1: 6_375_820_271_551.114,
    2: 1_593_955_067_887.7715,
    3: 398_488_766_971.94995,
    4: 99_622_191_742.98041,
    5: 24905_547_935.752182,
    6: 6_226_386_983.930966,
    7: 1_556_596_745.9898202,
    8: 389_149_186.4903765,
    9: 97_287_296.6296727,
    10: 24_321_824.150339592,
    11: 6_080_456.0446634805,
    12: 1_520_114.0040872877,
    13: 380_028.5081004044,
    14: 95_007.11994651864,
    15: 23_751.787065212124,
    16: 5_937.9396877205645,
    17: 1_484.492000512607,
    18: 371.1159215456855,
    19: 92.78605896888773,
    20: 23.189436159755584,
    21: 5.804437622405244,
    22: 1.4440308231349632,
    23: 0.36808628825008866,
    24: 0.0849429895961743,
    25: 0.028314329865391435,
    26: 7.08 * 10**-3,  # accuracy returns 0.0, avg_edge_len =  0.11562
    27: 1.77 * 10**-3,  # accuracy returns 0.0, avg_edge_len =  0.05781
    28: 4.42 * 10**-4,  # accuracy returns 0.0, avg_edge_len =  0.0289
    29: 1.11 * 10**-4,  # accuracy returns 0.0, avg_edge_len =  0.01445
    30: 2.77 * 10**-5,  # accuracy returns 0.0, avg_edge_len = 0.00723
    31: 6.91 * 10**-6,  # accuracy returns 0.0, avg_edge_len =  0.00361
    32: 1.73 * 10**-6,  # accuracy returns 0.0, avg_edge_len =  0.00181
    33: 5.76 * 10**-7,  # accuracy returns 0.0, avg_edge_len = 0.0009
    34: 1.92 * 10**-7,  # accuracy returns 0.0, avg_edge_len = 0.00045
    35: 6.40 * 10**-8,  # accuracy returns 0.0, avg_edge_len = 0.00023
    36: 2.13 * 10**-8,  # accuracy returns 0, avg_edge_len = 0.00011
    37: 7.11 * 10**-9,  # accuracy returns 0.0, avg_edge_len = 6*10**(-5)
    38: 2.37 * 10**-9,  # accuracy returns 0.0, avg_edge_len = 3*10**(-5)
    39: 7.90 * 10**-10,  # accuracy returns 0.0, avg_edge_len = 10**(-5)
}

isea3h_res_accuracy_dict = {
    0: 25_503_281_086_204.43,
    1: 17_002_187_390_802.953,
    2: 5_667_395_796_934.327,
    3: 1_889_131_932_311.4424,
    4: 629_710_644_103.8047,
    5: 209_903_548_034.5921,
    6: 69_967_849_344.8546,
    7: 23_322_616_448.284866,
    8: 7_774_205_482.77106,
    9: 2_591_401_827.5809155,
    10: 863_800_609.1842003,
    11: 287_933_536.4041716,
    12: 95_977_845.45861907,
    13: 31_992_615.152873024,
    14: 10_664_205.060395785,
    15: 3_554_735.0295700384,
    16: 1_184_911.6670852362,
    17: 394_970.54625696875,
    18: 131_656.84875232293,
    19: 43_885.62568888426,
    20: 14628.541896294753,
    21: 4_876.180632098251,
    22: 1_625.3841059227952,
    23: 541.7947019742651,
    24: 180.58879588146658,
    25: 60.196265293822194,
    26: 20.074859874562527,
    27: 6.6821818482323785,
    28: 2.2368320593659234,
    29: 0.7361725765001773,
    30: 0.2548289687885229,
    31: 0.0849429895961743,
    32: 0.028314329865391435,
    33: 0.009438109955130478,
    34: 0.0031460366517101594,
    35: 0.0010486788839033865,
    36: 0.0003495596279677955,
    37: 0.0001165198769892652,
    38: 0.0000388399589964217,
    39: 0.0000129466529988072,
    40: 0.0000043155509996024,
}

isea3h_accuracy_res_dict = {
    25_503_281_086_204.43: 0,
    17_002_187_390_802.953: 1,
    5_667_395_796_934.327: 2,
    1_889_131_932_311.4424: 3,
    629_710_644_103.8047: 4,
    209_903_548_034.5921: 5,
    69_967_849_344.8546: 6,
    23_322_616_448.284866: 7,
    7_774_205_482.77106: 8,
    2_591_401_827.5809155: 9,
    863_800_609.1842003: 10,
    287_933_536.4041716: 11,
    95_977_845.45861907: 12,
    31_992_615.152873024: 13,
    10_664_205.060395785: 14,
    3_554_735.0295700384: 15,
    1_184_911.6670852362: 16,
    394_970.54625696875: 17,
    131_656.84875232293: 18,
    43_885.62568888426: 19,
    14628.541896294753: 20,
    4_876.180632098251: 21,
    1_625.3841059227952: 22,
    541.7947019742651: 23,
    180.58879588146658: 24,
    60.196265293822194: 25,
    20.074859874562527: 26,
    6.6821818482323785: 27,
    2.2368320593659234: 28,
    0.7361725765001773: 29,
    0.2548289687885229: 30,
    0.0849429895961743: 31,
    0.028314329865391435: 32,
    0.0: 33,  # isea3h2point._accuracy always returns 0.0 from res 33
    0.0: 34,
    0.0: 35,
    0.0: 36,
    0.0: 37,
    0.0: 38,
    0.0: 39,
    0.0: 40,
}
