from zope.interface import implements
from plone import api
from plone.app.theming.interfaces import THEME_RESOURCE_NAME
from plone.app.theming.utils import getCurrentTheme
from plone.resource.utils import queryResourceDirectory
from urlparse import urlparse

from rapido.core.app import Context
from rapido.core.interfaces import IRapidable, IRapidoApplication


class RapidoApplication:
    implements(IRapidable)

    def __init__(self, id, context):
        self.id = id
        self.context = context
        self.available_rules = {}
        self.resources = self.get_resource_directory()

    def url(self, rest=False):
        if rest:
            url_format = "%s/@@rapido/json/%s"
        else:
            url_format = "%s/@@rapido/%s"
        return url_format % (
            api.portal.get().absolute_url(),
            self.id,
        )

    @property
    def root(self):
        return api.portal.get()

    @property
    def forms(self):
        return self.resources['forms'].listDirectory()

    def get_settings(self):
        try:
            return self.get_resource('settings.yaml')
        except KeyError:
            # settings.yaml is not mandatory
            return 'no_settings: {}'

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
            return self.resources.readFile(str(full_path))
        except:
            raise KeyError(full_path)

    def current_user(self):
        """ Returns the current user id
        """
        return api.user.get_current().getUserName()

    def current_user_groups(self):
        """ Get the current user groups
        """
        member = api.user.get_current()
        return member.getGroups()


def get_app(app_id, request):
    portal = api.portal.get()
    context = Context()
    context.request = request
    context.parent_request = request.get("PARENT_REQUEST", None)
    path = None
    if context.parent_request:
        path = context.parent_request['PATH_INFO']
    elif request.get('HTTP_REFERER', None):
        path = urlparse(request['HTTP_REFERER']).path
    if path:
        path = path.split("@@")[0]
        try:
            context.content = portal.unrestrictedTraverse(path)
        except KeyError:
            # not a Plone url, probably a browsertest context
            context.content = None
    else:
        context.content = None
    context.portal = portal
    context.api = api
    app = RapidoApplication(app_id, context)
    return IRapidoApplication(app)
