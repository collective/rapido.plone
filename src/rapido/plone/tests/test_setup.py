# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from rapido.plone.testing import RAPIDO_PLONE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that rapido.plone is properly installed."""

    layer = RAPIDO_PLONE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if rapido.plone is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('rapido.plone'))

    def test_uninstall(self):
        """Test if rapido.plone is cleanly uninstalled."""
        self.installer.uninstallProducts(['rapido.plone'])
        self.assertFalse(self.installer.isProductInstalled('rapido.plone'))
