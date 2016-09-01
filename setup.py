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
CLASSIFIERS = [
    # Project maturity:
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # License
    'License :: OSI Approved :: MIT License',

    # Supported Python versions.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',

    # Others
    'Intended Audience :: Science/Research',
    'Topic :: Text Processing :: Indexing',
]

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
    classifiers=CLASSIFIERS,
    install_requires=REQUIRES,
)
