"""
cloud_sptheme.utils -- internal helper utilities
"""
#=============================================================================
# imports
#=============================================================================
# core
from functools import update_wrapper
import logging; log = logging.getLogger(__name__)
import os
import sys
# site
import sphinx
from sphinx.util.fileutil import copyfile
# pkg
# local
__all__ = [
    # py2/3 compat
    'PY2', 'PY3', 'u', 'ru',
    'unicode', 'unicode_or_str',

    # monkeypatch helpers
    "patchapplier",
    "monkeypatch",
]

#=============================================================================
# internal py2/3 compat helpers
#=============================================================================
PY2 = sys.version_info < (3,0)
PY3 = not PY2

# FIXME: these aren't very rigorous / correct, but they work for current purposes.
if PY2:
    def u(s):
        return s.decode("unicode_escape")
    def ru(s):
        return s.decode("ascii")
    unicode = unicode
    unicode_or_str = (unicode, str)
else:
    def u(s):
        return s
    ru = u
    unicode = str
    unicode_or_str = (str,)

#=============================================================================
# monkeypatch helpers
#=============================================================================
def patchapplier(func):
    """
    function decorator to help functions that apply a monkeypatch.
    makes them only run once.
    """
    def wrapper():
        if wrapper.patched:
            return False
        func()
        wrapper.patched = True
        logging.getLogger(func.__module__).debug("%s: patch applied", func.__name__)
        return True
    wrapper.patched = False
    update_wrapper(wrapper, func)
    return wrapper

def monkeypatch(target, name=None):
    """
    helper to monkeypatch another object.
    the decorated function is wrapped around the existing function in
    :samp:`target.{name}`, and used to replace it.

    **name** defaults to the name of the function being decorated.

    the original value is passed in as the first positional argument to the function.
    """
    def builder(func):
        attr = name or func.__name__
        wrapped = getattr(target, attr)
        def wrapper(*args, **kwds):
            return func(wrapped, *args, **kwds)
        update_wrapper(wrapper, wrapped)
        wrapper.__wrapped__ = wrapped # not set by older update_wrapper() versions
        setattr(target, attr, wrapper)
        return func # return orig func so we can use it again
    return builder

#=============================================================================
# sphinx helpers
#=============================================================================

def _patch_html_extra_static(builder):
    """
    monkeypatch hook for add_static_file() to use
    """
    config = builder.config
    if hasattr(config, "html_extra_static"):
        return

    @monkeypatch(builder)
    def copy_static_files(wrapped):
        wrapped()
        # NOTE: code modeled after copy_static_files()...
        ctx = builder.globalcontext.copy()
        for source, target in config.html_extra_static:
            # 'source' existence should already be checked by add_static_file(),
            # 'target' should already be abspath w/in outdir
            copyfile(source, target)

    config.html_extra_static = []


def add_static_file(builder, source, name=None, stylesheet=False,
                    javascript=False):
    """
    monkeypatch sphinx's html builder to include specified static file.
    
    will copy file to :samp:`{outdir}/_static/{name}`.

    :param builder:
        ref to HTMLBuilder
        
    :param source: 
        path to source file
    
    :param name:
        name for target file; defaults to base name of source file.
        
    :param stylesheet:
        register file as additional stylesheet
    """
    app = builder.app
    _patch_html_extra_static(builder)

    if not os.path.exists(source):
        builder.warn('static asset %r does not exist' % source)
        return

    if not name:
        name = os.path.basename(source)

    target = os.path.join(builder.outdir, "_static", name)
    if stylesheet:
        if sphinx.version_info < (1, 8):
            app.add_stylesheet(name)
        else:
            app.add_css_file(name)

    if javascript:
        if sphinx.version_info < (1, 8):
            app.add_javascript(name)
        else:
            app.add_js_file(name)

    builder.config.html_extra_static.append((source, target))

#=============================================================================
# eof
#=============================================================================
