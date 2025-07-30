# python/cbits/__init__.py
##
# @file python/cbits/__init__.py
# @package cbits
# @brief cbits – High-performance BitVector for Python.
# 
# This module exposes the Python-level API for the BitVector C extension.
# 
# @author lambdaphoenix
# @version 0.1.1
# @copyright Copyright (c) 2025 lambdaphoenix
"""
cbits – High-performance BitVector for Python.

This module exposes the Python-level API for the BitVector C extension.

Author lambdaphoenix

Version 0.1.1

Copyright (c) 2025 lambdaphoenix
"""
from ._cbits import BitVector, __author__, __version__, __license__, __license_url__

##
# @brief The package author's name.
__author__ = _cbits.__author__
"""The package author's name."""

##
# @brief The current package version, synchronized with the C extension's version.
__version__ = _cbits.__version__
"""The current package version, synchronized with the C extension's version."""

##
# @brief SPDX short identifier for the license under which this package is released.
__license__ = _cbits.__license__
"""SPDX short identifier for the license under which this package is released."""

##
# @brief URL pointing to the full text of the LICENSE file in the project's GitHub repository.
__license_url__ = _cbits.__license_url__
"""URL pointing to the full text of the LICENSE file in the project's GitHub repository."""

##
# @defgroup cbits_api Public API
# @brief Symbols exposed to Python users
# @{
__all__ = [
    "BitVector",
]
"""cbits_api - Symbols exposed to Python users"""
## @} (end of cbits_api)