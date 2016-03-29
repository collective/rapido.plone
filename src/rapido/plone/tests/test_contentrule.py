import Globals
from plone.app.contentrules.rule import Rule
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.theming.interfaces import IThemeSettings
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IExecutable
from plone.registry.interfaces import IRegistry
from Products.statusmessages import STATUSMESSAGEKEY
from Products.statusmessages.adapter import _decodeCookieValue
import unittest2 as unittest
from zope.component import getUtility, getMultiAdapter
from zope.interface import implements, Interface

from rapido.plone.contentrule.action import Action, EditFormView
from rapido.plone.testing import RAPIDO_PLONE_FUNCTIONAL_TESTING


class DummyEvent(object):
    implements(Interface)

    def __init__(self, obj):
        self.object = obj


class TestRapidoAction(unittest.TestCase):

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
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def testRegistered(self):
        element = getUtility(IRuleAction, name='rapido.plone.Action')
        self.assertEqual('rapido.plone.Action', element.addview)
        self.assertEqual('edit', element.editview)

    def testInvokeAddView(self):
        element = getUtility(IRuleAction, name='rapido.plone.Action')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.request), name='+action')
        addview = getMultiAdapter((adding, self.request), name=element.addview)

        addview.form_instance.update()
        content = addview.form_instance.create(data={
            'app': 'testapp',
            'block': 'rule',
            'method': 'hello',
        })
        addview.form_instance.add(content)

        e = rule.actions[0]
        self.assertTrue(isinstance(e, Action))
        self.assertEqual('testapp', e.app)
        self.assertEqual(e.summary,
            u'Call Rapido method hello from testapp/rule')

    def testInvokeEditView(self):
        element = getUtility(IRuleAction, name='rapido.plone.Action')
        e = Action()
        editview = getMultiAdapter((e, self.request), name=element.editview)
        self.assertTrue(isinstance(editview, EditFormView))

    def testExecute(self):
        e = Action()
        e.app = 'testapp'
        e.block = 'rule'
        e.method = 'hello'

        ex = getMultiAdapter(
            (self.portal, e, DummyEvent(self.portal)), IExecutable)
        self.assertEqual(True, ex())

    def testNotFound(self):
        e = Action()
        e.app = 'badapp'
        e.block = 'rule'
        e.method = 'hello'

        ex = getMultiAdapter(
            (self.portal, e, DummyEvent(self.portal)), IExecutable)
        ex()
        new_cookies = self.request.RESPONSE.cookies[STATUSMESSAGEKEY]
        messages = _decodeCookieValue(new_cookies['value'])
        self.assertEquals(messages[0].message,
            u'Rapido application badapp cannot be found.')
