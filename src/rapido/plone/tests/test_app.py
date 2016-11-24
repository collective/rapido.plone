# -*- coding: utf-8 -*-
import Globals
import os.path
from plone.app.theming.interfaces import IThemeSettings
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
from plone.registry.interfaces import IRegistry
from plone.resource.interfaces import IResourceDirectory
from plone.resource.directory import FilesystemResourceDirectory
import unittest2 as unittest
from zope.component import getUtility, provideUtility
from zope.publisher.browser import TestRequest

from rapido.plone.app import get_app
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
        theme = getTheme('rapido.plone.tests')
        applyTheme(theme)

        import transaction
        transaction.commit()

        self.portal = self.layer['portal']
        package_dir_path = os.path.join(test_dir_path, 'other')
        dir = FilesystemResourceDirectory(package_dir_path)
        provideUtility(
            dir, provides=IResourceDirectory, name=u'++theme++other')

    def tearDown(self):
        Globals.DevelopmentMode = False

    def test_app_url(self):
        request = FakeRequest()
        app = get_app('testapp', request)
        self.assertEquals(app.url,
                          'http://localhost:55001/plone/@@rapido/testapp')

    def test_get_app_from_non_active_theme(self):
        request = FakeRequest()
        app = get_app('app2', request)
        self.assertTrue("""<strong>Hello!!!</strong>"""
                        in app.get_block('hello').display())
