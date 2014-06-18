from zope import schema
from five import grok
from plone.directives import form
from plone.dexterity.content import Container
from plone.app.textfield import RichText
from plone.namedfile.interfaces import IImageScaleTraversable

from rapido.core import interfaces as core
from rapido.plone import MessageFactory as _

class IForm(form.Schema, IImageScaleTraversable):
    """
    Form
    """

    id = schema.TextLine(
        title=_("Id"),
        required=True
        )
    
    html = RichText(
            title=_("Layout"),
            default_mime_type='text/html',
            output_mime_type='text/html',
            required=False,
        )

    assigned_rules = schema.List(
        title=_('Assigned rules'),
        value_type=schema.Choice(vocabulary="rapido.plone.rules"),
        required=False,
    )

class Form(Container):
    grok.implements(IForm, core.IFormable)

    meta_type = "Rapido form"

    code = u"# your code here"