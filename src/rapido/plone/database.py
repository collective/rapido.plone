from zope.interface import implements
from plone import api
from plone.app.theming.interfaces import THEME_RESOURCE_NAME
from plone.app.theming.utils import getCurrentTheme
from plone.resource.utils import queryResourceDirectory

from rapido.core.interfaces import IDatabasable


class Database:
    implements(IDatabasable)

    def __init__(self, id):
        self.id = id
        self.available_rules = {}
        self.resources = self.get_resource_directory()

    def url(self):
        return api.portal.get().absolute_url()

    @property
    def forms(self):
        return self.resources['forms'].listDirectory()

    def get_form(self, form_id, ftype='yaml'):
        path = "%s.%s" % (form_id, ftype)
        return self.get_resource(path)

    def get_resource_directory(self):
        theme = getCurrentTheme()
        if theme is None:
            raise KeyError(self.id)
        directory = queryResourceDirectory(THEME_RESOURCE_NAME, theme)
        if directory is None:
            raise KeyError(self.id)
        return directory

    def get_resource(self, path):
        full_path = "rapido/%s/%s" % (self.id, path)
        try:
            return self.resources.readFile(full_path)
        except:
            raise KeyError(full_path)
