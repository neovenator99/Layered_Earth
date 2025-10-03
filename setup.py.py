from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="layered-earth",
    version="1.0.0",
    author="neovenator99",
    description="Geospatial Special Support System - Interactive mapping and analysis library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "geopandas>=0.10.0",
        "rasterio>=1.2.0",
        "matplotlib>=3.3.0",
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "shapely>=1.7.0",
        "contextily>=1.2.0",
        "requests>=2.25.0",
        "plotly>=5.0.0",
    ],
    entry_points={
        "console_scripts": [
            "layered-earth=layered_earth:launch",
        ],
    },
)