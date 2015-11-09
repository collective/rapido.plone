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
import requests
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
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def tearDown(self):
        Globals.DevelopmentMode = False

    def test_view(self):
        response = requests.get(
            self.portal.absolute_url() + '/@@rapido/view/whatever',
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertTrue("This is the theme" in response.text)

    def test_refresh(self):
        response = requests.get(
            self.portal.absolute_url() + '/@@rapido/testdb/refresh',
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertTrue("Refreshed" in response.text)

    def test_json_refresh_no_token(self):
        response = requests.post(
            self.portal.absolute_url() + '/@@rapido/testdb/refresh',
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEquals(response.json()['error'],
            u'Form authenticator is invalid.')

    def test_json_refresh(self):
        response = requests.get(
            self.portal.absolute_url() + '/@@rapido/testdb',
            headers={'Accept': 'application/json'},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertTrue('x-csrf-token' in response.headers)
        token = response.headers['x-csrf-token']
        response = requests.post(
            self.portal.absolute_url() + '/@@rapido/testdb/refresh',
            headers={
                'Accept': 'application/json',
                'x-csrf-token': token
            },
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        )
        self.assertEquals(response.json()['success'], u'refresh')
