"""
Main ImageTiler class for extracting tiles from images.
"""

import os
import warnings
from pathlib import Path
from typing import Callable, List, Optional, Union

from .data_structures import Tile, TilePair, TilingResult
from .utils import (
    arrays_equal,
    calculate_tile_positions,
    extract_tile,
    get_image_files,
    load_image,
)


class ImageTiler:
    """
    Main class for extracting tiles from images with support for overlapping tiles
    and paired image processing for AI model training.
    """

    def __init__(
        self,
        tile_width: int,
        tile_height: int,
        overlap: float = 0.0,
        translate_path: Optional[
            Callable[[Union[str, os.PathLike]], Union[str, os.PathLike]]
        ] = None,
        filter_identical: bool = False,
    ):
        """
        Initialize the image tiler.

        Args:
            tile_width: Width of each tile in pixels
            tile_height: Height of each tile in pixels
            overlap: Overlap as fraction of tile size (0.0-1.0)
            translate_path: Optional callable that maps input paths to output paths.
                           Called for every image file in the input folder.
            filter_identical: Filter out identical tile pairs (requires translate_path)

        Raises:
            ValueError: If tile dimensions are invalid or overlap is out of range
        """
        if tile_width <= 0 or tile_height <= 0:
            raise ValueError("Tile dimensions must be positive")

        if not (0.0 <= overlap < 1.0):
            raise ValueError("Overlap must be between 0.0 and 1.0 (exclusive)")

        if filter_identical and translate_path is None:
            raise ValueError("filter_identical requires translate_path to be provided")

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.overlap = overlap
        self.translate_path = translate_path
        self.filter_identical = filter_identical

    def tile_image(self, image_path: Union[str, os.PathLike]) -> List[Tile]:
        """
        Process a single image and return its tiles.

        Args:
            image_path: Path to the image file

        Returns:
            List of tiles extracted from the image

        Raises:
            FileNotFoundError: If the image file doesn't exist
            ValueError: If the image cannot be processed
        """
        image_path = Path(image_path)

        try:
            # Load the image
            image_array = load_image(image_path)
            height, width = image_array.shape[:2]

            # Calculate tile positions
            positions = calculate_tile_positions(
                width, height, self.tile_width, self.tile_height, self.overlap
            )

            # Extract tiles
            tiles = []
            for tile_index, (x, y, tile_w, tile_h) in enumerate(positions):
                tile_data = extract_tile(image_array, x, y, tile_w, tile_h)

                tile = Tile(
                    image_data=tile_data,
                    source_path=image_path,
                    x=x,
                    y=y,
                    width=tile_w,
                    height=tile_h,
                    tile_index=tile_index,
                )
                tiles.append(tile)

            return tiles

        except Exception as e:
            raise ValueError(f"Failed to process image {image_path}: {e}") from e

    def tile_folder(self, folder_path: Union[str, os.PathLike]) -> TilingResult:
        """
        Main method that processes all images in a folder and returns tiling results.

        Args:
            folder_path: Path to the folder containing images

        Returns:
            TilingResult containing all extracted tiles or tile pairs

        Raises:
            FileNotFoundError: If the folder doesn't exist
        """
        folder_path = Path(folder_path)

        # Get all image files
        try:
            image_files = get_image_files(folder_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Folder not found: {folder_path}") from e

        if not image_files:
            warnings.warn(f"No image files found in {folder_path}", stacklevel=2)
            return TilingResult(
                tiles=[],
                tile_pairs=[],
                processed_images=[],
                skipped_images=[],
                total_tiles=0,
                filtered_pairs=0,
            )

        if self.translate_path is None:
            # Simple tiling without path translation
            return self._process_simple_tiling(image_files)
        else:
            # Paired tiling with path translation
            return self._process_paired_tiling(image_files)

    def _process_simple_tiling(self, image_files: List[Path]) -> TilingResult:
        """
        Process images for simple tiling without path translation.

        Args:
            image_files: List of image file paths

        Returns:
            TilingResult with tiles
        """
        all_tiles = []
        processed_images = []
        skipped_images = []

        for image_path in image_files:
            try:
                tiles = self.tile_image(image_path)
                all_tiles.extend(tiles)
                processed_images.append(image_path)
            except Exception as e:
                warnings.warn(f"Skipping image {image_path}: {e}", stacklevel=2)
                skipped_images.append(image_path)

        return TilingResult(
            tiles=all_tiles,
            tile_pairs=[],
            processed_images=processed_images,
            skipped_images=skipped_images,
            total_tiles=len(all_tiles),
            filtered_pairs=0,
        )

    def _process_paired_tiling(self, image_files: List[Path]) -> TilingResult:
        """
        Process images for paired tiling with path translation.

        Args:
            image_files: List of image file paths

        Returns:
            TilingResult with tile pairs
        """
        all_tile_pairs = []
        processed_images = []
        skipped_images = []
        filtered_pairs = 0

        for image_path in image_files:
            try:
                # Get translated path
                translated_path = self.translate_path(image_path)
                translated_path = Path(translated_path)

                # Check if translated image exists
                if not translated_path.exists():
                    warnings.warn(
                        f"Translated image not found: {translated_path}", stacklevel=2
                    )
                    skipped_images.append(image_path)
                    continue

                # Extract tiles from both images
                input_tiles = self.tile_image(image_path)
                output_tiles = self.tile_image(translated_path)

                # Ensure we have the same number of tiles
                if len(input_tiles) != len(output_tiles):
                    warnings.warn(
                        f"Tile count mismatch for {image_path}: {len(input_tiles)} vs {len(output_tiles)}",
                        stacklevel=2,
                    )
                    skipped_images.append(image_path)
                    continue

                # Create tile pairs
                for input_tile, output_tile in zip(input_tiles, output_tiles):
                    is_identical = arrays_equal(
                        input_tile.image_data, output_tile.image_data
                    )

                    # Filter identical pairs if requested
                    if self.filter_identical and is_identical:
                        filtered_pairs += 1
                        continue

                    tile_pair = TilePair(
                        input_tile=input_tile,
                        output_tile=output_tile,
                        is_identical=is_identical,
                    )
                    all_tile_pairs.append(tile_pair)

                processed_images.append(image_path)

            except Exception as e:
                warnings.warn(f"Skipping image {image_path}: {e}", stacklevel=2)
                skipped_images.append(image_path)

        total_tiles = len(all_tile_pairs) + filtered_pairs

        return TilingResult(
            tiles=[],
            tile_pairs=all_tile_pairs,
            processed_images=processed_images,
            skipped_images=skipped_images,
            total_tiles=total_tiles,
            filtered_pairs=filtered_pairs,
        )
