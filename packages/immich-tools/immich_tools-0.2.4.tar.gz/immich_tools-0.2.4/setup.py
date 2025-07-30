from setuptools import setup, find_packages
import src

setup(
    name="immich-tools",
    version=src.__version__,
    packages=find_packages(),
    install_requires=["click", "requests", "PyExifTool", "pytest", "dacite"],
    entry_points={
        "console_scripts": [
            "immich-tools = src.cli:main",
        ],
    },
)
