# -*- coding: utf-8 -*-
import Globals
from plone.app.theming.interfaces import IThemeSettings
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
from plone.registry.interfaces import IRegistry
import unittest2 as unittest
from zope.component import getUtility
from zope.publisher.browser import TestRequest

from rapido.plone.app import get_app
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

    def tearDown(self):
        Globals.DevelopmentMode = False

    def test_app_url(self):
        request = TestRequest()
        app = get_app('testapp', request)
        self.assertEquals(app.url,
            'http://localhost:55001/plone/@@rapido/testapp')
