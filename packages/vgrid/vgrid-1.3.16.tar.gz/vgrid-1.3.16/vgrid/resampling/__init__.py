"""
Resampling module for vgrid.

This module provides functions to resample data between different discrete global grid systems (DGGS)
and perform spatial analysis operations.
"""

from .dggsresample import (
    get_nearest_resolution,
    generate_grid,
    resampling,
    main as resampling_main
)

__all__ = [
    'get_nearest_resolution',
    'generate_grid', 
    'resampling',
    'resampling_main'
]
