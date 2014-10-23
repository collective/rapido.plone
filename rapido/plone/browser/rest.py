import json
from zope.interface import implements
from Products.Five.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound

from rapido.core.interfaces import IDatabase

class Api(BrowserView):
    implements(IPublishTraverse)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.db = IDatabase(self.context)
        self.query = None
        self.method = self.request.method
        self.doc = None
        self.form = None
        self.error = None

    def json_response(self, result):
        self.request.response.setHeader("Content-Type", "application/json")
        return json.dumps(result)

    def publishTraverse(self, request, name):
        if self.method == "GET" and name == "_search":
            self.query = name
            return self
        if self.method == "POST" and name in ["_update", "_create", "_delete"]:
            self.query = name
            return self
        if self.method == "GET" and name == "form":
            self.query = name
            return self

        if self.query == 'form':
            form = self.db.get_form(name)
            if not form:
                raise NotFound(self, name, request)
            self.form = form
            return self

        doc = self.db.get_document(name)
        if not doc:
            raise NotFound(self, name, request)
        self.doc = doc
        return self

    def render(self):
        try:
            if self.method == "GET" and not self.query:
                return self.json_response(self.doc.items())
            elif self.method == "PUT" or (self.method == "POST" and self.query == "_create"):
                return self.json_response({'error': 'Not implemented'})
            elif self.method == "DELETE" or (self.method == "POST" and self.query == "_delete"):
                self.db.delete_document(doc=self.doc)
                return self.json_response({'success': 'deleted'})
            elif self.method == "PATCH" or (self.method == "POST" and self.query == "_update"):
                return self.json_response({'error': 'Not implemented'})
            elif self.method == "GET" and self.query == "form":
                return self.render_form()
            else:
                return self.json_response({'error': 'Not allowed'})
        except Exception, e:
            return self.json_response({'error': str(e)})

    def render_form(self):
        data = {
            "layout": self.form.layout,
            "schema": {
                "type": "object",
                "title": self.form.title,
                "properties": {},
            },
            "form": [],
        }
        for field_id in self.form.fields.keys():
            settings = self.form.fields[field_id]
            data["schema"]["properties"][field_id] = {
                "title": field_id,
                "type": "string",
            }
            data["form"].append(field_id)

        return self.json_response(data)

    def __call__(self):
        return self.render()

    def __contains__(self, name):
        # When processing other methods than GET and POST, ZPublisher tries to
        # make sure the requested resource exists in the parent. So we just 
        # pretend that any part of the url path is an existing element.
        # That's quite hacky :)
        if name in self.request.URL.split('/'):
            return True
        else:
            return False