from five import grok

from z3c.form import field
from zope import schema

from plone.dexterity.content import Container
from plone.directives import dexterity, form

from rapido.plone import MessageFactory as _


class IAction(form.Schema):
    """
    Action
    """

    id = schema.TextLine(
        title=_("Id"),
        required=True
        )


class Action(Container):
    grok.implements(IAction)

    meta_type = "Rapido action"
