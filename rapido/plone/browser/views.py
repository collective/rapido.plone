from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from rapido.core.interfaces import IForm, IDatabase


class OpenDatabase(BrowserView):

    template = ViewPageTemplateFile('templates/opendatabase.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.db = IDatabase(self.context)

    def __call__(self):
        return self.template()


class OpenForm(BrowserView):

    template = ViewPageTemplateFile('templates/openform.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.form = IForm(context)
        self.api = self.form.database.url + '/api/form/' + self.form.id
        self.body = self.form.display(edit=True)

    def __call__(self):
        return self.template()


class CreateDocument(BrowserView):

    def __call__(self):
        form = IForm(self.context)
        doc = form.database.create_document()
        doc.set_item('Form', form.id)
        doc.save(self.request, form=form, creation=True)
        self.request.response.redirect(doc.url)


class DocumentView(BrowserView):
    implements(IPublishTraverse)

    view_template = ViewPageTemplateFile('templates/opendocument.pt')
    edit_template = ViewPageTemplateFile('templates/editdocument.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.doc = None
        self.edit_mode = False

    def publishTraverse(self, request, name):
        if name == "edit":
            self.edit_mode = True
            return self
        if name == "save":
            self.doc.save(self.request)
            return self

        doc = IDatabase(self.context).get_document(name)
        if not doc:
            raise NotFound(self, name, request)
        self.doc = doc
        return self

    def render(self):

        if self.edit_mode:
            self.body = self.doc.display(edit=True)
            return self.edit_template()
        else:
            self.body = self.doc.display()
            return self.view_template()

    def __call__(self):
        return self.render()


class AllDocumentsView(BrowserView):

    template = ViewPageTemplateFile('templates/documents.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.documents = IDatabase(self.context)._documents()

    def __call__(self):
        return self.template()