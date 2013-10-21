import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import rapido.plone

OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
               doctest.ELLIPSIS

ptc.setupPloneSite(products=['rapido.plone'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml',
              rapido.plone)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='rapido.plone',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='rapido.plone.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'INTEGRATION.txt',
            package='rapido.plone',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

        # -*- extra stuff goes here -*-

        # Integration tests for Column
        ztc.ZopeDocFileSuite(
            'Column.txt',
            package='rapido.plone',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Field
        ztc.ZopeDocFileSuite(
            'Field.txt',
            package='rapido.plone',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for View
        ztc.ZopeDocFileSuite(
            'View.txt',
            package='rapido.plone',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Form
        ztc.ZopeDocFileSuite(
            'Form.txt',
            package='rapido.plone',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Database
        ztc.ZopeDocFileSuite(
            'Database.txt',
            package='rapido.plone',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),



if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
