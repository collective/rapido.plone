from five import grok

from z3c.form import field, form, button
from zope import schema
from zope.interface import invariant, Invalid, Interface, implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.z3cform.layout import wrap_form, FormWrapper

from rapido.core import interfaces as core
from rapido.plone import MessageFactory as _
from rapido.plone.form import IForm

grok.context(IForm)

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