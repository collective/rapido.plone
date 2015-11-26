Elements
========

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

If the action function returns a value, it must be a string, and it will be used
as a redirection URL for the current request.

It is way to redirect to another location once the action has been executed.
