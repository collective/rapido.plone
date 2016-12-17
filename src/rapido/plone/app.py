from plone import api
from plone.app.theming.interfaces import THEME_RESOURCE_NAME
from plone.app.theming.utils import getCurrentTheme
from plone.memoize.interfaces import ICacheChooser
from plone.resource.utils import queryResourceDirectory
from zope.component import queryUtility
from zope.interface import implements
from zope.pagetemplate.pagetemplate import PageTemplate

from rapido.core import exceptions
from rapido.core.app import Context
from rapido.core.interfaces import IRapidable, IRapidoApplication


class RapidoTemplateFile(PageTemplate):

    def __init__(self, text):
        self.write(text)

    def __call__(self, elements, context):
        try:
            return self.pt_render({'elements': elements, 'context': context})
        except Exception, e:
            error = str(e)
            extra = ('<pre>' in error and error[
                error.index('<pre>') + 5:error.index('</pre>')]) or ''
            lines = error.split('\n')
            if len(lines) > 4:
                message = "%s\n%s" % (lines[2], lines[4])
            else:
                message = str(e)
            return "<pre>Rendering error\n%s\n\n%s</pre>" % (
                message, extra.replace('\\n', '\n'))


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
            content = self.get_resource(path)
            if ftype in ('html', 'pt', ):
                content = content.decode('utf-8')
            return content
        except KeyError:
            if ftype == "yaml":
                # the YAML file is not mandatory, return a default content
                return 'id: %s' % block_id
            elif ftype == "html":
                # if .html is missing, try .pt
                try:
                    pt = self.get_block(block_id, ftype="pt")
                    return RapidoTemplateFile(pt)
                except KeyError:
                    raise KeyError('%s.%s' % (block_id, ftype))
            else:
                raise KeyError('%s.%s' % (block_id, ftype))

    def get_resource_directory(self, name=None):
        directory = get_theme_directory(name)
        if not directory.isDirectory('rapido'):
            raise exceptions.NotFound(self.id)
        if directory['rapido'].isDirectory(self.id):
            return directory['rapido'][self.id]
        elif directory['rapido'].isFile(self.id + '.lnk'):
            directory_name = directory['rapido'].readFile(self.id + '.lnk')
            return self.get_resource_directory(name=directory_name)
        else:
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


def get_app(app_id, request, content=None):
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
    context.content = content
    while not hasattr(context.content, 'portal_type'):
        try:
            context.content = portal.unrestrictedTraverse(path)
        except:
            pass
        path = '/'.join(path.split('/')[0:-1])
    context.portal = portal
    context.api = api
    context.rapido = lambda id, content=context.content: get_app(
        id, request, content=content)
    app = RapidoApplication(app_id, context)
    return IRapidoApplication(app)


def get_theme_directory(name=None):
    return queryResourceDirectory(
        THEME_RESOURCE_NAME, name or getCurrentTheme())
