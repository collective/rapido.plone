# -*- coding: utf-8 -*-
from pyaml import yaml
from plone.app.mosaic.interfaces import ITile
from plone.registry.interfaces import IRegistry
from plone.tiles import Tile
from plone.tiles.interfaces import IBasicTile
from plone.tiles.type import TileType
from zope.component import provideAdapter, provideUtility, getUtility
from zope.interface import Interface
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces.browser import IBrowserRequest


def is_yaml(object):
    if object.getPhysicalPath()[-1].endswith('yaml'):
            return True
    return False


def get_block_view(path):

    class RapidoDynamicView(BrowserView):

        def __call__(self):
            rapido = self.context.unrestrictedTraverse("@@rapido")
            return rapido.content(path.split('/'))

    return RapidoDynamicView


class RapidoDynamicTile(Tile):
    __name__ = 'rapido.dynamic.tile'  # dynamic replace

    def __call__(self):
        rapido = self.context.unrestrictedTraverse("@@rapido")
        return rapido.content(self.path.split('/'))


def resource_created_or_modified(object, event):
    if is_yaml(object):
        yaml_settings = yaml.load(str(object))
        if 'view' in yaml_settings:
            id = yaml_settings['view']
            path = object.getPhysicalPath()
            path = '/'.join(path[path.index('rapido') + 1:])
            path = path.rpartition('.')[0]
            view = get_block_view(path)
            provideAdapter(view, (Interface, IBrowserRequest),
                Interface, name=id)

        if 'tile' in yaml_settings:
            id = object.id().rpartition('.')[0]
            tile_type = TileType(
                id,
                yaml_settings['tile']['label'],
                'zope.View',
                'zope.View',
                description=u'',
                schema=None)

            provideUtility(tile_type, name=id)
            tile = RapidoDynamicTile
            path = object.getPhysicalPath()
            path = '/'.join(path[path.index('rapido') + 1:])
            tile.path = path.rpartition('.')[0]
            provideAdapter(RapidoDynamicTile, (Interface, Interface),
                           IBasicTile, name=id)
            prefix = 'plone.app.mosaic.app_tiles.rapido_dynamic_tile_' + id
            registry = getUtility(IRegistry)
            registry.registerInterface(ITile, prefix=prefix)
            registry[prefix + '.name'] = unicode(id)
            registry[prefix + '.label'] = unicode(
                yaml_settings['tile']['label'])
            registry[prefix + '.category'] = u'advanced'
            registry[prefix + '.tile_type'] = u'app'
            registry[prefix + '.default_value'] = None
            registry[prefix + '.read_only'] = False
            registry[prefix + '.settings'] = True
            registry[prefix + '.favorite'] = False
            registry[prefix + '.rich_text'] = False
            registry[prefix + '.weight'] = 10
