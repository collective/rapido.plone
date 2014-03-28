from five import grok
from zope import schema

from plone.dexterity.content import Container
from plone.directives import dexterity, form

from rapido.plone import MessageFactory as _


class IRule(form.Schema):
    """
    Rule
    """

    id = schema.TextLine(
        title=_("Id"),
        required=True
        )

    code = schema.Text(
        title=_("Code"),
        required=False,
        )


class Rule(Container):
    grok.implements(IRule)

    meta_type = "Rapido rule"
