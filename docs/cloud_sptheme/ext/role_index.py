"""
======================================================
:mod:`cloud_sptheme.ext.role_index` -- JSON Role Index
======================================================

.. versionadded:: 1.8

Overview
========
This sphinx extension for the HTML builder places a file called ``roleindex.json``
in the output directory along with the documentation.  This file contains
a dictionary which mapping all reference ids (made via ``:ref:`` or ``:doc:``) to
a 3-element list of ``(page, anchor, title)``

This is useful for integrating a Sphinx manual into the online help of web application --
context-specific help can be provided by looking up a predefined ``:ref:`` tag within
the json file, and redirecting the user to the appropriate page and anchor location.

As an example, see the `roleindex.json <../roleindex.json>`_ for this documentation.

.. warning::

    This extension should be considered "beta" quality.
    It was recently written, may have unknown issues, and may need to be revised.

Configuration
=============
This extension reads the following ``conf.py`` options:

    ``role_index_style``

        style of json output -- can be ``"compact"`` (the default), or ``"pretty"`` (for debugging).
"""
#=========================================================
# imports
#=========================================================
# core
from __future__ import absolute_import, division, print_function
import codecs
import logging
log = logging.getLogger(__name__)
import json
import os
# site
from sphinx.locale import _TranslationProxy
# pkg
from cloud_sptheme import __version__
# local
__all__ = [
    "setup",
]
#=========================================================
# hooks
#=========================================================
def write_role_index(app):
    """
    helper which generates ``"roleindex.json"`` for document.
    """
    if app.builder.name != "html":
        return

    style = app.config.role_index_style or "compact"

    index = {}

    # add 'ref' role mappings
    index['ref'] = dict(
        (key, (page, anchor, label))
        for key, (page, anchor, label)
        in app.env.domaindata['std']['labels'].items()
    )

    # add 'doc' role mappings
    index['doc'] = dict(
        (doc.lower(), (doc, "", title.astext()))
        for doc, title in app.env.titles.items()
    )

    # create composite 'all' mapping
    index['any'] = index['doc'].copy()
    index['any'].update(index['ref'])

    # write to file
    def encode(value):
        if isinstance(value, _TranslationProxy):
            return str(value)
        raise TypeError("can't serialize value: %r (type=%r)" % (value, type(value)))

    target = os.path.join(app.builder.outdir, "roleindex.json")
    kwds = dict(sort_keys=True, separators=(",", ":"), default=encode)
    if style == "compact":
        pass
    elif style == "pretty":
        kwds.update(separators=(", ", ": "), indent=True)
    else:
        raise ValueError("unknown role_index_style: %r" % style)
    with codecs.open(target, "w", encoding="utf-8") as fh:
        json.dump(index, fh, **kwds)

#=========================================================
# sphinx entrypoint
#=========================================================
def setup(app):

    app.add_config_value('role_index_style', None, 'html')

    # XXX: this probably isn't right event to attach to...
    #      but want to run during writing phase, after all pages have been scanned into tree,
    #      and this seems like close to the right place.
    def wrapper(app):
        write_role_index(app)
        return []
    app.connect('html-collect-pages', wrapper)

    # identifies the version of our extension
    return {'version': __version__}

#=========================================================
# eof
#=========================================================
