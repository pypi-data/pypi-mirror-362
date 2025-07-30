#!/usr/bin/env python3
"""
Simple CLI interface for image-tiler library.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image

from image_tiler import ImageTiler


def main():
    parser = argparse.ArgumentParser(
        description="Extract tiles from images with support for overlapping tiles and paired processing"
    )

    parser.add_argument(
        "input_path",
        help="Path to input folder containing images, or path to single image file",
    )

    parser.add_argument(
        "--tile-width",
        type=int,
        default=256,
        help="Width of each tile in pixels (default: 256)",
    )

    parser.add_argument(
        "--tile-height",
        type=int,
        default=256,
        help="Height of each tile in pixels (default: 256)",
    )

    parser.add_argument(
        "--overlap",
        type=float,
        default=0.0,
        help="Overlap as fraction of tile size, 0.0-1.0 (default: 0.0)",
    )

    parser.add_argument(
        "--output-dir", help="Directory to save extracted tiles (optional)"
    )

    parser.add_argument(
        "--filter-identical",
        action="store_true",
        help="Filter out identical tile pairs (requires --translate-pattern)",
    )

    parser.add_argument(
        "--translate-pattern",
        help="Pattern for path translation, e.g. 'input,output' to replace 'input' with 'output'",
    )

    args = parser.parse_args()

    # Validate arguments
    if not (0.0 <= args.overlap < 1.0):
        print("Error: Overlap must be between 0.0 and 1.0 (exclusive)")
        sys.exit(1)

    if args.filter_identical and not args.translate_pattern:
        print("Error: --filter-identical requires --translate-pattern")
        sys.exit(1)

    # Set up path translation function if provided
    translate_path = None
    if args.translate_pattern:
        try:
            from_pattern, to_pattern = args.translate_pattern.split(",", 1)

            def translate_path(p):
                return str(p).replace(from_pattern, to_pattern)

        except ValueError:
            print("Error: --translate-pattern must be in format 'from,to'")
            sys.exit(1)

    # Create tiler
    tiler = ImageTiler(
        tile_width=args.tile_width,
        tile_height=args.tile_height,
        overlap=args.overlap,
        translate_path=translate_path,
        filter_identical=args.filter_identical,
    )

    input_path = Path(args.input_path)

    try:
        if input_path.is_file():
            # Process single image
            print(f"Processing single image: {input_path}")
            tiles = tiler.tile_image(input_path)

            print(f"Generated {len(tiles)} tiles")

            if args.output_dir:
                save_tiles(tiles, args.output_dir)
            else:
                print("Use --output-dir to save tiles to disk")

        elif input_path.is_dir():
            # Process folder
            print(f"Processing folder: {input_path}")
            result = tiler.tile_folder(input_path)

            print(f"Processed {len(result.processed_images)} images")
            print(f"Generated {result.total_tiles} tiles")

            if result.skipped_images:
                print(f"Skipped {len(result.skipped_images)} images")

            if result.filtered_pairs > 0:
                print(f"Filtered {result.filtered_pairs} identical pairs")

            if args.output_dir:
                if result.tiles:
                    save_tiles(result.tiles, args.output_dir)
                else:
                    save_tile_pairs(result.tile_pairs, args.output_dir)
            else:
                print("Use --output-dir to save tiles to disk")

        else:
            print(f"Error: Input path does not exist: {input_path}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def save_tiles(tiles, output_dir):
    """Save tiles to output directory."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Saving {len(tiles)} tiles to {output_path}")

    for tile in tiles:
        # Create filename
        source_name = Path(tile.source_path).stem
        filename = f"{source_name}_tile_{tile.tile_index:03d}_{tile.x}_{tile.y}.png"

        # Save tile
        tile_path = output_path / filename
        img = Image.fromarray(tile.image_data)
        img.save(tile_path)

    print(f"Tiles saved to: {output_path}")


def save_tile_pairs(tile_pairs, output_dir):
    """Save tile pairs to output directory."""
    output_path = Path(output_dir)
    input_dir = output_path / "input_tiles"
    output_tiles_dir = output_path / "output_tiles"

    input_dir.mkdir(parents=True, exist_ok=True)
    output_tiles_dir.mkdir(parents=True, exist_ok=True)

    print(f"Saving {len(tile_pairs)} tile pairs to {output_path}")

    for pair in tile_pairs:
        # Create filename
        source_name = Path(pair.input_tile.source_path).stem
        filename = f"{source_name}_tile_{pair.input_tile.tile_index:03d}_{pair.input_tile.x}_{pair.input_tile.y}.png"

        # Save input tile
        input_tile_path = input_dir / filename
        img = Image.fromarray(pair.input_tile.image_data)
        img.save(input_tile_path)

        # Save output tile
        output_tile_path = output_tiles_dir / filename
        img = Image.fromarray(pair.output_tile.image_data)
        img.save(output_tile_path)

    print(f"Tile pairs saved to: {output_path}")


if __name__ == "__main__":
    main()
