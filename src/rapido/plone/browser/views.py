from AccessControl import Unauthorized as unauth
from datetime import datetime
import json
from plone.protect import CheckAuthenticator
from plone.protect.authenticator import createToken
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import zExceptions
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse

from rapido.core.exceptions import NotAllowed, Unauthorized, NotFound
from rapido.core.interfaces import IRest, IDisplay
from rapido.plone.app import get_app


class PythonObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(
            obj,
            (list, dict, str, unicode, int, float, bool, type(None))
        ):
            return json.JSONEncoder.default(self, obj)
        return {'_not_serializable': str(obj)}


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

    def store_app_messages(self, app):
        if not app.settings.get('debug'):
            return
        if len(app.messages) > 0:
            old_messages = app.context.cache.get('messages', [])
            app.context.cache['messages'] = old_messages + app.messages

    def get_app_messages(self):
        app_id = self.path[0]
        app = get_app(app_id, self.request)
        messages = app.context.cache.get('messages', [])
        app.context.cache['messages'] = []
        return messages

    def content(self, path=None):
        if not path:
            path = self.path
        app_id = path[0]
        app = get_app(app_id, self.request)
        method = getattr(IDisplay(app), self.method)
        try:
            (result, redirect) = method(path, self.request)
        except NotAllowed:
            raise zExceptions.BadRequest()
        except NotFound:
            raise zExceptions.NotFound()
        except Unauthorized:
            raise unauth("Not authorized")
        self.store_app_messages(app)
        if redirect:
            self.request.RESPONSE.redirect(redirect)
        else:
            return result

    def json(self, path=None):
        if not path:
            path = self.path
        app_id = path[0]
        if len(path) > 1:
            path = path[1:]
        else:
            path = None
        try:
            app = get_app(app_id, self.request)
            if self.method not in ["GET", "OPTIONS"]:
                CheckAuthenticator(self.request)
            method = getattr(IRest(app), self.method)
            result = method(path, self.request.get('BODY'))
            self.store_app_messages(app)
            return result
        except NotAllowed:
            self.request.response.setStatus(403)
        except NotFound, e:
            self.request.response.setStatus(404)
            return {'id': str(e.name)}
        except Unauthorized:
            self.request.response.setStatus(401)
        except Exception, e:
            self.request.response.setStatus(500)
            return {'error': str(e)}

    def __call__(self):
        if self.path[0] == 'view':
            # this is neutral, we just return the default content view
            # but it gives the opportunity to create specific pseudo views
            # via our Diazo rules.xml
            return self.context()

        self.request.response.setHeader('X-Theme-Disabled', '1')

        if self.path[-1].startswith('$'):
            # inject Diazo parent request path
            parent_path = self.request.PARENT_REQUEST['URL'].split('/')
            try:
                offset = int(self.path[-1][1:])
            except ValueError:
                return "Bad Rapido url injection %s" % self.path[-1]
            index = parent_path.index('@@rapido')
            self.path = self.path[:-1] + parent_path[index + offset:]

        if len(self.path) == 2 and self.path[1] == '_log':
            messages = self.get_app_messages()
            self.request.response.setHeader('content-type', 'application/json')
            return json.dumps(messages, cls=PythonObjectEncoder)

        if "application/json" in self.request.getHeader('Accept', ''):
            result = self.json()
            if len(self.path) == 1:
                self.request.response.setHeader('X-CSRF-TOKEN', createToken())
            self.request.response.setHeader('content-type', 'application/json')
            return json.dumps(result, cls=PythonObjectEncoder)
        else:
            result = self.content()
            return result

    def __contains__(self, name):
        # When processing other methods than GET and POST, ZPublisher tries to
        # make sure the requested resource exists in the parent. So we just
        # pretend that any part of the url path is an existing element.
        # That's quite hacky :)
        if name in self.request.URL.split('/'):
            return True
        else:
            return False


def get_block_view(path, with_theme):

    class RapidoDynamicView(BrowserView):

        template = ViewPageTemplateFile('view.pt')

        def __call__(self):
            rapido = self.context.unrestrictedTraverse("@@rapido")
            self.content = rapido.content(path.split('/'))
            if with_theme:
                return self.template()
            else:
                return self.content

    return RapidoDynamicView
