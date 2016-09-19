Elements
========

Declaration
-----------

Elements must be declared in the YAML file under the ``elements`` entry.
Every element is declared by its identifier, and its definition is:

- either a list of parameters, e.g.:

    .. code-block:: yaml

        elements:
            do_something:
                type: ACTION
                label: Do something

- either just a string, in that case Rapido will assume it is the ``type`` parameter, e.g.:

    .. code-block:: yaml

        elements:
            message: BASIC

    is equivalent to:

    .. code-block:: yaml

        elements:
            message:
                type: BASIC

Types
-----

There are different types of elements (defined by the ``type`` parameter):

- ``BASIC``: a piece of HTML returned by its implementation function.
- ``ACTION``: a button that will execute the implementation function when clicked.
  Its label is provided by the ``label`` parameter.
- ``TEXT``: a text input field.
- ``NUMBER``: a number input field.
- ``DATETIME``: a date/time input field.

Input elements
--------------

Input elements (i.e. ``TEXT``, ``NUMBER``, or ``DATETIME``) can be indexed as
``field`` or ``text``. Indexing is indicated using the ``index_type`` parameter.

By default input elements are editable but they might also have a different
``mode``:

- ``COMPUTED_ON_SAVE``: the value is computed everytime the record is saved,
- ``COMPUTED_ON_CREATION``: the value is computed when the record is created.

Action elements
---------------

Action elements are rendered as submit buttons and allow to trigger a call to an associated Python function.

If the function returns a value, it must be a string, and it will be used as a redirection URL for the current request.

It is way to redirect to another location once the action has been executed.

Builtin actions
---------------

The following actions can be included in our block HTML layout, and they will not require an associated Python function:

- ``_save``: will create a record based on the field elements submitted values and then redirect to the record display in read mode;
- ``_edit``: will open the current record in edit mode;
- ``_delete``: will delete the current record.

Direct HTTP call to elements
----------------------------

We usually want to display blocks, but we can also call an element by its URL::

    http://localhost:8080/Plone/@@rapido/myapp/blocks/block1/element1

Both GET and POST request are supported.

If the element is an action, its Python function will be executed, the returned value is supposed to be a string and will be used as a redirection URL.
When building an application, it allows to create a link that will redirect the user to the proper location depending on our business criteria (e.g. if the user belongs to such group, go to page1, else go to page2).

If the element is not an action, its Python function will be executed, and the result is returned as a response.

.. note ::
    
    We can change the response content type like this:

    .. code-block:: python

        def my_element(context):
            context.request.reponse.setHeader('content-type', 'text/csv')
            return "one,two,three\n1,2,3"
