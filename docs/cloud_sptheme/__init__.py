"""
This module contains a few small sphinx extensions.
They are mainly used to help with the generation
of BPS's own documentation, but some other projects
use them as well, so they are kept here.
"""
#=============================================================================
# imports
#=============================================================================
# core
import re
import os.path
from warnings import warn
# site
# WARNING: since this is imported by setup.py, it's critical the toplevel
#          not depend on any imports outside of stdlib & setuptools
# local
__all__ = [
    # constants
    "__version__",
    "std_exts",
    "all_exts",

    # theme setup
    "get_theme_dir",  # deprecated
    # "_iter_theme_sources()",  # used by setup.py
    # "setup",  # used by sphinx.html_theme entrypoint

    # public helpers
    "get_version",

    # internal helpers
    "is_cloud_theme",
]

#=============================================================================
# constants
#=============================================================================

#: canonical version string
__version__ = '1.10.1.post20200504175005'

#: names of standard cloud extensions used by most cloud themes
std_exts = [
    'cloud_sptheme.ext.autodoc_sections',
    'cloud_sptheme.ext.autoattribute_search_bases',
    'cloud_sptheme.ext.docfield_markup',
    'cloud_sptheme.ext.escaped_samp_literals',
    'cloud_sptheme.ext.index_styling',
    'cloud_sptheme.ext.relbar_links',
    'cloud_sptheme.ext.table_styling',
]

#: names of all cloud extensions
all_exts = std_exts + [
    'cloud_sptheme.ext.issue_tracker',
]

#=============================================================================
# theme setup
#=============================================================================

#: root of this package
_root_dir = os.path.abspath(os.path.dirname(__file__))

#: root of themes subdir
_theme_dir = os.path.join(_root_dir, "themes")


def get_theme_dir():
    """Returns path to directory containing this package's Sphinx themes.

    .. deprecated:: 1.7

        As of Sphinx 1.2, this is passed to Sphinx via a ``setup.py`` entry point,
        and no longer needs to be included in your documentation's ``conf.py``.
    """
    warn("get_theme_dir() is deprecated, and will be removed in version 2.0",
         DeprecationWarning, stacklevel=1)
    return _theme_dir


def _iter_theme_sources():
    """
    setup helper -- iterates over ``(theme name, theme path)`` pairs
    for all HTML themes in this package.
    """
    base = _theme_dir
    assert os.path.isabs(base)
    for name in os.listdir(base):
        path = os.path.join(base, name)
        if os.path.exists(os.path.join(path, "theme.conf")):
            yield name, path


def setup(app):
    """
    sphinx 1.6 entrypoint for registring HTML themes;
    required by "sphinx.html_themes" entrypoint.
    """
    for name, path in _iter_theme_sources():
        app.add_html_theme(name, path)

#=============================================================================
# misc public helpers
#=============================================================================

def get_version(release):
    """
    Derive short version string from longer 'release' string.

    This is quick helper which takes a project's ``release`` string,
    and generates the shortened ``version`` string required by ``conf.py``.
    Usage example for ``conf.py``::

        import cloud_sptheme as csp

        ...

        # The version info for the project you're documenting
        from myapp import __version__ as release
        version = csp.get_version(release)
    """
    return re.match("(\d+\.\d+)", release).group(1)

#=============================================================================
# misc internal helpers
#=============================================================================

def is_cloud_theme(name):
    """
    [hack] internal helper to check if named theme belongs to this package
    """
    # TODO: find way to detect if an external theme *derives* from this package
    return os.path.isfile(os.path.join(_theme_dir, name, "theme.conf"))

#=============================================================================
# eof
#=============================================================================
