"""
Data structures for the image tiler library.
"""

import os
from dataclasses import dataclass
from typing import List, Union

import numpy as np


@dataclass
class Tile:
    """
    Represents a single tile extracted from an image.

    Attributes:
        image_data: The actual tile image data as a numpy array
        source_path: Path to the source image file
        x: X coordinate of the tile in the source image
        y: Y coordinate of the tile in the source image
        width: Width of the tile in pixels
        height: Height of the tile in pixels
        tile_index: Sequential tile number within the source image
    """

    image_data: np.ndarray
    source_path: Union[str, os.PathLike]
    x: int
    y: int
    width: int
    height: int
    tile_index: int


@dataclass
class TilePair:
    """
    Represents a pair of tiles (input and output) for AI model training.

    Attributes:
        input_tile: The input tile
        output_tile: The corresponding output tile
        is_identical: Whether the tiles are identical
    """

    input_tile: Tile
    output_tile: Tile
    is_identical: bool


@dataclass
class TilingResult:
    """
    Results from processing a folder of images.

    Attributes:
        tiles: List of tiles when no translation function is used
        tile_pairs: List of tile pairs when translation function is provided
        processed_images: List of successfully processed image paths
        skipped_images: List of images that couldn't be processed
        total_tiles: Total number of tiles generated
        filtered_pairs: Number of filtered identical pairs (when applicable)
    """

    tiles: List[Tile]
    tile_pairs: List[TilePair]
    processed_images: List[Union[str, os.PathLike]]
    skipped_images: List[Union[str, os.PathLike]]
    total_tiles: int
    filtered_pairs: int

    def __post_init__(self) -> None:
        """Validate that either tiles or tile_pairs is populated, but not both."""
        if self.tiles and self.tile_pairs:
            raise ValueError("TilingResult cannot have both tiles and tile_pairs")
