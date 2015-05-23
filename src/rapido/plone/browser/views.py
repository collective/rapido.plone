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

    def __call__(self):
        app_id = self.path[0]
        directive = self.path[1]
        obj_id = self.path[2]
        if len(self.path) > 3:
            action = self.path[3]
        else:
            action = 'view'

        app = get_app(app_id, self.request)
        if directive == "form":
            form = app.get_form(obj_id)
            if self.method == "POST":
                # execute submitted actions
                actions = [key for key in self.request.keys()
                    if key.startswith("action.")]
                for id in actions:
                    field_id = id[7:]
                    if form.fields.get(field_id, None):
                        form.compute_field(field_id, {'form': form})
            result = form.display(edit=True)
        else:
            result = "Unknown directive"

        self.request.response.setHeader('X-Theme-Disabled', '1')
        return result
