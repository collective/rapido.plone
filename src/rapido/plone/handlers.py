# -*- coding: utf-8 -*-
from pyaml import yaml
from plone.tiles import Tile
from plone.tiles.interfaces import IBasicTile
from plone.tiles.type import TileType
from zope.component import provideAdapter, provideUtility
from zope.interface import Interface


def is_yaml(object):
    if object.getPhysicalPath()[-1].endswith('yaml'):
            return True
    return False


class RapidoDynamicTile(Tile):
    __name__ = 'rapido.dynamic.tile'  # dynamic replace

    def __call__(self):
        rapido = self.context.unrestrictedTraverse("@@rapido")
        return rapido.content(self.path.split('/'))


def resource_created(object, event):
    if is_yaml(object):
        yaml_settings = yaml.load(str(object))


def resource_modified(object, event):
    if is_yaml(object):
        yaml_settings = yaml.load(str(object))
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
