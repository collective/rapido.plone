# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
import json
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
import zExceptions
from zope.component import getUtility
import Globals
import unittest2 as unittest

from rapido.core.exceptions import ExecutionError
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
        self.browser.raiseHttpErrors = False

    def tearDown(self):
        Globals.DevelopmentMode = False

    def test_static_block(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/otherapp/blocks/purehtml')
        self.assertTrue("""<p>Hello, I am static</p>"""
            in self.browser.contents)

    def test_traverse_to_content(self):
        self.browser.open(
            self.portal.absolute_url() +
            '/sendto_form/@@rapido/otherapp/blocks/purehtml')
        self.assertTrue("""<p>Hello, I am static</p>"""
            in self.browser.contents)

    def test_block_with_basic_element(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/basic')
        self.assertTrue("""<span>How simple is it? Very simple!</span>"""
            in self.browser.contents)

    def test_block_with_text_element(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/text')
        self.assertTrue('<span>How simple is it? <input type="text"\n'
            '        name="answer" value="" /></span>'
            in self.browser.contents)

    def test_block_with_action_element(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/action')
        self.assertTrue("""<span>Quote is: No quote</span>"""
            in self.browser.contents)
        self.assertTrue('<input type="submit"\n        name="action.create"'
            ' value="Create a quote" />'
            in self.browser.contents)
        self.browser.getControl('Create a quote').click()
        self.assertTrue('<span>Quote is: Knowledge is power, France is bacon.'
            '</span>'
            in self.browser.contents)

    def test_error(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/_log')
        self.assertEquals(self.browser.contents, '[]')
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/action')
        self.assertRaises(
            ExecutionError,
            self.browser.getControl('Make an error').click
        )

    def test_log(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/_log')
        self.assertEquals(self.browser.contents, '[]')
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/action')
        self.browser.getControl('Write a log').click()
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/_log')
        messages = json.loads(self.browser.contents)
        self.assertEquals(messages[0], "Hello!")
        self.assertEquals(messages[1], [1, 2, {"a": 3}])
        self.assertTrue("_not_serializable" in messages[2])

    def test_save_anonymous(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/book')
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
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/book')
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
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/book')
        self.browser.getControl(name='author').value = u"Victor Hugo"
        self.browser.getControl('Save').click()
        self.assertTrue("Victor Hugo" in self.browser.contents)

    def test_plone_security_anonymous(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/action')
        self.assertRaises(
            ExecutionError,
            self.browser.getControl('Create a content').click
        )
        self.assertTrue('my-content' not in self.portal.objectIds())

    def test_plone_security_member(self):
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (TEST_USER_ID, TEST_USER_PASSWORD,)
        )
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/action')
        self.assertRaises(
            ExecutionError,
            self.browser.getControl('Create a content').click
        )
        self.assertTrue('my-content' not in self.portal.objectIds())

    def test_plone_security_manager(self):
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/action')
        if "Confirm action" in self.browser.contents:
            self.browser.getControl('Confirm action').click()
        self.browser.getControl('Create a content').click()
        self.assertTrue('my-content' in self.portal.objectIds())

    def test_pt_template(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/knowledge')
        self.assertTrue('<p>Knowledge is power</p>\n<ul><li>France is bacon'
            '</li>\n<li>Francis Bacon</li></ul>\n<a href="http://localhost:'
            '55001/plone/@@rapido/testapp/blocks/knowledge">Home</a>'
            in self.browser.contents)

    def test_bad_pt_template(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/bad')
        self.assertTrue('Rendering error\n - Expression: "boom/jokes"\n'
            ' - Location:   (line 2: col 25)' in self.browser.contents)

    def test_missing_template(self):
        try:
            self.browser.open(
                self.portal.absolute_url() + '/@@rapido/testapp/blocks/oops')
        except Exception, e:
            self.assertTrue(type(e) is zExceptions.NotFound)
        else:
            self.fail("Missing template should produce a NotFound exception.")

    def test_call(self):
        self.assertEquals(
            self.portal.restrictedTraverse('@@rapido-call')(
                'testapp/call/call_me', x=7, y=6),
            42
        )

    def test_access_other_app(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/otherapp')
        self.assertTrue('Records=1' in self.browser.contents)
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido/testapp/blocks/otherapp')
        self.assertTrue('Records=2' in self.browser.contents)

    def test_block_can_be_a_view(self):
        self.browser.open(
            self.portal.absolute_url() + '/my-view')
        self.assertTrue("""And now for something completely different"""
            in self.browser.contents)

    def test_block_view_with_theme(self):
        self.browser.open(
            self.portal.absolute_url() + '/my-view2')
        self.assertTrue("""And now for something completely different"""
                        in self.browser.contents)
        self.assertTrue("""<div id="content-core">"""
                        in self.browser.contents)
        self.browser.open(
            self.portal.absolute_url() + '/my-view')
        self.assertFalse("""<div id="content-core">"""
                         in self.browser.contents)
