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
        self.query = "get"
        self.doc = None
        self.error = None

    def json_response(self, result):
        self.request.response.setHeader("Content-Type", "application/json")
        return json.dumps(result)

    def publishTraverse(self, request, name):
        if name in ["_update", "_create", "_delete", "_search"]:
            self.query = name
            return self

        doc = IDatabase(self.context).get_document(name)
        if not doc:
            raise NotFound(self, name, request)
        self.doc = doc
        return self

    def render(self):
        if self.query == "get":
            return self.json_response(self.doc.items())
        else:
            return self.json_response('Not implemented')

    def __call__(self):
        return self.render()