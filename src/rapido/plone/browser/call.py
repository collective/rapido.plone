from Products.Five.browser import BrowserView

from rapido.plone.app import get_app


class RapidoCall(BrowserView):
    """Call a Rapido element.

    Useful in PythonScripts
    """

    def __call__(self, path, content=None, **kw):
        (app_id, block_id, element_id) = path.split('/')
        app = get_app(app_id, self.request, content=content)
        block = app.get_block(block_id)
        return block.compute_element(
            element_id, {'block': block, 'params': kw})
