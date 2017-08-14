# -*- coding: utf-8 -*-
import json
import Globals
import os.path
from plone.app.theming.interfaces import IThemeSettings
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getCurrentTheme
from plone.app.theming.utils import getTheme, createThemeFromTemplate
from plone.registry.interfaces import IRegistry
from plone.resource.interfaces import IResourceDirectory
from plone.resource.directory import FilesystemResourceDirectory
import unittest2 as unittest
from plone.testing.z2 import Browser
from zope.component import getUtility, provideUtility
from zope.publisher.browser import TestRequest

from rapido.plone.app import get_app
from rapido.plone.utils import getAvailableRapidoApps, getRapidoAppFromTheme
from rapido.plone.utils import cloneLocalRapidoApp
from rapido.plone.testing import RAPIDO_PLONE_FUNCTIONAL_TESTING

test_dir_path = os.path.dirname(__file__)


class FakeRequest(TestRequest):

    def physicalPathFromURL(self, url):
        return []


class TestCase(unittest.TestCase):

    layer = RAPIDO_PLONE_FUNCTIONAL_TESTING

    def setUp(self):
        # Enable debug mode always to ensure cache is disabled by default
        Globals.DevelopmentMode = True

        self.settings = getUtility(IRegistry).forInterface(IThemeSettings)
        self.settings.enabled = True
        
        
        test_theme_name = createThemeFromTemplate(title="rapidotest", description="Generated from test")
        theme = getTheme(test_theme_name)
        applyTheme(theme)

        import transaction
        transaction.commit()

        self.portal = self.layer['portal']
        package_dir_path = os.path.join(test_dir_path, 'other')
        dir = FilesystemResourceDirectory(package_dir_path)
        provideUtility(
            dir, provides=IResourceDirectory, name=u'++theme++other')
            
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False

    def tearDown(self):
        Globals.DevelopmentMode = False
    
    def test_rapido_apps_from_theme(self):
        apps = getRapidoAppFromTheme("rapido.plone.tests")
        self.assertEquals(apps, [u'otherapp', u'testapp'])
    
    def test_available_rapido_apps(self):
        themes = getAvailableRapidoApps(exclude_theme=getCurrentTheme())
        self.assertNotEquals(len(themes), 0)
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=list')
        self.assertEquals(json.loads(self.browser.contents), {'rapido.plone.tests': [u'otherapp', u'testapp']})
        self.assertEquals(json.loads(self.browser.contents), themes)
        
    def test_install_rapido_app_from_another_theme(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=rapidotest&app_id=testapp')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], False)
        apps = getRapidoAppFromTheme("rapidotest")
        self.assertEquals(apps, [u'testapp'])
        
    def test_install_rapido_app_from_invalid_theme(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.tests&destination_id=rapidotest&app_id=testapp')
        resp = json.loads(self.browser.contents)
        self.assertNotEquals(resp["error"], False)
        
    def test_install_invalid_rapido_app_from_theme(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=rapidotest&app_id=test')
        resp = json.loads(self.browser.contents)
        self.assertNotEquals(resp["error"], False)
        
    def test_install_rapido_app_in_invalid_theme(self):
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=rapidot&app_id=testapp')
        resp = json.loads(self.browser.contents)
        self.assertNotEquals(resp["error"], False)
