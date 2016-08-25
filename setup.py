"""
setup.py
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("VERSION", "r") as version:
    TAG = version.readline().strip()

PYPI_DISTNAME = "suffixtree"
PACKAGE_NAME = PYPI_DISTNAME
DESCRIPTION = "Yet another suffix tree implementation in Python"
GIT_URL = "https://github.com/cartoonist/"
VCS_URL = GIT_URL + PYPI_DISTNAME
TAR_URL = GIT_URL + PYPI_DISTNAME + "/tarball/" + TAG
KEYWORDS = ['suffix', 'tree', 'indexing', 'data structure']
REQUIRES = ['graphviz==0.4.10']
AUTHOR = "Ali Ghaffaari"
EMAIL = "ali.ghaffaari@gmail.com"

setup(
    name=PYPI_DISTNAME,
    packages=[PACKAGE_NAME],
    version=TAG,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=VCS_URL,
    download_url=TAR_URL,
    keywords=KEYWORDS,
    classifiers=[],
    install_requires=REQUIRES,
)
