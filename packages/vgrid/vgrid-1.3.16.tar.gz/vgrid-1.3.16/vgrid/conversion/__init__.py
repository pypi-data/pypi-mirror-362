"""
Conversion module for vgrid.

This module provides functions to convert between different coordinate systems,
geographic data formats, and discrete global grid systems (DGGS).
"""

# CSV to DGGS conversions
from .csv2dggs import (
    csv2h3, csv2s2, csv2rhealpix, csv2isea4t, csv2isea3h, csv2ease,
    csv2qtm, csv2olc, csv2geohash, csv2georef, csv2mgrs, csv2tilecode,
    csv2quadkey, csv2maidenhead, csv2gars,
    # Individual cell to feature conversions
    h32feature, s22feature, rhealpix2feature, isea4t2feature, isea3h2feature,
    ease2feature, qtm2feature, olc2feature, geohash2feature, georef2feature,
    mgrs2feature, tilecode2feature, quadkey2feature, maidenhead2feature, gars2feature
)

# Latitude/Longitude to DGGS conversions
from .latlon2dggs import (
    latlon2h3, latlon2s2, latlon2rhealpix, latlon2isea4t, latlon2isea3h,
    latlon2dggrid, latlon2ease, latlon2qtm, latlon2olc, latlon2geohash,
    latlon2georef, latlon2mgrs, latlon2tilecode, latlon2quadkey,
    latlon2maidenhead, latlon2gars
)

# DGGS to GeoJSON conversions
from .dggs2geo.h32geo import h32geo, h32geojson
from .dggs2geo.s22geo import s22geo, s22geojson
from .dggs2geo.rhealpix2geo import rhealpix2geo, rhealpix2geojson
from .dggs2geo.isea4t2geo import isea4t2geo, isea4t2geojson
from .dggs2geo.isea3h2geo import isea3h2geo, isea3h2geojson
from .dggs2geo.dggrid2geo import dggrid2geojson
from .dggs2geo.ease2geo import ease2geo, ease2geojson
from .dggs2geo.qtm2geo import qtm2geo, qtm2geojson
from .dggs2geo.olc2geo import olc2geo, olc2geojson
from .dggs2geo.geohash2geo import geohash2geo, geohash2geojson
from .dggs2geo.georef2geo import georef2geo, georef2geojson
from .dggs2geo.mgrs2geo import mgrs2geo, mgrs2geojson
from .dggs2geo.maidenhead2geo import maidenhead2geo, maidenhead2geojson
from .dggs2geo.gars2geo import gars2geo, gars2geojson

# GeoJSON to CSV conversion
from .geojson2csv import geojson2csv

# DGGS compaction
from .dggscompact import h3compact, s2compact, rhealpixcompact, isea4tcompact, isea3hcompact, easecompact, qtmcompact, olccompact, geohashcompact, tilecodecompact, quadkeycompact

# Vector to DGGS conversions
from .vector2dggs.vector2h3 import vector2h3
from .vector2dggs.vector2s2 import vector2s2
from .vector2dggs.vector2rhealpix import vector2rhealpix
from .vector2dggs.vector2isea4t import vector2isea4t
from .vector2dggs.vector2isea3h import vector2isea3h
from .vector2dggs.vector2ease import vector2ease
from .vector2dggs.vector2qtm import vector2qtm
from .vector2dggs.vector2olc import vector2olc
from .vector2dggs.vector2geohash import vector2geohash
from .vector2dggs.vector2mgrs import vector2mgrs
from .vector2dggs.vector2tilecode import vector2tilecode
from .vector2dggs.vector2quadkey import vector2quadkey

# Raster to DGGS conversions
from .raster2dggs.raster2h3 import raster2h3
from .raster2dggs.raster2s2 import raster2s2
from .raster2dggs.raster2rhealpix import raster2rhealpix
from .raster2dggs.raster2isea4t import raster2isea4t
from .raster2dggs.raster2qtm import raster2qtm
from .raster2dggs.raster2olc import raster2olc
from .raster2dggs.raster2geohash import raster2geohash
from .raster2dggs.raster2tilecode import raster2tilecode
from .raster2dggs.raster2quadkey import raster2quadkey

__all__ = [
    # CSV to DGGS
    'csv2h3', 'csv2s2', 'csv2rhealpix', 'csv2isea4t', 'csv2isea3h', 'csv2ease',
    'csv2qtm', 'csv2olc', 'csv2geohash', 'csv2georef', 'csv2mgrs', 'csv2tilecode',
    'csv2quadkey', 'csv2maidenhead', 'csv2gars',
    # Cell to feature
    'h32feature', 's22feature', 'rhealpix2feature', 'isea4t2feature', 'isea3h2feature',
    'ease2feature', 'qtm2feature', 'olc2feature', 'geohash2feature', 'georef2feature',
    'mgrs2feature', 'tilecode2feature', 'quadkey2feature', 'maidenhead2feature', 'gars2feature',
    # LatLon to DGGS
    'latlon2h3', 'latlon2s2', 'latlon2rhealpix', 'latlon2isea4t', 'latlon2isea3h',
    'latlon2dggrid', 'latlon2ease', 'latlon2qtm', 'latlon2olc', 'latlon2geohash',
    'latlon2georef', 'latlon2mgrs', 'latlon2tilecode', 'latlon2quadkey',
    'latlon2maidenhead', 'latlon2gars',
    # DGGS to GeoJSON
    'h32geojson',
    # GeoJSON to CSV
    'geojson2csv',
    # DGGS compaction
    'h3compact', 's2compact', 'rhealpixcompact', 'isea4tcompact', 'isea3hcompact', 'easecompact', 'qtmcompact', 'olccompact', 'geohashcompact', 'mgrscompact', 'tilecodecompact', 'quadkeycompact', 'maidenheadcompact', 'garscompact',
    # Vector to DGGS
    'vector2h3', 'vector2s2', 'vector2rhealpix', 'vector2isea4t', 'vector2isea3h',
    'vector2ease', 'vector2qtm', 'vector2olc', 'vector2geohash',
    'vector2mgrs', 'vector2tilecode', 'vector2quadkey',
    # Raster to DGGS
    'raster2h3', 'raster2s2', 'raster2rhealpix', 'raster2isea4t', 'raster2qtm',
    'raster2olc', 'raster2geohash', 'raster2tilecode', 'raster2quadkey'
]
