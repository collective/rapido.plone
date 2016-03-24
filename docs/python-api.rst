Python API
==========

Any Rapido Python function receives ``context`` as parameter.

The ``context`` provides the following properties:

- ``context.app``,
- ``context.request``,
- ``context.parent_request``,
- ``context.portal``,
- ``context.content``,
- ``context.record``,
- ``context.api``,
- ``context.modules``.

``context.app``
---------------

This property gives access to the Rapido application object.

*Propeties*

``acl``
    Returns the Rapido application's access control list object (see below).

``blocks``
    Returns the existing block ids.

``indexes``
    Returns the existing index ids.

``url``
    Returns the application URL.

*Methods*

``create_record(self, id=None)``
    Creates and return a new record.
    If ``id`` is not provided, a default one is generated.
    If ``id`` already exists, it is replaced with another one (like ``...-1``,
    ``...-2``).

``delete_record(self, id=None, record=None, ondelete=True)``
    Delete the record (which can be passed as object or id).
    If ``ondelete``, the ``on_delete`` function will be called (if it exists)
    before deleting the record.

``get_block(self, block_id)``
    Returns a block.

``get_record(self, id)``
    Returns the record corresponding to the ``id``, or ``None`` if it does not
    exists.

``log(self, message)``
    Logs a message in the server log. And if the the app is in debug mode, logs
    the same message in the browser's javascript console.
    Messages can be strings or any other serializable object.

``records(self)``
    Returns all the records as a list.
    
``_records(self)``
    Returns all the records as a Python generator.

``search(self, query, sort_index=None, reverse=False)``
    Performs a search and returns records as a list.

``_search(self, query, sort_index=None, reverse=False)``
    Performs a search and returns records as a Python generator.

``context.request`` and ``context.parent_request``
--------------------------------------------------

``context.request`` is the actual request to Rapido, like::

    http://localhost:8080/Plone/@@rapido/rating/block/rate

When a block is embedded in a Plone page, ``context.request`` has not been
issued by the user's browser, it has been issued by Diazo.

To get the request issued by the user's browser, we use
``context.parent_request``.

Both of them are HTTP requests objects, see the `reference documentation <http://docs.plone.org/develop/plone/serving/http_request_and_response.html>`_.

Exemples:

- Reading submitted values:

.. code-block:: python

    val1 = context.request.get('field_1') # will returns None if not exists
    val1 = context.request['field_2'] # will fail if not exists

- Reading the ``BODY``:

.. code-block:: python

    request.get('BODY')


``context.portal``
------------------

It returns the Plone portal object.

It is equivalent to:

.. code-block:: python

    context.api.portal.get()

The most common task we will perform through the portal object is to get its contents:

.. code-block:: python

    folder = context.portal['my-folder']

``context.content``
-------------------

It returns the current Plone content.

The most common tasks we will perform on the content are:

- reading/writing its attributes (read/write):

.. code-block:: python

    the_tile = context.content.title
    context.content.title = "I prefer another title"

- getting its URL:

.. code-block:: python

    context.content.absolute_url()

To manipulate the content, refer to the `Plone API documentation about contents <http://docs.plone.org/develop/plone.api/docs/content.html>`_.

.. note ::

    Depending on its content type, the content object might have very different methods and properties.

``context.record``
-------------------

It returns the current Rapido record if any.

See `Record`_ for more information.

``context.api``
---------------

It gives access to the full `Plone API <http://docs.plone.org/develop/plone.api/docs/index.html>`_.

.. warning::

    There is no need to import the API, as shown in all the Plone API examples:

    .. code-block:: python

        from plone import api # WRONG

    because the API is already available in the Rapido `context`:

    .. code-block:: python

        catalog = context.api.portal.get().portal_catalog

This API mainly allows:

- to search contents, example:
    
    .. code-block:: python

        folders = context.api.content.find(portal_type="Folder")
        # be careful, the find() method return Brain objects, not real objects
        # so only indexed attributes are available.
        desc = folders[0].Description # OK
        folders[0].objectIds() # WRONG!
        folder = folders[0].getObject()
        folder.objectIds() # OK!

- to manipulate contents (create / delete / move / publish / etc.), example:

    .. code-block:: python

        new_page = context.api.content.create(
            type='Document',
            title='My Content',
            container=context.content)
        context.api.content.transition(obj=new_page, transition='publish')


- to access or manage the users and groups informations, and send emails. Example:

    .. code-block:: python

        current_user = context.api.user.get_current()
        context.api.portal.send_email(
            recipient=current_user.getProperty("email"),
            sender="noreply@plone.org",
            subject="Hello",
            body="World",
        )

For more detailed examples, refer to the `Plone API documentation <http://docs.plone.org/develop/plone.api/docs/index.html>`_.

``context.modules``
-------------------

.. warning:: For security reason, it is not allowed to import a Python module in a Rapido Python file.

Rapido provides some safe modules through ``context.modules``:

- ``context.modules.datetime``: `Basic date and time types <https://docs.python.org/2/library/datetime.html>`_,
- ``context.modules.random``: `Generate pseudo-random numbers <https://docs.python.org/2/library/random.html>`_,
- ``context.modules.time``: `Time access and conversions <https://docs.python.org/2/library/time.html>`_.

If we need to add extra modules to ``context.modules``, we can do it by adding in our own add-on something like:

.. code-block:: python

    import re
    from rapido.core import app

    app.safe_modules.re = re

In this example, we allow to access ``context.modules.re`` from our Rapido Python files.

Record
------

*Properties*

``url``
    Returns the record url.

``id``
    Returns the record identifier.

*Methods*

``display(self, edit=False)``
    Render the record using its associated block (if any).

``get(self, name, default=None)``
    Returns the value of the item (and defaults to ``default`` if the item does
    not exist).

``items(self)``
    Returns all the stored items.

``reindex(self)``
    Re-index the record.

``save(self, request=None, block=None, block_id=None, creation=False)``
    Update the record with the provided items and index it.

    ``request`` can be an actual HTTP request or a dictionnary.

    If a block is mentionned, formulas (``on_save``, computed elements, etc.)
    will be executed.

    If no block (and ``request`` is a dict), we just save the items values.

``set_block(self, block_id)``
    Assign a block to the record. The block will be then used to render the
    record or to save it.

*Python dictionary-like interface*

The record's items can be accessed and manipulated like dictionary items:

.. code-block:: python

    myrecord['fruit'] = "banana"
    for key in myrecord:
        context.app.log(myrecord[key])
    if 'vegetable' in myrecord:
        del myrecord['fruit']

.. note ::

    When setting an item value, the record is not reindexed.

Access control list
-------------------

.. note ::

    The application access control list can be obtain by ``context.app.acl``.

**Methods**

``current_user(self)``
    Returns the current user id.
    Equivalent to:

.. code-block:: python

    context.api.user.get_current().getUserName()

``current_user_groups(self)``
    Returns the groups the current user belongs to.
    Equivalent to:

.. code-block:: python

    api.user.get_current().getGroups()

``has_access_right(self, access_right)``
    Returns ``True`` if the current user has the specified access right (Rapido
    access rights are ``reader``, ``author``, ``editor``, ``manager``)

``has_role(self, role_id)``
    Returns ``True`` if the current user has the specified role.

``roles(self)``
    Returns the existing roles.
