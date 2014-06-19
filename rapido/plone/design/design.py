from zope import schema
from zope.interface.interface import Interface
from zope.interface import implements
from z3c.form import form, field, button
from z3c.form.interfaces import IFieldsForm
from plone.z3cform.layout import FormWrapper, wrap_form
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from rapido.plone import MessageFactory as _
from rapido.core.interfaces import IDatabase, IImporter, IExporter

class IDesignImportExportForm(Interface):
    """
    """
    path = schema.TextLine(title=_("Path"))

    watch = schema.Bool(title=_("Watch folder"),
        required=False,
        )


class DesignImportExportForm(form.Form):
    implements(IFieldsForm)

    fields = field.Fields(IDesignImportExportForm)
    ignoreContext = True

    def updateWidgets(self):
        super(form.Form, self).updateWidgets()
        watch_path = self.context.get_watcher()
        if watch_path:
            self.widgets['path'].value = watch_path
            self.widgets['watch'].value = ['selected']

    @button.buttonAndHandler(_('import_button', default=u"Import"),
                             name='import')
    def handleImport(self, action):
        data, errors = self.extractData()
        if errors:
            return
        else:
            path = data.get('path', None)
            importer = IImporter(IDatabase(self.context)).import_from_fs(path)
            if data.get('watch'):
                self.context.set_watcher(path)
            else:
                self.context.set_watcher(None)

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


class RefreshDesign(BrowserView):

    def __call__(self):
        if IDatabase.implementedBy(self.context):
            db = self.context
        else:
            db = self.context.getParentDatabase()
        path = db.get_watcher()
        if path:
            IImporter(IDatabase(db)).import_from_fs(path)
