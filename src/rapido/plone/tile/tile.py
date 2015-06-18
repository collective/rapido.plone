from plone.memoize.view import memoize
from plone.supermodel import model
from plone.tiles import Tile
from zope import schema

from rapido.plone import _


class IRapidoTile(model.Schema):

    path = schema.TextLine(
        title=_(u"Rapido path"),
        description=_(u"Enter a valid rapido url "
            "(without the @@rapido/ prefix)."),
        required=True,
    )


class RapidoTile(Tile):
    """Rapido tile
    """

    @property
    @memoize
    def content(self):
        rapido = self.context.unrestrictedTraverse("@@rapido")
        return rapido.content(self.data['path'].split('/'))
