from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="s2dl",
    version="0.3",
    url="https://github.com/DPIRD-DMA/S2DL",
    author="Nick Wright",
    author_email="nicholas.wright@dpird.wa.gov.au",
    description="S2DL is a Python library for downloading Sentinel-2 L1C and L2A satellite imagery data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
)
