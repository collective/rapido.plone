import json
from Products.Five.browser import BrowserView
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse

from rapido.plone.app import get_app


class RapidoView(BrowserView):
    implements(IPublishTraverse)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.method = self.request.method
        self.path = []

    def publishTraverse(self, request, name):
        self.path.append(name)
        return self

    def content(self, path=None):
        if not path:
            path = self.path
        app_id = path[0]
        directive = path[1]
        obj_id = path[2]
        if len(path) > 3:
            action = path[3]
        else:
            action = 'view'

        app = get_app(app_id, self.request)
        return app.process(self.method, directive, obj_id, action)

    def json(self, path=None):
        if not path:
            path = self.path[1:]
        app_id = path[0]
        directive = path[1]
        if len(path) > 2:
            obj_id = path[2]
        else:
            obj_id = None
        app = get_app(app_id, self.request)
        return app.json(self.method, self.request, directive, obj_id)

    def __call__(self):
        if self.path[0] == 'view':
            # this is neutral, we just return the default content view
            # but it gives the opportunity to create specific pseudo views
            # via our Diazo rules.xml
            return self.context()
        elif self.path[0] == 'json':
            result = self.json()
            self.request.response.setHeader('X-Theme-Disabled', '1')
            self.request.response.setHeader('content-type', 'application/json')
            return json.dumps(result)
        else:
            result = self.content()
            self.request.response.setHeader('X-Theme-Disabled', '1')
            return result
