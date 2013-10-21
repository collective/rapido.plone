Use the resources directory for non-template browser resources like images,
stylesheets and JavaScript.

Contents of this folder may be addressed in templates via TAL. For
example, if you placed at test.js resource in this folder, you could insert it
via template code like:

<script type="text/javascript" src="test.js"
    tal:attributes="src string:${context/@@plone_portal_state/portal_url}/++resource++rapido.plone/test.js"></script>

It's more likely you'd add it the portal_javascript registry with an id of ++resource++dexterity.test/test.js.

Static folder resources are public.