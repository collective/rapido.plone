Blocks
======

A block is defined by 3 files stored in the ``blocks`` folder of the
application.
Those files have the same filename (which is the block id) with the extensions
.html, .py and .yaml.

The HTML file
-------------

The .html file contains the layout of the block. It is regular html, and dynamic
elements are enclosed in curly brackets. Example:

.. code-block:: html

    <p>This is a dynamic message: {message}</p>

The curly brackets will be replaced by the corresponding element value.

If the element is a BASIC element and returns an object, we can access its
properties. Example:

.. code-block:: html

    <h1>{my_doc.title}</h1>

Similarly, if a BASIC element returns a dictionnary, we can access its items.
Example:

.. code-block:: html

    <p>{info[user]} said: {info[comment]}</p>

When rendered, the block layout is wrapped in an HTML ``<form>`` element.

The layout can contain Mockup patterns markup, they will be rendered as
expected.

Some Mockup patterns might need to render actual curly brackets in the output,
we need to double them:

.. code-block:: html

    <a href="#modal" class="pat-plone-modal"
        data-pat-modal='{{"content": "form"}}'>Display modal</a>

Once rendered, if the block contains some links an `ajax` target:

.. code-block:: html

    <a href="@@rapido/record/1234" target="ajax">Open</a>

the request will be loaded in AJAX mode and its content will replace the current
block content.

The YAML file
-------------

The .yaml file contains:
- the elements settings (see below),
- the ``target`` option: if set to ``ajax``, any action in the block resulting in a
form submission will not redirect the current page, it will just refresh the 
block content through an AJAX call.

The Python file
---------------

The .py file contains the implementation of each element as a Python function
which name is the element id, and taking ``context`` as parameter.