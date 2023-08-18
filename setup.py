#! /usr/bin/env python

import os

from setuptools import find_packages, setup

PACKAGE_NAME = "idr_torch"
VERSIONFILE = "VERSION"
AUTHOR = "IDRIS"
AUTHOR_EMAIL = "assist@idris.fr"
URL = "https://www.idris.fr"

with open(os.path.join(PACKAGE_NAME, VERSIONFILE), "r") as file:
    VERSION = file.read().strip()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
)
