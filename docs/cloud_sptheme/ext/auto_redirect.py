"""
==================================================================
:mod:`cloud_sptheme.ext.auto_redirect` -- Redirect Deprecated URLs
==================================================================

.. versionadded:: 1.9

Overview
========
This extension is helpful for when html documentation has been relocated
to a new host; e.g. moving from ``pythonhosted.org`` to ``readthedocs.io``.
Once enabled, it adds a helpful "Documentation has moved" message to the top
of every page, and automatically redirects the user as well.

Configuration
=============
This extension looks for the following config options:

    ``auto_redirect_subject``
    
        subject to insert into message.
        defaults to ``The {project name} documentation``.

    ``auto_redirect_domain_url``
        
        url to redirect user to.
        no message or redirect will happen if this isn't set.

    ``auto_redirect_domain_footer``
    
        optional footer text to append to message

Internals
=========
This should work with other sphinx themes, the js & css is (mostly) generic.

.. todo:: 

    the "redirect to exact page" part of JS code currently only works
    with this theme; would like to fix that.
    
.. todo::

    support configuring redirects to other pages within same documentation.

.. todo::

    if user has dismissed "auto redirect", remember via cookie?
"""
#=============================================================================
# imports
#=============================================================================
# core
import os
# site
from docutils.nodes import raw
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util.pycompat import htmlescape
# pkg
from cloud_sptheme import __version__, _root_dir, is_cloud_theme
from cloud_sptheme.utils import add_static_file
# local
__all__ = [
    "setup",
]

#=============================================================================
# patch builder to copy css file (if needed)
#=============================================================================

ext_static_dir = os.path.join(_root_dir, "ext", "static")

cloud_base_js_path = os.path.join(_root_dir, "themes", "cloud", "static", "cloud_base.js")

class RedirectHelper(object):

    template_path = os.path.join(ext_static_dir, "auto_redirect.html_t")
    css_path = os.path.join(ext_static_dir, "auto_redirect.css")

    def __init__(self, app):
        self.app = app

    @property
    def for_html(self):
        return isinstance(self.app.builder, StandaloneHTMLBuilder)

    @property
    def domain_subject(self):
        config = self.app.config
        return config.auto_redirect_domain_subject or \
               "The %s documentation" % (config.project,)
    @property
    def domain_url(self):
        return self.app.config.auto_redirect_domain_url

    @property
    def domain_root(self):
        root = self.app.config.auto_redirect_domain_root
        # XXX: use urljoin here?
        if not root:
            return self.domain_url
        if root[:1] == "/" and root[:2] != "//":
            return self.domain_url + root
        return root

    @property
    def domain_footer(self):
        return self.app.config.auto_redirect_domain_footer

    @property
    def timeout(self):
        return self.app.config.auto_redirect_timeout or 10


def install_static_assets(app):
    # skip unless html builder & redirect configured
    helper = RedirectHelper(app)
    if not helper.for_html or not helper.domain_url:
        return

    # make sure JS is added
    if not is_cloud_theme(app.config.html_theme):
        add_static_file(app.builder, cloud_base_js_path, javascript=True)

    # make sure needed css styling gets included when building html
    add_static_file(app.builder, helper.css_path, stylesheet=True)


# FIXME: This doesn't get called for auto-generated pages, e.g. search page & genindex.
#        Need to modify this code to get run as part of builder.handle_page() call,
#        such as via event that insert_canonical_link() is using below.
def prepend_redirect(app, doctree):

    """
    called after doctree has been read;
    inserted "Raw" node with our content.
    """
    # skip unless configured, and using html builder
    helper = RedirectHelper(app)
    if not helper.for_html or not helper.domain_url:
        return

    # render fragment into insert
    builder = app.builder
    renderer = builder.templates
    ctx = dict(app=app, redirector=helper)
    with open(helper.template_path) as fh:
        content = renderer.render_string(fh.read(), ctx)

    # insert raw node w/ content
    node = raw(content, content, format="html")
    doctree.insert(0, node)


def insert_canonical_link(app, pagename, templatename, context, doctree):
    # skip unless html builder & redirect configured
    helper = RedirectHelper(app)
    root_url = helper.domain_root
    if not helper.for_html or not root_url:
        return

    # XXX: any gotchas w/ generating url from pagename this way?
    url = "%s/%s.html" % (root_url.rstrip("/"), pagename)

    # insert "canonical" link to help search engines
    # XXX: skipping this if another ext sets this?
    # XXX: split this out under separate name / extension?
    meta = context.get("metatags", "")
    context['metatags'] = meta + '<link rel="canonical" href="%s" />\n' % htmlescape(url, True)

#=============================================================================
# register extension
#=============================================================================
def setup(app):
    #
    # register config vars
    #

    # title to use when referring to project.
    # defaults to "The {project} documentation"
    app.add_config_value("auto_redirect_domain_subject", None, "html")

    # base url to redirect to -- if not set, extension does nothing.
    app.add_config_value("auto_redirect_domain_url", None, "html")

    # optional url suffix to add before adding per-page redirects.
    app.add_config_value("auto_redirect_domain_root", None, "html")

    # optional html to append to message
    app.add_config_value("auto_redirect_domain_footer", None, "html")

    # seconds before redirecting via JS
    app.add_config_value("auto_redirect_timeout", 10, "html")

    #
    # connect events
    # XXX: can we connect events on the fly? could do single check when builder init'd,
    #      and attach events there as needed.  could then make everything a method
    #      of the redirect helper.
    #
    app.connect("builder-inited", install_static_assets)
    app.connect("doctree-read", prepend_redirect)
    app.connect("html-page-context", insert_canonical_link)

    #
    # identifies the version of our extension
    #
    return {'version': __version__}

#=============================================================================
# eof
#=============================================================================
