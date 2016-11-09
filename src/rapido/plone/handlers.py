# -*- coding: utf-8 -*-
from pyaml import yaml
from plone.registry.interfaces import IRegistry
from zope.component import provideAdapter, provideUtility, getUtility
from zope.interface import Interface
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces.browser import IBrowserRequest
from .app import get_theme_directory

try:
    from plone.app.mosaic.interfaces import ITile
    from plone.tiles import Tile
    from plone.tiles.interfaces import IBasicTile
    from plone.tiles.type import TileType
    HAS_MOSAIC = True
except ImportError:
    HAS_MOSAIC = False

RELOADED_SITES = []


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


if HAS_MOSAIC:
    class RapidoDynamicTile(Tile):
        __name__ = 'rapido.dynamic.tile'  # dynamic replace

        def __call__(self):
            rapido = self.context.unrestrictedTraverse("@@rapido")
            return rapido.content(self.path.split('/'))


def process_yaml(object):
        yaml_settings = yaml.load(str(object))
        if 'view' in yaml_settings:
            id = yaml_settings['view']
            path = object.getPhysicalPath()
            path = '/'.join(path[path.index('rapido') + 1:])
            path = path.rpartition('.')[0]
            view = get_block_view(path)
            provideAdapter(view, (Interface, IBrowserRequest),
                Interface, name=id)

        if HAS_MOSAIC and 'tile' in yaml_settings:
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


def resource_created_or_modified(object, event):
    if is_yaml(object):
        process_yaml(object)


def reload(event):
    # When rebooting the server, all TTW registered tiles or views are lost,
    # we need to go through all the existing .yaml files to redeclare them.
    # But as there is no plone_site_after_start event,
    # we subscribe to IPubSuccess and IPubFailure, and make sure we only
    # process the .yaml files once for each Plone site.
    site_id = event.request.steps[0]
    if site_id not in RELOADED_SITES:
        RELOADED_SITES.append(site_id)
        theme_dir = None
        try:
            theme_dir = get_theme_directory()
        except:
            # not a Plone site
            pass

        if theme_dir and theme_dir.isDirectory('rapido'):
            for entry in theme_dir['rapido'].listDirectory():
                if not theme_dir['rapido'].isDirectory(entry):
                    continue
                app_folder = theme_dir['rapido'][entry]
                if not app_folder.isDirectory('blocks'):
                    continue
                for file_id in app_folder['blocks'].listDirectory():
                    file = app_folder['blocks'][file_id]
                    if is_yaml(file):
                        try:
                            process_yaml(file)
                        except:
                            # we do not want to break the rendering of all our
                            # pages if something is wrong in a rapido app
                            pass
