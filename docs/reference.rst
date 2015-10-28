Rapido reference
================

Application
-----------

A Rapido application is defined by a folder in the `rapido` folder in the
current theme.

The application folder might contain a `settings.yaml` file in its root to
define its access control settings (see below), but that is not mandatory.

It always contain a `blocks` folder containing its blocks (see below).

It might also contain regular theme items (rules.xml, CSS, Javascript, etc.).

Blocks
------

A block is defined by 3 files stored in the `blocks` folder of the application.
Those files have the same filename (which is the block id) with the extensions
.html, .py and .yaml.

The .html file contains the layout of the block. It is regular html, and dynamic
elements are enclosed in brackets. Example:

.. code-block:: html

    <p>This is a dynamic message: {message}</p>

When rendered, the block layout is wrapped in an HTML `<form>` element.

Note: the layout can contain Mockup patterns markup, they will be rendered as
expected.

The .yaml file contains:
- the elements settings (see below),
- the `target` option: if set to `ajax`, any action in the block resulting in a
form submission will not redirect the current page, it will just refresh the 
block content through an AJAX call.

The .py file contains the implementation of each element as a Python function
which name is the element id, and taking `context` as parameter.

Elements
--------

There are different types of elements (defined by the `type` parameter):

- `BASIC`: a piece of HTML returned by its implementation function.
- `ACTION`: a button that will execute the implementation function when clicked.
  Its label is provided by the `label` parameter.
- `TEXT`: a text input field.
- `NUMBER`: a number input field.
- `DATETIME`: a date/time input field.

Input elements (i.e. `TEXT`, `NUMBER`, or `DATETIME`) can be indexed as `field`
(matching exact value, and allowing sorting and compairison), or `text` (
indexing words). Indexing is indicated using the `index_type` parameter.

Python API
----------

Specific actions
----------------

Specific Python functions
-------------------------

REST API
--------

Import/export
-------------

Access control
--------------

The access control settings are managed in the `settings.yaml` file in the app
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