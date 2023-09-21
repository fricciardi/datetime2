"""
cloud_sptheme.ext.relbar_toc -- adds TOC entry (and other links) to relbar.
NOTE: this has been renamed to 'relbar_links'. this module is left as a legacy alias.
"""
#=========================================================
# imports
#=========================================================
# core
from __future__ import absolute_import, division, print_function
import warnings
# pkg
from . import relbar_links
# local
__all__ = [
    "setup"
]

#=========================================================
# sphinx entrypoint
#=========================================================
def setup(app):
    """
    setup extension for sphinx run
    """
    # TODO: decide when to remove this, and promote to "DeprecationWarning"
    warnings.warn("'cloud_sptheme.ext.relbar_toc' is deprecated, "
                  "use 'cloud_sptheme.ext.relbar_links' instead",
                  PendingDeprecationWarning)
    return relbar_links.setup(app)

#=========================================================
# eof
#=========================================================
