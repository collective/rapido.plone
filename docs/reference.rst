Rapido reference
================

Application
-----------

A Rapido application is defined by a folder in the ``rapido`` folder in the
current theme.

The application folder might contain a ``settings.yaml`` file in its root to
define its access control settings (see below), but that is not mandatory.

It always contain a ``blocks`` folder containing its blocks (see below).

It might also contain regular theme items (rules.xml, CSS, Javascript, etc.).

Blocks
------

A block is defined by 3 files stored in the ``blocks`` folder of the
application.
Those files have the same filename (which is the block id) with the extensions
.html, .py and .yaml.

The .html file contains the layout of the block. It is regular html, and dynamic
elements are enclosed in brackets. Example:

.. code-block:: html

    <p>This is a dynamic message: {message}</p>

When rendered, the block layout is wrapped in an HTML ``<form>`` element.

Note: the layout can contain Mockup patterns markup, they will be rendered as
expected.

The .yaml file contains:
- the elements settings (see below),
- the ``target`` option: if set to ``ajax``, any action in the block resulting in a
form submission will not redirect the current page, it will just refresh the 
block content through an AJAX call.

The .py file contains the implementation of each element as a Python function
which name is the element id, and taking ``context`` as parameter.

Elements
--------

There are different types of elements (defined by the ``type`` parameter):

- ``BASIC``: a piece of HTML returned by its implementation function.
- ``ACTION``: a button that will execute the implementation function when clicked.
  Its label is provided by the ``label`` parameter.
- ``TEXT``: a text input field.
- ``NUMBER``: a number input field.
- ``DATETIME``: a date/time input field.

Input elements (i.e. ``TEXT``, ``NUMBER``, or ``DATETIME``) can be indexed as
``field`` or ``text``. Indexing is indicated using the ``index_type`` parameter.

 By default input elements are editable but they might also have a different
 ``mode``:

- ``COMPUTED_ON_SAVE``: the value is computed everytime the record is saved,
- ``COMPUTED_ON_CREATION``: the value is computed when the record is created.

Records
-------

Rapido records can be created by saving a block containing field elements.
the value of each submitted elements will be stored in corresponding items.

In that case, the record has an associated block (the block id is stored in an
item named ``block``), when the record is rendered for display (when we load its
URL in our browser), it uses the block layout.

Records can also be created manually (without any associated block) using the
Python API or the REST API. Such records cannot be rendered automatically by
calling their URL, but their items values can be used in a block if we know how
to find the record (in the :doc:`./tutorial` for instance, our records are
created manually from the ``like`` function, they are not associated to the
``rate`` block, but we use the stored items to produce our elements content).

Associated Python functions
---------------------------

For a ``BASIC`` element, the associated Python function (having the same id)
will return the content of the element.

For field elements (``TEXT``, ``NUMBER``, ``DATETIME``), the associated Python
function will return its default value.

For an ``ACTION`` element, the associated Python function will be executed when
the action is triggered.

Specific actions
----------------

The following actions can included in our block HTML layout, and they will not
require an associated Python function:

- ``_save``: will create a record based on the field elements submitted values
  and then redirect to the record display in read mode;
- ``_edit``: will open the current record in edit mode;
- ``_delete``: will delete the current record.

Specific Python functions
-------------------------

``on_save``
    Executed when a record is saved with the block.

``on_delete``
    Executed when a record is deleted.

``record_id``
    Executed at creation time to compute the record id.

``title``
    Executed when a record is saved to compute the record ``title`` item.

Indexing and searching
----------------------

The Rapido storage system (`souper <https://github.com/bluedynamics/souper>`_)
supports indexing.

Any block element can be indexed by adding a ``index_type`` setting in its YAML
definition.

The ``index_type`` setting can have two possible values:

- ``field``: such index matches exact values, and support comparison queries,
  range queries, and sorting.
- ``text``: such index matches contained words (applicable for text values only).

Queries use the *CQE format* (`see documentation <http://docs.repoze.org/catalog/usage.html#query-objects>`_.

Example (assuming `author`, `title` and `price` are existing indexes):

..code:: python

    context.app.search(
        "author == 'Conrad' and 'Lord Jim' in title",
        sort_index="price")

Records are indexed at the time they are saved. We can force reindexing using
the Python API:

..code:: python

    myrecord.reindex()

We can also reindex all the records using the ``refresh`` URL command::

    http://localhost:8080/Plone/@@rapido/<app-id>/refresh

or using the REST API (see :doc:`./rest`).

Import/export
-------------

Access control
--------------

The access control settings are managed in the ``settings.yaml`` file in the app
root folder.

The expected format is:

.. code-block:: yaml

    acl:
      rights:
        author: [<list of users or groups>]
        editor: [<list of users or groups>]
        manager: [<list of users or groups>]
        reader: [<list of users or groups>]
      roles: {<role_id>: [<list of users or groups>]}

Content rules
-------------

Mosaic
------