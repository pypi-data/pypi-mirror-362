"""
Utility functions for image loading and processing.
"""

import os
from pathlib import Path
from typing import List, Union

import numpy as np
from PIL import Image


def load_image(image_path: Union[str, os.PathLike]) -> np.ndarray:
    """
    Load an image from disk and return as numpy array.

    Args:
        image_path: Path to the image file

    Returns:
        Image as numpy array

    Raises:
        FileNotFoundError: If the image file doesn't exist
        ValueError: If the image cannot be loaded
    """
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    try:
        with Image.open(image_path) as img:
            # Convert to RGB if needed (handles RGBA, grayscale, etc.)
            if img.mode != "RGB":
                img = img.convert("RGB")
            return np.array(img)
    except Exception as e:
        raise ValueError(f"Failed to load image {image_path}: {e}") from e


def get_image_files(folder_path: Union[str, os.PathLike]) -> List[Path]:
    """
    Get all image files from a folder.

    Args:
        folder_path: Path to the folder containing images

    Returns:
        List of image file paths

    Raises:
        FileNotFoundError: If the folder doesn't exist
    """
    folder_path = Path(folder_path)

    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not folder_path.is_dir():
        raise ValueError(f"Path is not a directory: {folder_path}")

    # Common image extensions
    image_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".tiff",
        ".tif",
        ".bmp",
        ".gif",
        ".webp",
    }

    image_files = []
    for file_path in folder_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)

    return sorted(image_files)


def calculate_tile_positions(
    image_width: int,
    image_height: int,
    tile_width: int,
    tile_height: int,
    overlap: float,
) -> List[tuple]:
    """
    Calculate tile positions for an image with overlap.

    Args:
        image_width: Width of the source image
        image_height: Height of the source image
        tile_width: Width of each tile
        tile_height: Height of each tile
        overlap: Overlap as fraction of tile size (0.0-1.0)

    Returns:
        List of (x, y, width, height) tuples for each tile
    """
    if not (0.0 <= overlap < 1.0):
        raise ValueError("Overlap must be between 0.0 and 1.0 (exclusive)")

    if tile_width <= 0 or tile_height <= 0:
        raise ValueError("Tile dimensions must be positive")

    if image_width <= 0 or image_height <= 0:
        raise ValueError("Image dimensions must be positive")

    # Calculate step size
    step_x = int(tile_width * (1 - overlap))
    step_y = int(tile_height * (1 - overlap))

    # Ensure minimum step size of 1
    step_x = max(1, step_x)
    step_y = max(1, step_y)

    positions = []

    y = 0
    while y + tile_height <= image_height:
        x = 0
        while x + tile_width <= image_width:
            # Only add tiles that can be the full desired size
            positions.append((x, y, tile_width, tile_height))

            x += step_x
            if x + tile_width > image_width:
                break

        y += step_y
        if y + tile_height > image_height:
            break

    return positions


def extract_tile(
    image_array: np.ndarray, x: int, y: int, width: int, height: int
) -> np.ndarray:
    """
    Extract a tile from an image array.

    Args:
        image_array: Source image as numpy array
        x: X coordinate of the tile
        y: Y coordinate of the tile
        width: Width of the tile
        height: Height of the tile

    Returns:
        Tile as numpy array
    """
    # Ensure coordinates are within bounds
    x = max(0, min(x, image_array.shape[1] - 1))
    y = max(0, min(y, image_array.shape[0] - 1))

    # Extract the tile
    tile = image_array[y : y + height, x : x + width]

    return tile


def arrays_equal(arr1: np.ndarray, arr2: np.ndarray, tolerance: float = 1e-6) -> bool:
    """
    Check if two numpy arrays are equal within a tolerance.

    Args:
        arr1: First array
        arr2: Second array
        tolerance: Tolerance for comparison

    Returns:
        True if arrays are equal within tolerance
    """
    if arr1.shape != arr2.shape:
        return False

    return np.allclose(arr1, arr2, atol=tolerance)
