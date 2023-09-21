"""
cloud_sptheme.tests.utils -- test helpers
"""
#=============================================================================
# imports
#=============================================================================
# core
from __future__ import absolute_import, division, print_function
import logging
log = logging.getLogger(__name__)
try:
    import unittest2 as unittest
except ImportError:
    import unittest
# site
# pkg
# local
__all__ = [
    "TestCase",
    "unittest",
]

#=============================================================================
# custom test case
#=============================================================================
class TestCase(unittest.TestCase):

    pass

#=============================================================================
# eof
#=============================================================================

