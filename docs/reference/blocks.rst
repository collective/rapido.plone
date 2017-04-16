Blocks
======

A block is defined by 3 files stored in the ``blocks`` folder of the
application.
Those files have the same filename (which is the block id) with the extensions
``.html``, ``.py`` and ``.yaml``.

The HTML file
-------------

The ``.html`` file contains the layout of the block. It is regular HTML. 
Dynamic elements are enclosed in curly brackets. Example:

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

Some Mockup patterns might need to render actual curly brackets in the output.
Double them to escape them:

.. code-block:: html

    <a href="#modal" class="pat-plone-modal"
        data-pat-modal='{{"content": "form"}}'>Display modal</a>

Once rendered, if the block contains some links with an ``ajax`` target:

.. code-block:: html

    <a href="@@rapido/record/1234" target="ajax">Open</a>

the request will be loaded in AJAX mode and its content will replace the current
block content.

TAL template
^^^^^^^^^^^^

The HTML template only offers element insertion. If we need more templating
features, the ``.html`` file can be replaced by a ``.pt`` file, and we can use the
`TAL commands <http://www.owlfish.com/software/simpleTAL/tal-guide.html>`_.

In the context of a Page Template, the block elements are available in the
``elements`` object:

.. code-block:: python

    def my_title(context):
        return "Chapter 1"

.. code-block:: html

    <h1 tal:content="elements/my_title"></h1>

Elements can be used as conditions:

.. code-block:: python

    def is_footer(context):
        return True

.. code-block:: html

    <footer tal:condition="elements/is_footer">My footer</footer>

If an element returns an iterable object (list, dictionary), we can make a loop:

.. code-block:: python

    def links(context):
        return [
            {'url': 'https://validator.w3.org/', 'title': 'Markup Validation Service'},
            {'url': 'https://www.w3.org/Style/CSS/', 'title': 'CSS'},
        ]

.. code-block:: html

    <ul>
        <li tal:repeat="link elements/links">
            <a tal:attributes="link/url"
                tal:content="link/title"></a>
        </li>
    </ul>

The current Rapido context is available in the ``context`` object:

.. code-block:: html

    <h1 tal:content="context/content/title"></h1>

The YAML file
-------------

The ``.yaml`` file contains:
- the elements settings (see below),

- the ``target`` option: if set to ``ajax``, any action in the block resulting in a
  form submission will not redirect the current page, it will just refresh the 
  block content through an AJAX call,

- the ``view_permission`` to manage who can see the block (see :doc:`./access`).

The Python file
---------------

The ``.py`` file contains the implementation of each element as a Python function
which name is the element id, and taking ``context`` as parameter.
