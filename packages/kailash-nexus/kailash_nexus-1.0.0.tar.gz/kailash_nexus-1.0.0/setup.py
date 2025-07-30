"""Setup script for Kailash Nexus."""

from setuptools import find_packages, setup

setup(
    name="kailash-nexus",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "kailash>=0.6.6",
    ],
    python_requires=">=3.8",
)
