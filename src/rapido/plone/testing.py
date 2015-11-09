# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig


class RapidoPloneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import rapido.plone.tests
        xmlconfig.file(
            'configure.zcml',
            rapido.plone.tests,
            context=configurationContext
        )
        # Run the startup hook
        from plone.app.theming.plugins.hooks import onStartup
        onStartup(None)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'rapido.plone:default')


RAPIDO_PLONE_FIXTURE = RapidoPloneLayer()


RAPIDO_PLONE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RAPIDO_PLONE_FIXTURE,),
    name='RapidoPloneLayer:IntegrationTesting'
)


RAPIDO_PLONE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RAPIDO_PLONE_FIXTURE, z2.ZSERVER_FIXTURE),
    name='RapidoPloneLayer:FunctionalTesting'
)


RAPIDO_PLONE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        RAPIDO_PLONE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='RapidoPloneLayer:AcceptanceTesting'
)
