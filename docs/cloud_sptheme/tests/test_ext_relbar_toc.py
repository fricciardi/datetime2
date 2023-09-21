"""
cloud_sptheme.tests -- test relbar_toc extension
"""
#=============================================================================
# imports
#=============================================================================
# core
from __future__ import absolute_import, division, print_function
import logging
log = logging.getLogger(__name__)
import os
# site
import mock
# pkg
from .utils import TestCase, unittest
# subject
from cloud_sptheme.ext import relbar_links
# local
__all__ = [
]

#=============================================================================
# extension test
#=============================================================================

# root_dir = os.path.abspath(os.path.join(__file__, *[".."]*3))
# docs_dir = os.path.join(root_dir, "docs")

# TODO: would like to test extensions *actual* behavior with sphinx,
#       and/or test our assumptions about format of ctx & ctx['rellinks'].
#       Have idea of running integration test by running sphinx,
#       and building either our docs, or some "test" docs;
#       and then examining the output.  not sure best way to approach
#       that though.
# from sphinx import main
# target_dir = self.makeTempDir()
# self.assertFalse(main(["sphinx", "-b", "html", "-E", docs_dir, target_dir]))

#=============================================================================
# utils tests
#=============================================================================
class UtilsTestCase(TestCase):

    def setUp(self):
        super(UtilsTestCase, self).setUp()

        # patch sphinx's _() to be noop
        patch = mock.patch.object(relbar_links, "_", side_effect=lambda s: s)
        self.addCleanup(patch.__exit__)
        patch.__enter__()

    def test_insert_no_links(self):
        """
        test insert hooks -- with no links present (e.g. json builder)
        """
        from cloud_sptheme.ext.relbar_links import insert_relbar_links
        app = mock.Mock()
        insert_relbar_links(app, None, None, {}, None)

    def test_insert_default(self):
        """
        test insert hooks -- with default links
        """
        from cloud_sptheme.ext.relbar_links import insert_relbar_links
        app = mock.Mock()
        app.config.master_doc = "test-contents"
        app.config.relbar_links = ["toc"]
        app.config.relbar_links_after = ["next", "previous"]
        links = [
            ("genindex", "General Index", "I", "genidx"),
            ("next-test-page", "Next Page", "N", "next"),
            ("previous-test-page", "Previous Page", "P", "previous"),
        ]
        insert_relbar_links(app, None, None, dict(rellinks=links), None)
        self.assertEqual(links, [
            ("genindex", "General Index", "I", "genidx"),
            ("test-contents", "Table Of Contents", "C", "toc"),
            ("next-test-page", "Next Page", "N", "next"),
            ("previous-test-page", "Previous Page", "P", "previous"),
        ])

    def test_insert_custom(self):
        """
        test insert hooks -- with custom links
        """
        from cloud_sptheme.ext.relbar_links import insert_relbar_links
        app = mock.Mock()
        app.config.relbar_links = [dict(page="my-page", label="my page")]
        app.config.relbar_links_after = ["previous"]
        links = [
            ("genindex", "General Index", "I", "genidx"),
            ("next-test-page", "Next Page", "N", "next"),
            ("previous-test-page", "Previous Page", "P", "previous"),
        ]
        insert_relbar_links(app, None, None, dict(rellinks=links), None)
        self.assertEqual(links, [
            ("genindex", "General Index", "I", "genidx"),
            ("next-test-page", "Next Page", "N", "next"),
            ("my-page", "my page", None, "my page"),
            ("previous-test-page", "Previous Page", "P", "previous"),
        ])

    def test_parse_entry(self):
        """
        test parse_entry() helper
        """
        from cloud_sptheme.ext.relbar_links import parse_entry
        app = mock.Mock()
        app.config.master_doc = "test-master-doc"

        #
        # dicts
        #
        self.assertRaises(ValueError, parse_entry, app, dict())

        self.assertRaises(ValueError, parse_entry, app, dict(page="page"))

        self.assertRaises(ValueError, parse_entry, app, dict(label="label"))

        self.assertEqual(parse_entry(app, dict(page="page", label="label")),
                         ("page", "label", None, "label"))

        self.assertEqual(parse_entry(app, dict(page="page", title="title", key="key", label="label")),
                         ("page", "title", "key", "label"))

        #
        # tuples
        #
        self.assertRaises(ValueError, parse_entry, app, ())

        self.assertRaises(ValueError, parse_entry, app, ("a",))

        self.assertEqual(parse_entry(app, ("page", "label")),
                         ("page", "label", None, "label"))

        self.assertRaises(ValueError, parse_entry, app, ("a", "b", "c"))

        self.assertEqual(parse_entry(app, ("page", "title", "key", "label")),
                         ("page", "title", "key", "label"))

        #
        # other
        #
        self.assertEqual(parse_entry(app, "toc"),
                         ("test-master-doc", "Table Of Contents", "C", "toc"))

#=============================================================================
# eof
#=============================================================================

