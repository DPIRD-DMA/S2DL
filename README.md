# S2DL - Sentinel 2 Downloader

S2DL is a Python library for downloading Sentinel-2 L1C satellite imagery data.
## Features

- Download Sentinel-2 product data using product IDs

## Installation

You can install the S2DL library via pip:

```bash
pip install s2dl
```

## Usage

Here's a simple usage example:

```python
from s2dl import fetch_single_sentinel_product
from pathlib import Path

product_id = "S2B_MSIL1C_20190523T150729_N0207_R082_T18MZA_20190523T183104"
target_directory = Path("./data")

# Fetch and save a single Sentinel-2 product's data
scene_dir = fetch_single_sentinel_product(product_id, target_directory)
```

For downloading multiple products:

```python
from s2dl import fetch_multiple_sentinel_products
from pathlib import Path

product_ids = ["S2B_MSIL1C_20190523T150729_N0207_R082_T18MZA_20190523T183104", "...", "..."]
target_directory = Path("./data")

# Fetch and save multiple Sentinel-2 products' data
scene_dirs = fetch_multiple_sentinel_products(product_ids, target_directory)
```

## Contributions

We welcome contributions from the community. Please submit a pull request with your improvements or bug fixes.

## License

S2DL is licensed under the MIT License.
