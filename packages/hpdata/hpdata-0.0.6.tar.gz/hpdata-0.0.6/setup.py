#!/usr/bin/env python
import pathlib
import pkg_resources
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


with pathlib.Path("requirements.txt").open() as requirements_txt:
    requirements = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="hpdata",
    version="0.0.6",
    author="Data Product Sq",
    author_email="sid.jang@healingpaper.com",
    description="Data Product Sq Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/healingpaper/vegas-workflow",
    packages=find_packages(),
    install_requires=requirements,
)
