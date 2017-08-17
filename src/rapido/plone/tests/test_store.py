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
        
        
        createThemeFromTemplate(title="linked", description="Generated from test")
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
        """ Test the list of rapido apps found in the rapido.plone.tests theme."""
        apps = getRapidoAppFromTheme("rapido.plone.tests")
        self.assertEquals(apps, [u'otherapp', u'testapp'])
    
    def test_available_rapido_apps(self):
        """ Test the list of rapido apps per theme."""
        themes = getAvailableRapidoApps(exclude_theme=getCurrentTheme())
        self.assertNotEquals(len(themes), 0)
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=list')
        self.assertEquals(json.loads(self.browser.contents), themes)
        
    def test_install_rapido_app_from_another_theme(self):
        """ Test the installation of a rapido app from another theme inside the given theme."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=rapidotest&app_id=testapp')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], False)
        apps = getRapidoAppFromTheme("rapidotest")
        self.assertEquals(apps, [u'testapp'])
        
    def test_install_rapido_app_from_invalid_theme(self):
        """ Test if an error will be thrown when an invalid theme is given."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.tests&destination_id=rapidotest&app_id=testapp')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], "rapido.tests theme not found")
        
    def test_no_source_theme(self):
        """ Test if an error will be thrown if no source theme is given."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&destination_id=rapidotest&app_id=testapp')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], "No theme id was given")
        
    def test_no_rapido_app_id(self):
        """ Test if an error will be thrown if no rapido app id is given."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.tests&destination_id=rapidotest')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], "No app id was given")
        
    def test_install_invalid_rapido_app_from_theme(self):
        """ Test if an error will be thrown when an invalid rapido app is given for the source theme."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=rapidotest&app_id=test')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], "test rapido app is not found in rapido.plone.tests theme")
        
    def test_install_rapido_app_in_invalid_theme(self):
        """ Test if an error will be thrown when installing a rapido app from another theme to an invalid theme."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=rapidot&app_id=testapp')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], "rapidot theme not found")
        
    def test_install_rapido_app_from_another_theme_twice(self):
        """ Test if a rapido app can be installed twice."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=rapidotest&app_id=testapp')
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=rapidotest&app_id=testapp')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], "A rapido app with testapp id already exists in rapidotest")

    def test_install_rapido_app_from_another_theme_link(self):
        """ Test if a rapido app can be installed by using reference to another theme."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=linked&app_id=testapp&make_link=1')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], False)

    def test_install_rapido_app_from_another_theme_with_make_link_false(self):
        """ Test if a rapido app can be installed by using reference to another theme."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=linked&app_id=testapp&make_link=0')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], False)

    def test_install_linked_rapido_app_from_another_theme(self):
        """ Test if a referenced rapido app can be installed from another theme."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=linked&app_id=testapp&make_link=1')
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=linked&destination_id=rapidotest&app_id=testapp')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], False)

    def test_install_linked_rapido_app_from_another_them_linked(self):
        """ Test if a referenced rapido app can be installed by using reference from another theme."""
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=rapido.plone.tests&destination_id=linked&app_id=testapp&make_link=1')
        self.browser.open(
            self.portal.absolute_url() + '/@@rapido-store-api?action=import&source_id=linked&destination_id=rapidotest&app_id=testapp&make_link=1')
        resp = json.loads(self.browser.contents)
        self.assertEquals(resp["error"], False)
