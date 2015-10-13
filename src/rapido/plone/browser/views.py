import json
from plone.protect.authenticator import createToken
from Products.Five.browser import BrowserView
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse

from rapido.core.exceptions import NotAllowed, Unauthorized, NotFound
from rapido.core.interfaces import IRest
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
        (result, redirect) = app.process(
            self.method, directive, obj_id, action)
        if redirect:
            self.request.RESPONSE.redirect(redirect)
        else:
            return result

    def json(self, path=None):
        if not path:
            path = self.path[1:]
        app_id = path[0]
        if len(path) > 0:
            path = path[1:]
        else:
            path = None
        app = get_app(app_id, self.request)
        method = getattr(IRest(app), self.method)
        try:
            return method(path, self.request.get('BODY'))
        except NotAllowed:
            self.request.response.setStatus(403)
        except NotFound:
            self.request.response.setStatus(404)
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
        elif self.path[0] == 'json':
            result = self.json()
            self.request.response.setHeader('X-Theme-Disabled', '1')
            if len(self.path) == 2:
                self.request.response.setHeader('X-CSRF-TOKEN', createToken())
            self.request.response.setHeader('content-type', 'application/json')
            return json.dumps(result)
        else:
            result = self.content()
            self.request.response.setHeader('X-Theme-Disabled', '1')
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
