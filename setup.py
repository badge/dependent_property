#!/usr/bin/env python
"""pathlib Package
"""
import re

from pathlib import Path
from setuptools import find_packages, setup


long_description = Path("README.md").read_text()


def find_version():
    """Get the current version of the package

    Returns
    -------
    str
        The current version of the package
    """

    here = Path(__file__).resolve().parent

    text = (here / "dependent_property" / "__init__.py").read_text()

    version_match = re.search(
        pattern=r"^__version__ = ['\"]([^'\"]*)['\"]", string=text, flags=re.M
    )

    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="dependent_property",
    version=find_version(),
    description="Create dependent relationships between class attributes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Matthew Badger",
    packages=find_packages(),
)
