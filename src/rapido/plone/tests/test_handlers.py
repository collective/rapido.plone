# -*- coding: utf-8 -*-
import Globals
import os.path
from plone.app.theming.interfaces import IThemeSettings
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
from plone.registry.interfaces import IRegistry
from plone.resource.interfaces import IResourceDirectory
from plone.resource.directory import FilesystemResourceDirectory
from plone.resourceeditor.browser import FileManager
import unittest2 as unittest
from zExceptions import NotFound
from zope.component import getUtility, provideUtility
from zope.publisher.browser import TestRequest

from rapido.plone.app import get_app
from rapido.plone.handlers import is_yaml
from rapido.plone.testing import RAPIDO_PLONE_FUNCTIONAL_TESTING

test_dir_path = os.path.dirname(__file__)


class FakeRequest(TestRequest):

    def physicalPathFromURL(self, url):
        return []


class TestCase(unittest.TestCase):

    layer = RAPIDO_PLONE_FUNCTIONAL_TESTING

    def _make_directory(self, resourcetype='theme', resourcename='mytheme'):
        from plone.resource.interfaces import IResourceDirectory
        from zope.component import getUtility

        resources = getUtility(IResourceDirectory, name='persistent')
        resources.makeDirectory(resourcetype)
        resources[resourcetype].makeDirectory(resourcename)

        return resources[resourcetype][resourcename]

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

    def test_is_yaml(self):
        request = FakeRequest()
        app = get_app('testapp', request)
        blocks = app.context.resources['blocks']
        self.assertTrue(is_yaml(blocks['action.yaml']))
        self.assertFalse(is_yaml(blocks['action.html']))
        with self.assertRaises(NotFound) as context:
            is_yaml(blocks['action.txt'])

    def test_resource_created_or_modified(self):
        request = FakeRequest()
        r = self._make_directory()
        view = FileManager(r, request)
        info = view.addNew('/', 'test_tile.yaml')
        self.assertEqual(info['code'], 0)
        self.assertEqual(info['error'], '')
        self.assertEqual(info['name'], 'test_tile.yaml')
        self.assertEqual(info['parent'], '/')
        self.assertEqual(r.readFile('test_tile.yaml'), '')
