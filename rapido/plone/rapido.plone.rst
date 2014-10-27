Integration Tests
-----------------

Create a Rapido database object and put it in a folder::

    >>> id = folder.invokeFactory('rapido.plone.database', 'test-db')
    >>> db = folder['test-db']
    >>> db
    <Database at /plone/Members/test_user_1_/test-db>
    >>> db.portal_type
    'rapido.plone.database'
    >>> db.setTitle('Test db')
    >>> db.Title()
    'Test db'

Storage has been initialized::
    >>> from rapido.core.interfaces import IDatabase
    >>> IDatabase(db).storage
    <rapido.souper.soup.SoupStorage object at ...>

Add a form::

    >>> id = db.invokeFactory('rapido.plone.form', 'frmtest')
    >>> form = db['frmtest']
    >>> form
    <Form at /plone/Members/test_user_1_/test-db/frmtest>
    >>> form.portal_type
    'rapido.plone.form'
    >>> form.setTitle('Test form')
    

Layout is updated on change::
    >>> from plone.app.textfield.value import RichTextValue
    >>> form.html = RichTextValue("""Song: <span data-rapido-field="song">song</span>""")
    >>> from zope.event import notify
    >>> from zope.lifecycleevent import ObjectModifiedEvent
    >>> notify(ObjectModifiedEvent(form))
    >>> from rapido.core.interfaces import IForm
    >>> IForm(form).layout
    'Song: <span data-rapido-field="song">song</span>'

Add a field in the form::

    >>> id = form.invokeFactory('rapido.plone.field', 'song')
    >>> field = form['song']
    >>> field
    <Field at /plone/Members/test_user_1_/test-db/frmtest/song>
    >>> field.portal_type
    'rapido.plone.field'
    

Form fields definition is updated on change::
    >>> field.type = 'TEXT'
    >>> field.index_type = 'FIELD'
    >>> notify(ObjectModifiedEvent(field))
    >>> IForm(form).fields
    {'song': {'index_type': 'FIELD', 'type': 'TEXT', 'description': '', 'title': ''}}

The database design can be exported and imported::
    >>> from rapido.core.interfaces import IExporter
    >>> exporter = IExporter(IDatabase(db))
    >>> data = exporter.export_database()
    >>> data
    {'forms': {'frmtest': {'frmtest.html': 'Song: <span data-rapido-field="song">song</span>', 'frmtest.yaml': "assigned_rules: []\nfields:\n  song: {description: '', index_type: FIELD, title: '', type: TEXT}\nid: frmtest\ntitle: !!python/unicode 'Test form'\n", 'frmtest.py': ''}}, 'settings.yaml': 'acl:\n  rights:\n    author: []\n    editor: []\n    manager: [test_user_1_]\n    reader: []\n  roles: {}\n'}
    >>> id = folder.invokeFactory('rapido.plone.database', 'new-db')
    >>> newdb = folder['new-db']
    >>> newdb.forms
    []
    >>> from rapido.core.interfaces import IImporter
    >>> IImporter(IDatabase(newdb)).import_database(data)
    >>> newdb.forms[0].id
    'frmtest'

When the imported design contains a form already existing in the db, the local
one will be overridden ::
    >>> newdb.frmtest.song.type
    'TEXT'
    >>> newdb.frmtest.song.type = 'NUMBER'
    >>> IImporter(IDatabase(newdb)).import_database(data)
    >>> newdb.frmtest.song.type
    'TEXT'


