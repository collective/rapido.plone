# -*- coding: utf-8 -*-
from plone.app.theming.interfaces import IThemeSettings
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from zope.component import getUtility
import Globals
import unittest2 as unittest

from rapido.plone.testing import RAPIDO_PLONE_FUNCTIONAL_TESTING


class TestCase(unittest.TestCase):

    layer = RAPIDO_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        # Enable debug mode always to ensure cache is disabled by default
        Globals.DevelopmentMode = True

        self.settings = getUtility(IRegistry).forInterface(IThemeSettings)
        self.settings.enabled = True
        theme = getTheme('rapido.plone.tests')
        applyTheme(theme)

        import transaction
        transaction.commit()

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def tearDown(self):
        Globals.DevelopmentMode = False

    def test_view(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/view/whatever')
        self.assertTrue("This is the theme" in self.browser.contents)

    def test_path_from_parent_request(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/view/anything/testapp/blocks/basic')
        self.assertTrue("How simple is it" in self.browser.contents)

    def test_refresh(self):
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/refresh')
        self.assertTrue("Refreshed" in self.browser.contents)
