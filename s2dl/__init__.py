from .__version__ import __version__

from .s2dl import (
    fetch_multiple_sentinel_products,
    fetch_single_sentinel_product,
)

__all__ = [
    "__version__",
    "fetch_multiple_sentinel_products",
    "fetch_single_sentinel_product",
]
