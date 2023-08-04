# S2DL - Sentinel 2 Downloader

S2DL is a Python library for downloading Sentinel-2 L1C and L2A satellite imagery data.
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

product_id = "S2A_MSIL2A_20220111T021351_N0301_R060_T50HLK_20220111T041611"
target_directory = Path("./data")
target_directory.mkdir(exist_ok=True)

# Fetch and save a single Sentinel-2 product's data
scene_dir = fetch_single_sentinel_product(product_id, target_directory)
```

For downloading multiple products:

```python
from s2dl import fetch_multiple_sentinel_products
from pathlib import Path

product_ids = [
    "S2A_MSIL2A_20220111T021351_N0301_R060_T50HLK_20220111T041611",
    "S2A_MSIL1C_20230712T032521_N0509_R018_T52WFD_20230712T051642",
]
target_directory = Path("./data")
target_directory.mkdir(exist_ok=True)

# Fetch and save multiple Sentinel-2 products' data
scene_dirs = fetch_multiple_sentinel_products(product_ids, target_directory)
```

## Contributions

We welcome contributions from the community. Please submit a pull request with your improvements or bug fixes.

## License

S2DL is licensed under the MIT License.
