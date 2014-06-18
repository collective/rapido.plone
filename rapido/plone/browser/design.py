from zope import schema
from zope.interface.interface import Interface
from zope.interface import implements
from z3c.form import form, field, button
from z3c.form.interfaces import IFieldsForm
from plone.z3cform.layout import FormWrapper, wrap_form
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from rapido.plone import MessageFactory as _
from rapido.core.interfaces import IDatabase, IImporter, IExporter

class IDesignImportExportForm(Interface):
    """
    """
    path = schema.TextLine(title=_("Path"))


class DesignImportExportForm(form.Form):
    implements(IFieldsForm)

    fields = field.Fields(IDesignImportExportForm)
    ignoreContext = True

    @button.buttonAndHandler(_('import_button', default=u"Import"),
                             name='import')
    def handleImport(self, action):
        data, errors = self.extractData()
        if errors:
            return
        else:
            path = data.get('path', None)
            importer = IImporter(IDatabase(self.context)).import_from_fs(path)

    @button.buttonAndHandler(_('export_button', default=u"Export"),
                             name='export')
    def handleExport(self, action):
        data, errors = self.extractData()
        if errors:
            return
        else:
            path = data.get('path', None)
            exporter = IExporter(IDatabase(self.context)).export_to_fs(path)
            

class DesignImportExportFormWrapper(FormWrapper):

    form = DesignImportExportForm

layout = ViewPageTemplateFile("templates/design.pt")

import_export_design = wrap_form(
    DesignImportExportForm,
    __wrapper_class=DesignImportExportFormWrapper,
    index=layout,
    label=_(u"Import/export design"),
)
