#!/usr/bin/env python
"""Minimal setup script for APILinker."""

from setuptools import setup, find_packages

__version__ = "0.1.0"

setup(
    name="apilinker",
    version=__version__,
    description="A universal bridge to connect, map, and automate data transfer between any two REST APIs",
    author="K. Kartas",
    author_email="kkartas@users.noreply.github.com",
    url="https://github.com/kkartas/APILinker",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.23.0",
        "pyyaml>=6.0",
        "typer>=0.7.0",
        "pydantic>=1.10.2",
        "croniter>=1.3.8",
        "rich>=12.6.0",
    ],
    entry_points={
        "console_scripts": [
            "apilinker=apilinker.cli:app",
        ],
    },
)
