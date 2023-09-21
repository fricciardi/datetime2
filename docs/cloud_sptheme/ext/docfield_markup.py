"""
cloud_sptheme.ext.docfield_markup -- monkeypatches sphinx to allow ``~`` in docfields.
"""
#=============================================================================
# imports
#=============================================================================
# core
import logging; log = logging.getLogger(__name__)
# site
# pkg
from cloud_sptheme import __version__
from cloud_sptheme.utils import patchapplier, monkeypatch
# local
__all__ = [
    "setup",
]

#=============================================================================
# patch
#=============================================================================
@patchapplier
def _patch_docfield():
    from sphinx.util.docfields import Field, nodes, addnodes

    # NOTE: would like to just wrap make_xref(), but have to override first arg (rawsource) of
    #       pending_xref() call, so have to replicate the code.

    @monkeypatch(Field)
    def make_xref(_wrapped, self, rolename, domain, target, innernode=addnodes.literal_emphasis,
                  contnode=None, env=None):
        #------------------------------------------------------------------------
        # custom prep work before real sphinx code.
        #------------------------------------------------------------------------

        # given raw text in 'target', parse into 'title' and effective 'target'
        # NOTE: this tries to replicate the markup convention used in PyXRefRole.process_link()
        rawtext = title = target
        if rawtext.startswith("~"):
            # if the first character is a tilde, don't display the module/class
            # parts of the content
            target = target.lstrip("~")
            title = target.rpartition(".")[2]

        # create wrapper for innernode(title,title) calls, which honors custom title.
        # NOTE: doing as wrapper so code below will match sphinx as closely as possible.
        #       could instead just plug this in as contnode (if not already set)
        node_type = innernode

        def innernode(*ignored):
            if issubclass(node_type, nodes.Text):
                # Text classes want rawtext second
                return node_type(title, rawtext)
            else:
                # Element classes want rawtext first
                return node_type(rawtext, title)

        #------------------------------------------------------------------------
        # remainder of this should match sphinx code exactly, except where noted.
        #------------------------------------------------------------------------
        if not rolename:
            return contnode or innernode(target, target)
        # NOTE: passing <title> as first arg, sphinx passes ''
        refnode = addnodes.pending_xref(title, refdomain=domain, refexplicit=False,
                                        reftype=rolename, reftarget=target)
        refnode += contnode or innernode(target, target)
        if env:
            env.domains[domain].process_field_xref(refnode)
        return refnode

#=============================================================================
# sphinx entrypoint
#=============================================================================
def setup(app):
    # don't apply our patch unless actually loaded by sphinx
    _patch_docfield()

    # identifies the version of our extension
    return {'version': __version__}

#=============================================================================
# eoc
#=============================================================================
