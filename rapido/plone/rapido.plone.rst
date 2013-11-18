Integration Tests
-----------------

Create a Rapido database object and put it in a folder:

    >>> from zope.component import createObject
    >>> db_obj = createObject('rapido.plone.database')
    >>> from zope.event import notify
    >>> from zope.lifecycleevent import ObjectCreatedEvent
    >>> notify(ObjectCreatedEvent(db_obj))
    >>> db_obj.portal_type
    'rapido.plone.database'
    >>> db_obj.setTitle('Test db')
    >>> db_obj.Title()
    'Test db'
    >>> from plone.dexterity.utils import addContentToContainer
    >>> db = addContentToContainer(folder, db_obj)
    >>> db
    <Database at /plone/Members/test_user_1_/test-db>

Storage has been initialized:
    >>> from rapido.core.interfaces import IDatabase
    >>> IDatabase(db).storage
    <rapido.souper.soup.SoupStorage object at ...>

Add a form:

    >>> form_obj = createObject('rapido.plone.form', id='frmtest')
    >>> notify(ObjectCreatedEvent(form_obj))
    >>> form_obj.portal_type
    'rapido.plone.form'
    >>> form_obj.setTitle('Test form')
    >>> form = addContentToContainer(db, form_obj)
    >>> form
    <Form at /plone/Members/test_user_1_/test-db/frmtest>

Layout is updated on change:
    >>> from plone.app.textfield.value import RichTextValue
    >>> form.html = RichTextValue("""Song: <span data-rapido-field="song">song</span>""")
    >>> from zope.lifecycleevent import ObjectModifiedEvent
    >>> notify(ObjectModifiedEvent(form))
    >>> from rapido.core.interfaces import IForm
    >>> IForm(form).layout
    'Song: <span data-rapido-field="song">song</span>'

Add a field in the form:

    >>> field_obj = createObject('rapido.plone.field', id='song')
    >>> notify(ObjectCreatedEvent(field_obj))
    >>> field_obj.portal_type
    'rapido.plone.field'
    >>> field = addContentToContainer(form, field_obj)
    >>> field
    <Field at /plone/Members/test_user_1_/test-db/frmtest/song>

Form fields definition is updated on change:
    >>> field.type = 'TEXT'
    >>> field.index_type = 'FIELD'
    >>> notify(ObjectModifiedEvent(field))
    >>> IForm(form).fields
    {'song': {'index_type': 'FIELD', 'type': 'TEXT'}}
