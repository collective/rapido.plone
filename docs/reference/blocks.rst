Blocks
======

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