from zope.interface import implements
from Products.Five.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound

from rapido.core.interfaces import IDatabase


class RapidoView(BrowserView):
    implements(IPublishTraverse)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.path = []

    def publishTraverse(self, request, name):
        self.path.append(name)
        return self

    def render(self):
        db_id = self.path[0]
        return db_id

    def __call__(self):
        return self.render()
