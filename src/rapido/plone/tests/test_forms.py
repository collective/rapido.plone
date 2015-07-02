# -*- coding: utf-8 -*-
from plone.app.theming.interfaces import IThemeSettings
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
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
        self.browser = Browser(self.layer['app'])

    def tearDown(self):
        Globals.DevelopmentMode = False

    def test_form_with_basic_field(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testdb/form/basic')
        self.assertTrue("""<span>How simple is it? Very simple!</span>"""
            in self.browser.contents)

    def test_form_with_text_field(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testdb/form/text')
        self.assertTrue("""<span>How simple is it? <input type="text"\n        name="answer" value="" /></span>"""
            in self.browser.contents)

    def test_form_with_action_field(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testdb/form/action')
        self.assertTrue("""<span>Quote is: No quote</span>"""
            in self.browser.contents)
        self.assertTrue("""<input type="submit"\n        name="action.create" value="Create a quote" />"""
            in self.browser.contents)
        self.browser.getControl('Create a quote').click()
        self.assertTrue("""<span>Quote is: Knowledge is power, France is bacon.</span>"""
            in self.browser.contents)
