#!/usr/bin/env python3
"""
Example usage of the image-tiler library.
"""

import os
import shutil
import tempfile
from pathlib import Path

from PIL import Image

from image_tiler import ImageTiler


def create_sample_images():
    """Create some sample images for demonstration."""
    temp_dir = Path(tempfile.mkdtemp())
    print(f"Creating sample images in: {temp_dir}")

    # Create sample images
    for i in range(3):
        img = Image.new(
            "RGB", (200, 200), color=f"#{i * 80:02x}{i * 60:02x}{i * 40:02x}"
        )
        img_path = temp_dir / f"sample_{i}.png"
        img.save(img_path)
        print(f"Created: {img_path}")

    return temp_dir


def demonstrate_basic_tiling():
    """Demonstrate basic image tiling."""
    print("\n=== Basic Image Tiling Demo ===")

    # Create sample images
    image_dir = create_sample_images()

    # Create tiler with 100x100 tiles and 20% overlap
    tiler = ImageTiler(tile_width=100, tile_height=100, overlap=0.2)

    # Process the folder
    result = tiler.tile_folder(image_dir)

    print(f"Processed {len(result.processed_images)} images")
    print(f"Generated {result.total_tiles} tiles total")

    # Show details for first few tiles
    print("\nFirst 5 tiles:")
    for i, tile in enumerate(result.tiles[:5]):
        print(
            f"  Tile {i}: {tile.width}x{tile.height} at ({tile.x}, {tile.y}) "
            f"from {tile.source_path.name}"
        )

    # Clean up
    shutil.rmtree(image_dir)


def demonstrate_paired_processing():
    """Demonstrate paired image processing."""
    print("\n=== Paired Image Processing Demo ===")

    temp_dir = Path(tempfile.mkdtemp())
    input_dir = temp_dir / "input"
    output_dir = temp_dir / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    print(f"Creating paired images in: {temp_dir}")

    # Create input and output image pairs
    for i in range(2):
        # Input image (noisy)
        input_img = Image.new(
            "RGB", (150, 150), color=f"#{i * 100:02x}{i * 80:02x}{i * 60:02x}"
        )
        input_path = input_dir / f"image_{i}.png"
        input_img.save(input_path)

        # Output image (clean version)
        output_img = Image.new(
            "RGB", (150, 150), color=f"#{i * 120:02x}{i * 100:02x}{i * 80:02x}"
        )
        output_path = output_dir / f"image_{i}.png"
        output_img.save(output_path)

    # Define path translation function
    def translate_path(input_path):
        return str(input_path).replace("input", "output")

    # Create tiler with paired processing
    tiler = ImageTiler(
        tile_width=75,
        tile_height=75,
        overlap=0.1,
        translate_path=translate_path,
        filter_identical=False,  # Don't filter for demo
    )

    result = tiler.tile_folder(input_dir)

    print(f"Processed {len(result.processed_images)} image pairs")
    print(f"Generated {len(result.tile_pairs)} tile pairs")

    # Show details for first few pairs
    print("\nFirst 3 tile pairs:")
    for i, pair in enumerate(result.tile_pairs[:3]):
        print(
            f"  Pair {i}: Input tile from {pair.input_tile.source_path.name} "
            f"at ({pair.input_tile.x}, {pair.input_tile.y})"
        )
        print(
            f"          Output tile from {pair.output_tile.source_path.name} "
            f"at ({pair.output_tile.x}, {pair.output_tile.y})"
        )
        print(f"          Identical: {pair.is_identical}")

    # Clean up
    shutil.rmtree(temp_dir)


def demonstrate_single_image():
    """Demonstrate processing a single image."""
    print("\n=== Single Image Processing Demo ===")

    # Create a sample image
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        img = Image.new("RGB", (300, 200), color="blue")
        img.save(tmp.name)
        tmp_path = tmp.name

    print(f"Processing single image: {tmp_path}")

    # Create tiler
    tiler = ImageTiler(tile_width=100, tile_height=100, overlap=0.0)

    # Process the image
    tiles = tiler.tile_image(tmp_path)

    print(f"Generated {len(tiles)} tiles from single image")

    # Show all tiles
    print("\nAll tiles:")
    for tile in tiles:
        print(
            f"  Tile {tile.tile_index}: {tile.width}x{tile.height} "
            f"at ({tile.x}, {tile.y})"
        )

    # Clean up
    os.unlink(tmp_path)


if __name__ == "__main__":
    print("Image Tiler Library Demo")
    print("=" * 50)

    demonstrate_basic_tiling()
    demonstrate_paired_processing()
    demonstrate_single_image()

    print("\n" + "=" * 50)
    print("Demo complete!")
