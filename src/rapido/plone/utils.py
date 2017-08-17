
import StringIO
from plone.app.theming.utils import getAvailableThemes
from plone.resource.utils import queryResourceDirectory, cloneResourceDirectory
from zope.component import queryUtility
from rapido.plone.app import get_app, get_theme_directory



def getRapidoAppFromTheme(name):
    apps = []
    directory = get_theme_directory(name)
    if directory.isDirectory("rapido"):
        rapido_dir = directory["rapido"]
        for app in rapido_dir.listDirectory():
            if rapido_dir.isDirectory(app):
                apps.append(app)
            elif rapido_dir.isFile(app + '.lnk'):
                apps.append(app)
    return apps


def getAvailableRapidoApps(exclude_theme=None):
    themes = getAvailableThemes()
    apps = dict()
    for theme in themes:
        if theme.__name__ not in ["template", "barceloneta"] and theme.__name__ != exclude_theme:
            apps[theme.__name__] = getRapidoAppFromTheme(theme.__name__)
    return apps


def cloneLocalRapidoApp(src_theme, dest_theme, app_id, make_link=False):
    src_theme_dir = get_theme_directory(src_theme)
    dest_theme_dir = get_theme_directory(dest_theme)
    
    if not src_theme_dir:
        raise ThemeNotFound("{} theme not found".format(src_theme))
    if not dest_theme_dir:
        raise ThemeNotFound("{} theme not found".format(dest_theme))

    if not dest_theme_dir.isDirectory("rapido"):
        dest_theme_dir.makeDirectory("rapido")
    if src_theme_dir.isDirectory("rapido"):
        if src_theme_dir["rapido"].isDirectory(app_id):
            if dest_theme_dir["rapido"].isDirectory(app_id):
                raise RapidoAppAlreadyExists("A rapido app with {} id already exists in {}".format(app_id, dest_theme))
            if not make_link:
                dest_theme_dir["rapido"].makeDirectory(app_id)
                cloneResourceDirectory(src_theme_dir["rapido"][app_id], dest_theme_dir["rapido"][app_id])
            else:
                f = StringIO.StringIO()
                f.write(src_theme)
                try:
                    dest_theme_dir["rapido"].writeFile(app_id + '.lnk', f)
                finally:
                    f.close()
        elif src_theme_dir["rapido"].isFile(app_id + '.lnk'):
            f = src_theme_dir["rapido"].openFile(app_id + '.lnk')
            try:
                dest_theme_dir["rapido"].writeFile(app_id + '.lnk', f)
            finally:
                f.close()
        else:
            raise RapidoAppNotFound("{} rapido app is not found in {} theme".format(
                    app_id, src_theme
                ))
    else:
        raise RapidoAppNotFound("{} rapido app is not found in {} theme".format(
                app_id, src_theme
            ))


class ThemeNotFound(Exception):
    """Base class for exceptions in this module."""
    pass

class RapidoAppNotFound(Exception):
    """Base class for exceptions in this module."""
    pass

class RapidoAppAlreadyExists(Exception):
    """Base class for exceptions in this module."""
    pass