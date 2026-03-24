#!/usr/bin/env python
"""Setup script for crime_analysis package."""

from setuptools import setup, find_packages

setup(
    name="crime_analysis",
    version="0.1.0",
    description="Crime Data Analysis Pipeline",
    author="Crime Analysis Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas==2.1.4",
        "numpy==1.26.3",
        "matplotlib==3.8.2",
        "seaborn==0.13.2",
        "pytest==7.4.4",
        "pytest-cov==4.1.0",
        "argparse==1.4.0",
    ],
    entry_points={
        "console_scripts": [
            "crime-analysis=main:main",
        ],
    },
    python_requires=">=3.9",
)
