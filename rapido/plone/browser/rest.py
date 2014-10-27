import json
from zope.interface import implements
from Products.Five.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound

from rapido.core.interfaces import IDatabase, IRest


class Api(BrowserView):
    implements(IPublishTraverse)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.db = IDatabase(self.context)
        self.method = self.request.method
        self.path = []

    def json_response(self, result, status):
        self.request.response.setStatus(status)
        self.request.response.setHeader("Content-Type", "application/json")
        return json.dumps(result)

    def publishTraverse(self, request, name):
        self.path.append(name)
        return self

    def render(self):
        rest = IRest(self.db)
        method = getattr(rest, self.method)
        body = self.request.get('BODY')
        data = method(self.path, body)
        return self.json_response(data, rest.status)

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