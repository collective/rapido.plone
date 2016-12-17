# -*- coding: utf-8 -*-
from pyaml import yaml
from plone.resource.file import FilesystemFile
from zope.component import provideAdapter
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest
from .app import get_theme_directory
from .browser.views import get_block_view

RELOADED_SITES = []


def getPath(file):
    if isinstance(file, FilesystemFile):
        return file.path.split('/')
    else:
        return file.getPhysicalPath()


def is_yaml(file):
    if getPath(file)[-1].endswith('yaml'):
            return True
    return False


def process_yaml(path, yaml_content):
    yaml_settings = yaml.load(yaml_content)
    if not yaml_settings:
        return
    if 'view' in yaml_settings:
        config = yaml_settings['view']
        with_theme = False
        if isinstance(config, dict):
            id = config['id']
            with_theme = config.get('with_theme', False)
        else:
            id = config
        path = '/'.join(path[-path[::-1].index('rapido'):])
        path = path.rpartition('.')[0]
        view = get_block_view(path, with_theme)
        provideAdapter(view, (Interface, IBrowserRequest),
                       Interface, name=id)


def resource_created_or_modified(obj, event):
    if is_yaml(obj):
        process_yaml(
            getPath(obj),
            str(obj)
        )


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
        except:  # pragma: no cover
            # not a Plone site
            pass

        if theme_dir and theme_dir.isDirectory('rapido'):
            for entry in theme_dir['rapido'].listDirectory():
                if not theme_dir['rapido'].isDirectory(entry):
                    continue
                app_folder = theme_dir['rapido'][entry]
                if not app_folder.isDirectory('blocks'):  # pragma: no cover
                    continue
                for file_id in app_folder['blocks'].listDirectory():
                    if file_id.endswith('.yaml'):
                        try:
                            process_yaml(
                                getPath(app_folder['blocks'][file_id]),
                                app_folder['blocks'].readFile(file_id)
                            )
                        except:  # pragma: no cover
                            # we do not want to break the rendering of all our
                            # pages if something is wrong in a rapido app
                            pass
