"""
Tests for utility functions.
"""

import os
import tempfile
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from image_tiler.utils import (
    arrays_equal,
    calculate_tile_positions,
    extract_tile,
    get_image_files,
    load_image,
)


class TestUtils:
    """Test cases for utility functions."""

    def test_load_image_valid(self):
        """Test loading a valid image."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img = Image.new("RGB", (100, 100), color="red")
            img.save(tmp.name)
            tmp_path = tmp.name

        try:
            image_array = load_image(tmp_path)
            assert image_array.shape == (100, 100, 3)
            assert image_array.dtype == np.uint8
            # Check that it's red (255, 0, 0)
            assert np.all(image_array[:, :, 0] == 255)
            assert np.all(image_array[:, :, 1] == 0)
            assert np.all(image_array[:, :, 2] == 0)
        finally:
            os.unlink(tmp_path)

    def test_load_image_nonexistent(self):
        """Test loading a non-existent image."""
        with pytest.raises(FileNotFoundError, match="Image file not found"):
            load_image("/nonexistent/image.png")

    def test_get_image_files_valid(self):
        """Test getting image files from a valid directory."""
        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)

            # Create test images
            img1_path = tmpdir / "image1.png"
            img2_path = tmpdir / "image2.jpg"
            txt_path = tmpdir / "not_image.txt"

            Image.new("RGB", (10, 10)).save(img1_path)
            Image.new("RGB", (10, 10)).save(img2_path)
            txt_path.write_text("not an image")

            image_files = get_image_files(tmpdir)

            # Should find 2 image files, sorted
            assert len(image_files) == 2
            assert img1_path in image_files
            assert img2_path in image_files
            assert txt_path not in image_files

    def test_get_image_files_nonexistent(self):
        """Test getting image files from a non-existent directory."""
        with pytest.raises(FileNotFoundError, match="Folder not found"):
            get_image_files("/nonexistent/folder")

    def test_get_image_files_empty(self):
        """Test getting image files from an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            image_files = get_image_files(tmpdir)
            assert len(image_files) == 0

    def test_calculate_tile_positions_no_overlap(self):
        """Test calculating tile positions without overlap."""
        positions = calculate_tile_positions(100, 100, 50, 50, 0.0)

        expected = [(0, 0, 50, 50), (50, 0, 50, 50), (0, 50, 50, 50), (50, 50, 50, 50)]

        assert positions == expected

    def test_calculate_tile_positions_with_overlap(self):
        """Test calculating tile positions with overlap."""
        positions = calculate_tile_positions(100, 100, 50, 50, 0.2)

        # Step size should be 40 (50 * 0.8)
        # Only tiles that can be full size (50x50) are included
        expected = [
            (0, 0, 50, 50),
            (40, 0, 50, 50),
            (0, 40, 50, 50),
            (40, 40, 50, 50),
        ]

        assert positions == expected

    def test_calculate_tile_positions_invalid_overlap(self):
        """Test calculating tile positions with invalid overlap."""
        with pytest.raises(ValueError, match="Overlap must be between 0.0 and 1.0"):
            calculate_tile_positions(100, 100, 50, 50, -0.1)

        with pytest.raises(ValueError, match="Overlap must be between 0.0 and 1.0"):
            calculate_tile_positions(100, 100, 50, 50, 1.0)

    def test_calculate_tile_positions_invalid_dimensions(self):
        """Test calculating tile positions with invalid dimensions."""
        with pytest.raises(ValueError, match="Tile dimensions must be positive"):
            calculate_tile_positions(100, 100, 0, 50, 0.0)

        with pytest.raises(ValueError, match="Image dimensions must be positive"):
            calculate_tile_positions(0, 100, 50, 50, 0.0)

    def test_extract_tile_basic(self):
        """Test basic tile extraction."""
        # Create a test image array
        image_array = np.zeros((100, 100, 3), dtype=np.uint8)
        image_array[10:60, 10:60] = [255, 0, 0]  # Red square

        tile = extract_tile(image_array, 10, 10, 50, 50)

        assert tile.shape == (50, 50, 3)
        assert np.all(tile == [255, 0, 0])

    def test_extract_tile_edge_clipping(self):
        """Test tile extraction with edge clipping."""
        image_array = np.zeros((100, 100, 3), dtype=np.uint8)

        # Extract tile that goes beyond image bounds
        tile = extract_tile(image_array, 80, 80, 50, 50)

        # Should get a 20x20 tile (clipped to image bounds)
        assert tile.shape == (20, 20, 3)

    def test_arrays_equal_identical(self):
        """Test array equality with identical arrays."""
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([1, 2, 3])

        assert arrays_equal(arr1, arr2)

    def test_arrays_equal_different_shape(self):
        """Test array equality with different shapes."""
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([[1, 2], [3, 4]])

        assert not arrays_equal(arr1, arr2)

    def test_arrays_equal_different_values(self):
        """Test array equality with different values."""
        arr1 = np.array([1, 2, 3])
        arr2 = np.array([1, 2, 4])

        assert not arrays_equal(arr1, arr2)

    def test_arrays_equal_with_tolerance(self):
        """Test array equality with tolerance."""
        arr1 = np.array([1.0, 2.0, 3.0])
        arr2 = np.array([1.001, 2.001, 3.001])

        assert arrays_equal(arr1, arr2, tolerance=1e-2)
        assert not arrays_equal(arr1, arr2, tolerance=1e-4)
