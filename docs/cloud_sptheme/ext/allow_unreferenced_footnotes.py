"""
cloud_sptheme.ext.allow_unreferenced_footnotes --
hack that silences "Footnote XXX is not referenced" warnings in Sphinx.

TODO: include this in documentation.
"""
#=============================================================================
# imports
#=============================================================================
# core
import os
# site
from sphinx.transforms import UnreferencedFootnotesDetector
# pkg
from cloud_sptheme import __version__
# local
__all__ = [
    "setup",
]

#=============================================================================
# register extension
#=============================================================================
def setup(app):
    # remove transform from list
    transforms = app.registry.get_transforms()
    try:
        transforms.remove(UnreferencedFootnotesDetector)
    except ValueError:
        pass

    # identifies the version of our extension
    return {'version': __version__}

#=============================================================================
# eof
#=============================================================================
