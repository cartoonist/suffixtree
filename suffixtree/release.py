# coding=utf-8

"""
    suffixtree.release
    ~~~~~~~~~~~~~~~~~~

    Include release information of the package.

    :copyright: (c) 2016 by Ali Ghaffaari.
    :license: MIT, see LICENSE for more details.
"""

# CONSTANTS ###################################################################
# Development statuses:
DS_PLANNING = 1
DS_PREALPHA = 2
DS_ALPHA = 3
DS_BETA = 4
DS_STABLE = 5
DS_MATURE = 6
DS_INACTIVE = 7
DS_STRING = {
    DS_PLANNING: 'Development Status :: 1 - Planning',
    DS_PREALPHA: 'Development Status :: 2 - Pre-Alpha',
    DS_ALPHA: 'Development Status :: 3 - Alpha',
    DS_BETA: 'Development Status :: 4 - Beta',
    DS_STABLE: 'Development Status :: 5 - Production/Stable',
    DS_MATURE: 'Development Status :: 6 - Mature',
    DS_INACTIVE: 'Development Status :: 7 - Inactive'
}
###############################################################################

# Package release information.
__title__ = 'suffixtree'
__description__ = 'Yet another suffix tree implementation in Python'
__author__ = 'Ali Ghaffaari'
__email__ = 'ali.ghaffaari@mpi-inf.mpg.de'
__license__ = 'MIT'

# Release
__version__ = '0.2.0'
__status__ = DS_ALPHA

# PyPI-related information
__keywords__ = 'suffix tree indexing data-structure'
__classifiers__ = [
    # Development status
    DS_STRING[__status__],

    # License
    'License :: OSI Approved :: MIT License',

    # Supported Python versions.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',

    # Intended Audience and Topic
    'Intended Audience :: Science/Research',
    'Topic :: Text Processing :: Indexing',
]
__requires__ = ['graphviz==0.4.10']
__tests_require__ = []
__extras_require__ = {
    'test': ['nose>=1.0', 'coverage'],
}
__setup_requires__ = ['nose>=1.0', 'coverage']
__entry_points__ = '''
'''
