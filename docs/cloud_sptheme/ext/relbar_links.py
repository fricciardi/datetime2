"""
=================================================================
:mod:`cloud_sptheme.ext.relbar_links` - adds TOC entry to relbar
=================================================================

.. module:: cloud_sptheme.ext.relbar_links
    :synopsis: adds TOC entry to right side of relbar

.. versionadded:: 1.8.1

Overview
========
This Sphinx extension allows you to insert links into
the navigation bar ("relbar") at the top of bottom of all pages.

While it can be configured with arbitrary links, by default it automatically
inserts a Table Of Contents entry, similar to the old python documentation format.
This is mainly useful when the title link in the navigation bar has been redirected
to page other than Table Of Contents (such as allowed by the ``roottarget``
option of the :doc:`/cloud_theme`).

Configuration
=============
By default, this inserts a "TOC" link to the right of any "Next" or "Previous"
buttons, which points to your sphinx master document.

It can be customized using the following options in ``conf.py``:

``relbar_links``

    Optional list of links to insert, defaults to ``["toc"]``.
    Each list item can have one of four formats:

    * A dictionary containing the keys ``"page"`` and ``"label"``,
      as well as optional ``"key"`` and ``"title"`` keywords.

      "page" should be the an absolute path to your page (e.g. "contents",
      or "lib/mypage"). "label" is the text that will be displayed on the link,
      "title" is the tooltip set for the link, and "key" is the accesskey
      for selecting the link.

    * A 2-element tuple of ``(page, label)``

    * A 4-element tuple of ``(page, title, key, label)``

    * The predefined string ``"toc"``, which is replaced with a table
      of contents link to your master document.

``relbar_links_after``

    When inserting the links, this extension will place them as far
    left as possible, so long as they are to the right of any links
    that are included in this list. Defaults to ``["next", "previous"]``.
"""
#=========================================================
# imports
#=========================================================
# core
from __future__ import absolute_import, division, print_function
import logging
log = logging.getLogger(__name__)
# site
from sphinx.locale import _
# pkg
from cloud_sptheme import __version__
from cloud_sptheme.utils import unicode
# local
__all__ = [
    "setup"
]

#=========================================================
# helpers
#=========================================================

# indices for looking up link-row elements in relbar entry
# TODO: find authoriative source for this info.
NAME = 0  # name of document
TITLE = 1  # used for [title] attribute
ACCESS_KEY = 2  # used for [accesskey] attribute
LABEL = 3  # used for link content (NOTE: has already been run through translation)


def parse_entry(app, entry):
    """
    normalize entry representation from config
    """
    if entry == "toc":
        master_doc = app.config.master_doc
        return master_doc, _("Table Of Contents"), "C", _("toc")
    if isinstance(entry, (list, tuple)):
        if len(entry) == 4:
            return entry
        if len(entry) == 2:
            page, label = entry
            return page, label, None, label
    elif isinstance(entry, dict):
        page = entry.get("page")
        label = entry.get("label")
        if not (page and label):
            raise ValueError("dict must define at least 'page' and "
                             "'label': %r" % (entry,))
        title = entry.get("title") or label
        key = entry.get("key")
        return page, title, key, label
    raise ValueError("expected dict or 2/4-element sequence: %r" % (entry,))

#=========================================================
# hooks
#=========================================================

def insert_relbar_links(app, pagename, templatename, ctx, event_arg):
    # check for relbar link list
    # NOTE: not defined for some pages of some builders,
    #       e.g. json builder's "genindex" page.
    if "rellinks" not in ctx:
        return
    links = ctx['rellinks']

    # get list of links to insert
    custom_links = [parse_entry(app, entry)
                    for entry in app.config.relbar_links]

    # remove existing links with same label
    # NOTE: unicode() wrapper is to resolve any _TranslationProxy() instances
    custom_labels = set(unicode(entry[LABEL]) for entry in custom_links)
    idx = 0
    while idx < len(links):
        if unicode(links[idx][LABEL]) in custom_labels:
            del links[idx]
        else:
            idx += 1

    # insert custom links to right of any "next" / "previous" links
    # NOTE: 'links' is in right to left order!
    after_labels = set(unicode(_(label)) for label in app.config.relbar_links_after)
    for pos, entry in enumerate(links):
        if unicode(entry[LABEL]) in after_labels:
            break
    else:
        pos = len(links)

    # insert links
    links[pos:pos] = custom_links

#=========================================================
# sphinx entrypoint
#=========================================================
def setup(app):
    """
    setup extension for sphinx run
    """

    # let user customize list of links
    app.add_config_value('relbar_links', ["toc"], 'env')
    app.add_config_value('relbar_links_after', ["next", "previous"], 'env')

    # attach rewrite-hook
    app.connect('html-page-context', insert_relbar_links)

    # identifies the version of our extension
    return {'version': __version__}

#=========================================================
# eof
#=========================================================
