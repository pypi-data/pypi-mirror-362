"""
Generator module for vgrid.

This module provides functions to generate discrete global grid systems (DGGS)
for various coordinate systems and geographic areas.
"""

import platform

# Main grid generation functions
from .h3grid import h3grid, generate_grid as h3_generate_grid, generate_grid_within_bbox as h3_generate_grid_within_bbox, generate_grid_resample as h3_generate_grid_resample
from .s2grid import s2grid, generate_grid as s2_generate_grid, generate_grid_resample as s2_generate_grid_resample, s2_cell_to_polygon
from .rhealpixgrid import rhealpixgrid, generate_grid as rhealpix_generate_grid, generate_grid_within_bbox as rhealpix_generate_grid_within_bbox, generate_grid_resample as rhealpix_generate_grid_resample
# if platform.system() == "Windows":
#     from .isea4tgrid import generate_grid as isea4t_generate_grid, generate_grid_within_bbox as isea4t_generate_grid_within_bbox, generate_grid_resample as isea4t_generate_grid_resample
#     from .isea3hgrid import generate_grid as isea3h_generate_grid, generate_grid_within_bbox as isea3h_generate_grid_within_bbox

from .easegrid import easegrid, generate_grid as ease_generate_grid, generate_grid_within_bbox as ease_generate_grid_within_bbox
from .qtmgrid import qtmgrid, generate_grid as qtm_generate_grid, generate_grid_within_bbox as qtm_generate_grid_within_bbox
from .olcgrid import olcgrid, generate_grid as olc_generate_grid, generate_grid_within_bbox as olc_generate_grid_within_bbox
from .geohashgrid import geohashgrid, generate_grid as geohash_generate_grid, generate_grid_within_bbox as geohash_generate_grid_within_bbox
from .georefgrid import georefgrid, generate_grid as georef_generate_grid
from .mgrsgrid import mgrsgrid, generate_grid as mgrs_generate_grid
from .tilecodegrid import tilecodegrid, generate_grid as tilecode_generate_grid
from .quadkeygrid import quadkeygrid, generate_grid as quadkey_generate_grid
from .maidenheadgrid import maidenheadgrid, generate_grid as maidenhead_generate_grid, generate_grid_within_bbox as maidenhead_generate_grid_within_bbox
from .garsgrid import garsgrid, generate_grid as gars_generate_grid, generate_grid_within_bbox as gars_generate_grid_within_bbox

__all__ = [
    # Main grid functions
    'h3grid', 's2grid', 'rhealpixgrid', 'isea4tgrid', 'isea3hgrid',
    'easegrid', 'qtmgrid', 'olcgrid', 'geohashgrid', 'georefgrid', 'mgrsgrid',
    'tilecodegrid', 'quadkeygrid', 'maidenheadgrid', 'garsgrid',
    # Grid generation with specific parameters
    'h3_generate_grid', 'h3_generate_grid_within_bbox', 'h3_generate_grid_resample',
    's2_generate_grid', 's2_generate_grid_resample', 's2_cell_to_polygon',
    'rhealpix_generate_grid', 'rhealpix_generate_grid_within_bbox', 'rhealpix_generate_grid_resample',
    # 'isea4t_generate_grid', 'isea4t_generate_grid_within_bbox', 'isea4t_generate_grid_resample',
    # 'isea3h_generate_grid', 'isea3h_generate_grid_within_bbox', 
    'ease_generate_grid', 'ease_generate_grid_within_bbox',
    'qtm_generate_grid', 'qtm_generate_grid_within_bbox',
    'olc_generate_grid', 'olc_generate_grid_within_bbox', 
    'geohash_generate_grid', 'geohash_generate_grid_within_bbox',
    'georef_generate_grid',  
    'mgrs_generate_grid',  
    'tilecode_generate_grid',
    'quadkey_generate_grid', 
    'maidenhead_generate_grid', 'maidenhead_generate_grid_within_bbox',
    'gars_generate_grid', 'gars_generate_grid_within_bbox',   
]
