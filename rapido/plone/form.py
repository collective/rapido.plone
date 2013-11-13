from five import grok

from z3c.form import group, field, form, button
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.app.textfield import RichText
from plone.app.z3cform.layout import wrap_form, FormWrapper

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

grok.context(IForm)

class Form(Container):
    grok.implements(IForm, core.IFormable)

    code = u"# your code here"

class IFormCode(Interface):

    code = schema.Text(
        title=_("Code"),
        required=False,
        )

class FormContext(object):
    implements(IFormCode)

class EditFormCode(form.Form):
    implements(IFormCode)

    fields = field.Fields(IFormCode)
    
    def getContent(self):
        obj = FormContext()
        obj.code = core.IForm(self.context).code
        return obj

    @button.buttonAndHandler(u'Apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            return
        core.IForm(self.context).set_code(data['code'])
        self.status = _("Code saved")

class EditFormCodeWrapper(FormWrapper):

    def update(self):
        FormWrapper.update(self)

edit_code_layout = ViewPageTemplateFile("templates/form_edit_code.pt")

edit_form_code_view_class = wrap_form(
    EditFormCode,
    __wrapper_class=EditFormCodeWrapper,
    index=edit_code_layout,
    label=u"Form code"
)

