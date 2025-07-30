# Image Tiler

A Python library for extracting tiles from images in a folder, with support for overlapping tiles and paired image processing for AI model training.

## Features

- **Flexible Tiling**: Extract tiles of any size from images with configurable overlap
- **Batch Processing**: Process entire folders of images efficiently
- **Paired Processing**: Support for training AI models with input/output image pairs
- **Intelligent Filtering**: Optional filtering of identical tiles to improve training efficiency
- **Comprehensive Error Handling**: Robust handling of edge cases and invalid inputs
- **Memory Efficient**: Process large datasets without loading all images into memory simultaneously

## Installation

```bash
# Install with uv (recommended)
uv add image-tiler

# Or install with pip
pip install image-tiler
```

## Quick Start

### Basic Tiling

```python
from image_tiler import ImageTiler
from pathlib import Path

# Create a tiler with 256x256 tiles and 10% overlap
tiler = ImageTiler(tile_width=256, tile_height=256, overlap=0.1)

# Process all images in a folder
result = tiler.tile_folder("/path/to/images")

# Access the tiles
for tile in result.tiles:
    print(f"Tile from {tile.source_path} at ({tile.x}, {tile.y})")
    print(f"Tile shape: {tile.image_data.shape}")
```

### Paired Image Processing (for AI Training)

```python
from image_tiler import ImageTiler
from pathlib import Path

def translate_path(input_path):
    """
    This function is called for every image file found in the input folder.
    It should return the corresponding output image path.
    """
    input_path = Path(input_path)
    # Example: translate from input/ to output/ directory
    return input_path.parent.parent / "output" / input_path.name

# Create tiler with path translation and filtering
tiler = ImageTiler(
    tile_width=512, 
    tile_height=512, 
    overlap=0.2,
    translate_path=translate_path,
    filter_identical=True  # Skip identical input/output pairs
)

result = tiler.tile_folder("/path/to/input/images")

# Process tile pairs for training
for pair in result.tile_pairs:
    if not pair.is_identical:
        input_data = pair.input_tile.image_data
        output_data = pair.output_tile.image_data
        # Use for training...
```

### Single Image Processing

```python
from image_tiler import ImageTiler

tiler = ImageTiler(tile_width=256, tile_height=256, overlap=0.1)

# Process a single image
tiles = tiler.tile_image("/path/to/image.jpg")

for tile in tiles:
    print(f"Tile {tile.tile_index}: {tile.width}x{tile.height} at ({tile.x}, {tile.y})")
```

## API Reference

### ImageTiler

The main class for extracting tiles from images.

```python
class ImageTiler:
    def __init__(
        self, 
        tile_width: int, 
        tile_height: int, 
        overlap: float = 0.0,
        translate_path: Optional[Callable] = None,
        filter_identical: bool = False
    )
```

**Parameters:**
- `tile_width`: Width of each tile in pixels
- `tile_height`: Height of each tile in pixels  
- `overlap`: Overlap as fraction of tile size (0.0-1.0)
- `translate_path`: Optional function to map input paths to output paths
- `filter_identical`: Filter out identical tile pairs (requires `translate_path`)

**Methods:**
- `tile_image(image_path)`: Process a single image, returns `List[Tile]`
- `tile_folder(folder_path)`: Process all images in a folder, returns `TilingResult`

### Data Structures

#### Tile

Represents a single tile extracted from an image.

```python
@dataclass
class Tile:
    image_data: np.ndarray              # The tile image data
    source_path: Union[str, os.PathLike] # Path to source image
    x: int                              # X coordinate in source image
    y: int                              # Y coordinate in source image
    width: int                          # Tile width
    height: int                         # Tile height
    tile_index: int                     # Sequential tile number
```

#### TilePair

Represents a pair of tiles for AI training.

```python
@dataclass
class TilePair:
    input_tile: Tile
    output_tile: Tile
    is_identical: bool     # Whether tiles are identical
```

#### TilingResult

Results from processing a folder of images.

```python
@dataclass
class TilingResult:
    tiles: List[Tile]                    # When no translation function
    tile_pairs: List[TilePair]           # When translation function provided
    processed_images: List[Path]         # Successfully processed images
    skipped_images: List[Path]           # Images that couldn't be processed
    total_tiles: int                     # Total number of tiles generated
    filtered_pairs: int                  # Number of filtered identical pairs
```

## Examples

### Different Overlap Strategies

```python
from image_tiler import ImageTiler

# No overlap - tiles are adjacent
tiler_no_overlap = ImageTiler(256, 256, overlap=0.0)

# 50% overlap - significant overlap between tiles
tiler_high_overlap = ImageTiler(256, 256, overlap=0.5)

# 10% overlap - slight overlap for better coverage
tiler_slight_overlap = ImageTiler(256, 256, overlap=0.1)
```

### Custom Path Translation

```python
def custom_translate_path(input_path):
    """Example: Convert noise/image.jpg to clean/image.jpg"""
    return str(input_path).replace("noise", "clean")

def suffix_translate_path(input_path):
    """Example: Convert image.jpg to image_output.jpg"""
    path = Path(input_path)
    return path.parent / f"{path.stem}_output{path.suffix}"

tiler = ImageTiler(
    tile_width=256, 
    tile_height=256,
    translate_path=custom_translate_path
)
```

### Processing Results

```python
from image_tiler import ImageTiler

tiler = ImageTiler(256, 256, overlap=0.1)
result = tiler.tile_folder("/path/to/images")

print(f"Processed {len(result.processed_images)} images")
print(f"Generated {result.total_tiles} tiles")
print(f"Skipped {len(result.skipped_images)} images")

if result.filtered_pairs > 0:
    print(f"Filtered {result.filtered_pairs} identical pairs")
```

## Supported Image Formats

The library supports all common image formats through Pillow:
- PNG
- JPEG
- TIFF
- BMP
- GIF
- WebP

## Requirements

- Python 3.8+
- NumPy
- Pillow (PIL)

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/image-tiler.git
cd image-tiler

# Install with development dependencies
uv sync --dev

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=image_tiler

# Format code
uv run black src/ tests/
uv run isort src/ tests/

# Type checking
uv run mypy src/
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.