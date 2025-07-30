"""
Image Tiler - A Python library for extracting tiles from images with support
for overlapping tiles and paired image processing for AI model training.
"""

from .data_structures import Tile, TilePair, TilingResult
from .tiler import ImageTiler

__version__ = "0.1.0"
__all__ = ["ImageTiler", "Tile", "TilePair", "TilingResult"]
