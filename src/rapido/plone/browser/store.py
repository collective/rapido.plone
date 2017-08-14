import json
from Products.Five.browser import BrowserView
from plone.app.theming.utils import getAvailableThemes
from plone.app.theming.utils import getCurrentTheme

from rapido.plone.app import get_app
from rapido.plone.utils import getAvailableRapidoApps, getRapidoAppFromTheme
from rapido.plone.utils import cloneLocalRapidoApp
from rapido.plone.utils import ThemeNotFound, RapidoAppNotFound, RapidoAppAlreadyExists



class RapidoStoreAPI(BrowserView):
    """Call a Rapido element.

    Useful in PythonScripts
    """
    
    def do_action(self, action):
        if action == "list":
            apps = getAvailableRapidoApps(exclude_theme=getCurrentTheme())
            return json.dumps(apps)
        elif action == "import":
            return self.import_rapido_app()
        return json.dumps({
            "error": "No request param was given",
            "code": 1
        })
    
    
    def import_rapido_app(self):
        app_id = self.request.get("app_id")
        source_id = self.request.get("source_id")
        destination_id = self.request.get("destination_id") or getCurrentTheme()
        make_link = self.request.get("make_link") == '1'
        
        if not source_id:
            return json.dumps({
                "error": "No theme id was given",
                "code": 2
            })
        if not app_id:
            return json.dumps({
                "error": "No app id was given",
                "code": 3
            })
        try:
            cloneLocalRapidoApp(
                src_theme=source_id,
                dest_theme=destination_id,
                app_id=app_id,
                make_link=make_link
            )
        except RapidoAppNotFound as e:
            return json.dumps({
                "error": e.message,
                "code": 4
            })
        except ThemeNotFound as e:
            return json.dumps({
                "error": e.message,
                "code": 5
            })
        except RapidoAppAlreadyExists as e:
            return json.dumps({
                "error": e.message,
                "code": 6
            })
        except Exception as e:
            return json.dumps({
                "error": e.message,
                "code": 7
            })
        return json.dumps({
            "message": "{} has been imported in {} theme".format(app_id, destination_id),
            "error": False
        })
            

    def __call__(self):
        action = self.request.get("action")
        return self.do_action(action)