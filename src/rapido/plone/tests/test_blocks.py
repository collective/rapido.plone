# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from plone.app.testing import (
    TEST_USER_ID,
    TEST_USER_PASSWORD,
    SITE_OWNER_NAME,
    SITE_OWNER_PASSWORD,
)
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
        self.browser.handleErrors = False

    def tearDown(self):
        Globals.DevelopmentMode = False

    def test_static_block(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/otherapp/block/purehtml')
        self.assertTrue("""<p>Hello, I am static</p>"""
            in self.browser.contents)

    def test_traverse_to_content(self):
        self.browser.open(
            self.portal.absolute_url() +
            '/sendto_form/@@rapido/otherapp/block/purehtml')
        self.assertTrue("""<p>Hello, I am static</p>"""
            in self.browser.contents)

    def test_block_with_basic_element(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/block/basic')
        self.assertTrue("""<span>How simple is it? Very simple!</span>"""
            in self.browser.contents)

    def test_block_with_text_element(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/block/text')
        self.assertTrue('<span>How simple is it? <input type="text"\n'
            '        name="answer" value="" /></span>'
            in self.browser.contents)

    def test_block_with_action_element(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/block/action')
        self.assertTrue("""<span>Quote is: No quote</span>"""
            in self.browser.contents)
        self.assertTrue('<input type="submit"\n        name="action.create"'
            ' value="Create a quote" />'
            in self.browser.contents)
        self.browser.getControl('Create a quote').click()
        self.assertTrue('<span>Quote is: Knowledge is power, France is bacon.'
            '</span>'
            in self.browser.contents)

    def test_log(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/_log')
        self.assertEquals(self.browser.contents, '[]')
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/block/action')
        self.browser.getControl('Make an error').click()
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/_log')
        self.assertEquals(self.browser.contents, '["Rapido execution error - '
            'testapp:\\n   \'Context\' object has no attribute \'wrong\'\\n'
            '   File \\"action.py\\", line 16, in boom"]')

    def test_save_anonymous(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/block/book')
        self.assertRaises(
            Unauthorized,
            self.browser.getControl('Save').click,
        )

    def test_save_not_author(self):
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (TEST_USER_ID, TEST_USER_PASSWORD,)
        )
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/block/book')
        self.assertRaises(
            Unauthorized,
            self.browser.getControl('Save').click,
        )

    def test_save(self):
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/block/book')
        self.browser.getControl(name='author').value = u"Victor Hugo"
        self.browser.getControl('Save').click()
        self.assertTrue("Victor Hugo" in self.browser.contents)
