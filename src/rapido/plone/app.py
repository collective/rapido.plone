from plone import api
from plone.app.theming.interfaces import THEME_RESOURCE_NAME
from plone.app.theming.utils import getCurrentTheme
from plone.memoize.interfaces import ICacheChooser
from plone.resource.utils import queryResourceDirectory
from zope.component import queryUtility
from zope.interface import implements
from zExceptions import NotFound

from rapido.core import exceptions
from rapido.core.app import Context
from rapido.core.interfaces import IRapidable, IRapidoApplication


class RapidoApplication(object):
    implements(IRapidable)

    def __init__(self, id, context):
        self.id = id
        self.context = context
        self.available_rules = {}
        self.resources = self.get_resource_directory()
        self.cache = queryUtility(ICacheChooser)("rapido-" + id)

    def url(self):
        url_format = "%s/@@rapido/%s"
        target = self.context.content or api.portal.get()
        return url_format % (
            target.absolute_url(),
            self.id,
        )

    @property
    def root(self):
        return api.portal.get()

    @property
    def blocks(self):
        ids = []
        files = self.resources['blocks'].listDirectory()
        for filename in files:
            id = filename.rpartition('.')[0]
            if id not in ids:
                ids.append(id)
        return ids

    def get_settings(self):
        try:
            return self.get_resource('settings.yaml')
        except KeyError:
            # settings.yaml is not mandatory
            return 'no_settings: {}'

    def get_block(self, block_id, ftype='yaml'):
        path = "blocks/%s.%s" % (block_id, ftype)
        try:
            return self.get_resource(path)
        except KeyError:
            if ftype == "yaml":
                return 'id: %s' % block_id
            else:
                raise KeyError('%s.%s' % (block_id, ftype))

    def get_resource_directory(self):
        theme = getCurrentTheme()
        directory = queryResourceDirectory(THEME_RESOURCE_NAME, theme)
        try:
            return directory['rapido'][self.id]
        except NotFound:
            raise exceptions.NotFound(self.id)

    def get_resource(self, path):
        try:
            return self.resources.readFile(str(path))
        except:
            raise KeyError(path)

    def current_user(self):
        """ Returns the current user id
        """
        return api.user.get_current().getUserName()

    def current_user_groups(self):
        """ Get the current user groups
        """
        if api.user.is_anonymous():
            return []
        member = api.user.get_current()
        return member.getGroups()

    def is_manager(self):
        if api.user.is_anonymous():
            return False
        if 'Manager' in api.user.get_roles():
            return True
        return False


def get_app(app_id, request):
    portal = api.portal.get()
    context = Context()
    context.request = request
    context.parent_request = request.get("PARENT_REQUEST", None)
    if context.parent_request:
        path = '/'.join(
            context.parent_request.physicalPathFromURL(
                context.parent_request.URL))
    else:
        path = '/'.join(request.physicalPathFromURL(request.URL))
    path = path.split("@@")[0]
    context.content = None
    while not hasattr(context.content, 'portal_type'):
        try:
            context.content = portal.unrestrictedTraverse(path)
        except:
            pass
        path = '/'.join(path.split('/')[0:-1])
    context.portal = portal
    context.api = api
    app = RapidoApplication(app_id, context)
    return IRapidoApplication(app)
