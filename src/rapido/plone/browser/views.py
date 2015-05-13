from Products.Five.browser import BrowserView
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse

from rapido.core.interfaces import IDatabase
from rapido.plone.storage import Storage


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

    def __call__(self):
        db_id = self.path[0]
        currentTheme = getCurrentTheme()
        if currentTheme is None:
            raise KeyError(db_id)
        themeDirectory = queryResourceDirectory(THEME_RESOURCE_NAME, currentTheme)  # noqa
        if themeDirectory is None:
            raise KeyError(db_id)
        settingsPath = "rapido/%s/settings.yaml" % (db_id,)
        if not themeDirectory.isFile(settingsPath):
            raise KeyError(db_id)

        result = themeDirectory.readFile(settingsPath)

        self.request.response.setHeader('X-Theme-Disabled', '1')
        return result
