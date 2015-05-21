from zope.interface import implements
from plone import api
from plone.app.theming.interfaces import THEME_RESOURCE_NAME
from plone.app.theming.utils import getCurrentTheme
from plone.resource.utils import queryResourceDirectory

from rapido.core.app import Context
from rapido.core.interfaces import IRapidable, IRapidoApplication


class RapidoApplication:
    implements(IRapidable)

    def __init__(self, id, context):
        self.id = id
        self.context = context
        self.available_rules = {}
        self.resources = self.get_resource_directory()

    def url(self):
        return "%s/@@rapido/%s" % (
            api.portal.get().absolute_url(),
            self.id,
        )

    @property
    def forms(self):
        return self.resources['forms'].listDirectory()

    def get_form(self, form_id, ftype='yaml'):
        path = "forms/%s.%s" % (form_id, ftype)
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


def get_app(app_id, request):
    portal = api.portal.get()
    context = Context()
    context.request = request
    context.parent_request = request.get("PARENT_REQUEST", None)
    context.portal = portal
    context.api = api
    context.content = portal.restrictedTraverse(
        request['PARENT_REQUEST']['PATH_INFO'])
    app = RapidoApplication(app_id, context)
    return IRapidoApplication(app)
