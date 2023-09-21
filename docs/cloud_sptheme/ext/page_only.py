"""
==============================================================
:mod:`cloud_sptheme.ext.page_only` -- Exclude Pages from Build
==============================================================

.. versionadded:: 1.8

Overview
========
This extension provides a ``.. page-only::`` directive,
which allows conditionally omitting entire pages from the document based on build tags.

The first line of a page should be a ``.. page-only:: <expr>`` directive;
where ``<expr>`` is a tag, or simple tag expression, just like ``.. only::``.
If the expression evaluates to False, the page won't be included in the final build
(and should be silently omitted from any TOC lists).

E.g. ``.. page-only:: draft and html``
"""
#=============================================================================
# imports
#=============================================================================
# core
from __future__ import absolute_import, division, print_function
import io
import re
from weakref import WeakKeyDictionary
# site
from docutils.parsers.rst import Directive
import sphinx
import sphinx.addnodes
from sphinx.util import logging
# pkg
from cloud_sptheme import __version__
from cloud_sptheme.utils import patchapplier, monkeypatch
# local
logger = logging.getLogger(__name__)
__all__ = [
    "setup",
]

#=============================================================================
# patching
#=============================================================================
@patchapplier
def _patch_sphinx():

    #
    # to get files list right, best to modify found_files before env.get_outdated_files()
    # gets a hold of them, and starts looking for changes.
    #
    from sphinx.environment import BuildEnvironment
    @monkeypatch(BuildEnvironment)
    def get_outdated_files(__wrapped__, env, config_changed):
        # call out hook to modify found_docs to remove omitted entries,
        # and store them in env.omitted_by_page_only
        strip_omitted_docs(env)

        # hand off to orig function
        return __wrapped__(env, config_changed)

    #
    # patch TocTree.run() so it doesn't warning about broken toc entries.
    #
    from sphinx.directives.other import TocTree
    @monkeypatch(TocTree)
    def run(__wrapped__, self):
        env = self.state.document.settings.env
        omitted_docs = env.omitted_by_pageonly
        found_docs = env.found_docs
        try:
            # temporarily restore found_docs so TocTree doesn't throw warning.
            # NOTE: this causes broken toc entries to be generated (rather than warnings).
            #       these are cleaned up by remove_toc_entries() below
            _set_found_docs(env, found_docs | omitted_docs)
            return __wrapped__(self)
        finally:
            _set_found_docs(env, found_docs)


def _set_found_docs(env, found_docs):
    """
    compat helper for writing found_docs attribute
    """
    if sphinx.version_info < (2, 0):
        env.found_docs = found_docs
    else:
        env.project.docnames = found_docs

#=============================================================================
# hooks
#=============================================================================

#: regex used to detect page-only directive
_header_re = re.compile(r"^\.\.\s+page-only::\s+(?P<expr>.+)\s*$")


#: as hack, using this to store reference to app so we can resolve it w/in env monkeypatch
_env_to_app = WeakKeyDictionary()


def install_app_ref(app):
    """
    hack to get app ref w/in env.get_outdated_files() monkeypatch,
    called on 'builder-inited' event
    """
    _env_to_app[app.env] = app


def strip_omitted_docs(env):
    """
    helper invoked right before env.get_outdated_files() is called,
    scans for omitted files and modifies document set accordingly.

    called via monkeypatch before .get_outdated_files() is run,
    which happens during env.update(), shortly before 'env-get-outdated' event.
    """
    # scan through found docs, removing any that should be omitted
    app = _env_to_app[env]
    found_docs = env.found_docs
    omitted_docs = set()
    for doc in found_docs:
        # find first non-empty line
        with io.open(env.doc2path(doc), encoding="latin-1") as fh:
            line = ''
            for line in fh:
                if line.strip():
                    break

        # check if it's a PageOnly directive
        m = _header_re.match(line)
        if not m:
            continue

        # add page to omitted list if expression doesn't validate
        if not app.tags.eval_condition(m.group("expr")):
            omitted_docs.add(doc)

    if omitted_docs:
        logger.info("%s pages omitted by page-only" % len(omitted_docs))

    # persist omitted list for TocTree.run() wrapper and remove_from_toc()
    env.omitted_by_pageonly = omitted_docs

    # remove omitted from 'found_docs', so get_outdated_files() doesn't see them
    found_docs.difference_update(omitted_docs)


class PageOnly(Directive):
    """
    Directive used to capture info.
    Notes that this doesn't actually do anything, job has already been done by find_omitted_docs().
    This is just here to prevent parse errors.
    """
    # NOTE: cloned from Author directive, should be ok...
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}

    def run(self):
        # XXX: could issue warning if this is encountered anywhere but top of document.
        return []


def remove_from_toc(app, doctree):
    """
    remove omitted pages from TOC, let through by TocTree.run() monkeypatch
    called on doctree-read event.
    """
    omitted_docs = app.env.omitted_by_pageonly
    for toctreenode in doctree.traverse(sphinx.addnodes.toctree):
        entries = toctreenode['entries']
        # print("%r %r %r" % (doctree, toctreenode, entries))
        # dbgcon()
        idx = 0
        while idx < len(entries):
            entry = entries[idx]
            # entry is (label|None, doc) tuple...
            if str(entry[1]) in omitted_docs:
                del entries[idx]
            else:
                idx += 1

#=============================================================================
# sphinx entrypoint
#=============================================================================
def setup(app):
    _patch_sphinx()
    app.add_directive('page-only', PageOnly)
    app.connect('builder-inited', install_app_ref)
    app.connect('doctree-read', remove_from_toc)

    # identifies the version of our extension
    return {'version': __version__}

#=============================================================================
# eoc
#=============================================================================
