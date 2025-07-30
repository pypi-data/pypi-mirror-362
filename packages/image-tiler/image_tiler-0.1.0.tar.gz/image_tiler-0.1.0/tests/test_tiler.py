"""
Tests for the ImageTiler class.
"""

import os
import tempfile
from pathlib import Path

import pytest
from PIL import Image

from image_tiler import ImageTiler


class TestImageTiler:
    """Test cases for ImageTiler class."""

    def test_init_valid_params(self):
        """Test initialization with valid parameters."""
        tiler = ImageTiler(256, 256, 0.1)
        assert tiler.tile_width == 256
        assert tiler.tile_height == 256
        assert tiler.overlap == 0.1
        assert tiler.translate_path is None
        assert tiler.filter_identical is False

    def test_init_invalid_tile_dimensions(self):
        """Test initialization with invalid tile dimensions."""
        with pytest.raises(ValueError, match="Tile dimensions must be positive"):
            ImageTiler(0, 256)

        with pytest.raises(ValueError, match="Tile dimensions must be positive"):
            ImageTiler(256, -1)

    def test_init_invalid_overlap(self):
        """Test initialization with invalid overlap value."""
        with pytest.raises(ValueError, match="Overlap must be between 0.0 and 1.0"):
            ImageTiler(256, 256, -0.1)

        with pytest.raises(ValueError, match="Overlap must be between 0.0 and 1.0"):
            ImageTiler(256, 256, 1.0)

    def test_init_filter_identical_without_translate_path(self):
        """Test initialization with filter_identical but no translate_path."""
        with pytest.raises(
            ValueError, match="filter_identical requires translate_path"
        ):
            ImageTiler(256, 256, filter_identical=True)

    def test_tile_image_basic(self):
        """Test basic image tiling functionality."""
        # Create a temporary image
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img = Image.new("RGB", (100, 100), color="red")
            img.save(tmp.name)
            tmp_path = tmp.name

        try:
            tiler = ImageTiler(50, 50, 0.0)
            tiles = tiler.tile_image(tmp_path)

            # Should have 4 tiles for a 100x100 image with 50x50 tiles
            assert len(tiles) == 4

            # Check first tile
            assert tiles[0].x == 0
            assert tiles[0].y == 0
            assert tiles[0].width == 50
            assert tiles[0].height == 50
            assert tiles[0].tile_index == 0
            assert tiles[0].source_path == Path(tmp_path)
            assert tiles[0].image_data.shape == (50, 50, 3)

        finally:
            os.unlink(tmp_path)

    def test_tile_image_with_overlap(self):
        """Test image tiling with overlap."""
        # Create a temporary image
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img = Image.new("RGB", (100, 100), color="red")
            img.save(tmp.name)
            tmp_path = tmp.name

        try:
            tiler = ImageTiler(50, 50, 0.2)  # 20% overlap
            tiles = tiler.tile_image(tmp_path)

            # With 20% overlap, step size is 40 pixels
            # Starting at 0, next tile at 40, but 40+50=90 > 100, so only 2 tiles per row/column
            # So we should have 2x2 = 4 tiles (no partial tiles)
            assert len(tiles) == 4

            # Check positions
            assert tiles[0].x == 0 and tiles[0].y == 0
            assert tiles[1].x == 40 and tiles[1].y == 0
            assert tiles[2].x == 0 and tiles[2].y == 40
            assert tiles[3].x == 40 and tiles[3].y == 40

        finally:
            os.unlink(tmp_path)

    def test_tile_image_edge_cases(self):
        """Test edge cases in image tiling."""
        # Create a small image smaller than tile size
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img = Image.new("RGB", (30, 30), color="red")
            img.save(tmp.name)
            tmp_path = tmp.name

        try:
            tiler = ImageTiler(50, 50, 0.0)
            tiles = tiler.tile_image(tmp_path)

            # Should have 0 tiles since image is smaller than tile size
            assert len(tiles) == 0

        finally:
            os.unlink(tmp_path)

    def test_tile_image_exact_size(self):
        """Test image tiling with image exactly matching tile size."""
        # Create an image that's exactly the tile size
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img = Image.new("RGB", (50, 50), color="red")
            img.save(tmp.name)
            tmp_path = tmp.name

        try:
            tiler = ImageTiler(50, 50, 0.0)
            tiles = tiler.tile_image(tmp_path)

            # Should have exactly 1 tile
            assert len(tiles) == 1
            assert tiles[0].width == 50
            assert tiles[0].height == 50
            assert tiles[0].x == 0
            assert tiles[0].y == 0

        finally:
            os.unlink(tmp_path)

    def test_tile_folder_simple(self):
        """Test folder processing without path translation."""
        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)

            # Create test images
            img1_path = tmpdir / "image1.png"
            img2_path = tmpdir / "image2.png"

            img1 = Image.new("RGB", (100, 100), color="red")
            img2 = Image.new("RGB", (100, 100), color="blue")

            img1.save(img1_path)
            img2.save(img2_path)

            tiler = ImageTiler(50, 50, 0.0)
            result = tiler.tile_folder(tmpdir)

            # Should have 8 tiles total (4 from each image)
            assert len(result.tiles) == 8
            assert len(result.tile_pairs) == 0
            assert len(result.processed_images) == 2
            assert len(result.skipped_images) == 0
            assert result.total_tiles == 8
            assert result.filtered_pairs == 0

    def test_tile_folder_with_translation(self):
        """Test folder processing with path translation."""
        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)

            # Create input and output directories
            input_dir = tmpdir / "input"
            output_dir = tmpdir / "output"
            input_dir.mkdir()
            output_dir.mkdir()

            # Create test images
            img1_path = input_dir / "image1.png"
            img2_path = input_dir / "image2.png"
            out1_path = output_dir / "image1.png"
            out2_path = output_dir / "image2.png"

            img1 = Image.new("RGB", (100, 100), color="red")
            img2 = Image.new("RGB", (100, 100), color="blue")
            out1 = Image.new("RGB", (100, 100), color="green")
            out2 = Image.new("RGB", (100, 100), color="yellow")

            img1.save(img1_path)
            img2.save(img2_path)
            out1.save(out1_path)
            out2.save(out2_path)

            def translate_path(input_path):
                return str(input_path).replace("input", "output")

            tiler = ImageTiler(50, 50, 0.0, translate_path=translate_path)
            result = tiler.tile_folder(input_dir)

            # Should have 8 tile pairs total (4 from each image pair)
            assert len(result.tiles) == 0
            assert len(result.tile_pairs) == 8
            assert len(result.processed_images) == 2
            assert len(result.skipped_images) == 0
            assert result.total_tiles == 8
            assert result.filtered_pairs == 0

    def test_tile_folder_with_filtering(self):
        """Test folder processing with identical tile filtering."""
        with tempfile.TemporaryDirectory() as tmpdir_str:
            tmpdir = Path(tmpdir_str)

            # Create input and output directories
            input_dir = tmpdir / "input"
            output_dir = tmpdir / "output"
            input_dir.mkdir()
            output_dir.mkdir()

            # Create identical test images
            img_path = input_dir / "image1.png"
            out_path = output_dir / "image1.png"

            img = Image.new("RGB", (100, 100), color="red")
            img.save(img_path)
            img.save(out_path)  # Same image

            def translate_path(input_path):
                return str(input_path).replace("input", "output")

            tiler = ImageTiler(
                50, 50, 0.0, translate_path=translate_path, filter_identical=True
            )
            result = tiler.tile_folder(input_dir)

            # All tiles should be filtered out as identical
            assert len(result.tile_pairs) == 0
            assert result.filtered_pairs == 4  # 4 tiles were filtered
            assert result.total_tiles == 4

    def test_tile_folder_nonexistent(self):
        """Test folder processing with non-existent folder."""
        tiler = ImageTiler(50, 50, 0.0)

        with pytest.raises(FileNotFoundError, match="Folder not found"):
            tiler.tile_folder("/nonexistent/folder")

    def test_tile_folder_empty(self):
        """Test folder processing with empty folder."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tiler = ImageTiler(50, 50, 0.0)

            with pytest.warns(UserWarning, match="No image files found"):
                result = tiler.tile_folder(tmpdir)

            assert len(result.tiles) == 0
            assert len(result.processed_images) == 0
            assert result.total_tiles == 0
