# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="SynMem",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Pillow",
        "rapidfuzz",
        "numpy"
    ],
    author="Tristan McBride Sr.",
    author_email="TristanMcBrideSr@users.noreply.github.com",
    description="A Modern 4-Stage Synthetic Memory",
)
