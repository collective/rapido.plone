from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from rapido.core.browser import views as core

class OpenForm(core.OpenForm):

    template = ViewPageTemplateFile('templates/openform.pt')

class DocumentView(core.DocumentView):

    view_template = ViewPageTemplateFile('templates/opendocument.pt')
    edit_template = ViewPageTemplateFile('templates/editdocument.pt')

class AllDocumentsView(core.AllDocumentsView):

    template = ViewPageTemplateFile('templates/documents.pt')