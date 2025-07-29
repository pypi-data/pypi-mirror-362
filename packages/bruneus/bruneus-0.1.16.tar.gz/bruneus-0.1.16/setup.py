# Author: yokoe <kreuz45@kreuz45.com>
# Copyright (c) 2023- yokoe
# Licence: MIT

from setuptools import setup

DESCRIPTION = "bruneus: BigQuery helper utils."
NAME = "bruneus"
AUTHOR = "yokoe"
AUTHOR_EMAIL = "kreuz45@kreuz45.com"
URL = "https://github.com/yokoe/bruneus"
LICENSE = "MIT"
DOWNLOAD_URL = URL
VERSION = "0.1.16"
PYTHON_REQUIRES = ">=3.9"
INSTALL_REQUIRES = [
    "google-cloud-bigquery>=3.4.0",
    "Jinja2>=3.0.0",
    "pandas>=1.4.0",
    "db-dtypes>=1.0.5",
]
PACKAGES = ["bruneus"]
PACKAGE_DIR = {"": "src"}
KEYWORDS = "bigquery"
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
]
with open("README.md", "r", encoding="utf-8") as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES,
)
