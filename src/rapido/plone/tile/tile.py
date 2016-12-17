from plone.memoize.view import memoize
from plone.supermodel import model
from plone.tiles import Tile
from zope import schema
from zope.interface import implements
from plone.tiles.interfaces import ITile

from rapido.plone import _


class IRapidoTile(model.Schema):

    path = schema.TextLine(
        title=_(u"Rapido path"),
        description=_(u"Enter a valid rapido url "
            "(without the @@rapido/ prefix)."),
        required=True,
    )


class RapidoTile(Tile):
    """Rapido tile"""

    @property
    @memoize
    def content(self):
        rapido = self.context.unrestrictedTraverse("@@rapido")
        return rapido.content(self.data['path'].split('/'))


class IRapidoDynamicTile(model.Schema):

    pass


def get_dynamic_tile(path):

    class RapidoDynamicTile(Tile):
        implements(ITile)

        __name__ = 'rapido.dynamic.tile'

        def __call__(self):
            rapido = self.context.unrestrictedTraverse("@@rapido")
            return rapido.content(path.split('/'))

    return RapidoDynamicTile
