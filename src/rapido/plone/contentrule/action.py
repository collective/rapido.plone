from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules.actions import ActionAddForm, ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope.component import adapts
from zope.interface import implements, Interface
from zope import schema

from rapido.core.exceptions import NotFound
from rapido.plone import _
from rapido.plone.app import get_app


class IAction(Interface):
    """Interface for the configurable aspects of a rapido action.

    This is also used to create add and edit forms, below.
    """

    app = schema.TextLine(title=_(u"Rapido application"),
        description=_(u"The targeted Rapido application."),
        required=True)

    block = schema.TextLine(title=_(u"Block"),
        description=_(u"The block providing the method."),
        required=True)

    method = schema.TextLine(title=_(u"Method"),
        description=_(u"The name of the method to execute."),
        required=True)


class Action(SimpleItem):
    """The actual persistent implementation of the action element.
    """
    implements(IAction, IRuleElementData)

    app = ''
    block = ''
    method = ''

    element = 'rapido.plone.Action'

    @property
    def summary(self):
        return _(u"Call Rapido method %s from %s/%s" % (
            self.method, self.app, self.block))


class ActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        request = self.context.REQUEST
        try:
            app = get_app(self.element.app, request, content=self.event.object)
        except NotFound:
            api.portal.show_message(
                message="Rapido application %s cannot be found." % (
                    self.element.app,),
                request=request,
                type='error',
            )
            return True
        block = app.get_block(self.element.block)
        block.compute_element(self.element.method, {'block': block})
        return True


class AddForm(ActionAddForm):
    """An add form for rapido action.
    """
    schema = IAction
    label = _(u"Add Rapido Action")
    description = _(u"A Rapido action executes a Rapido method.")
    form_name = _(u"Configure element")
    Type = Action


class AddFormView(ContentRuleFormWrapper):
    form = AddForm


class EditForm(ActionEditForm):
    """An edit form for rapido action.
    """
    schema = IAction
    label = _(u"Edit Rapido Action")
    description = _(u"A Rapido action executes a Rapido method.")
    form_name = _(u"Configure element")


class EditFormView(ContentRuleFormWrapper):
    form = EditForm
