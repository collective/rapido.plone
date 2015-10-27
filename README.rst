====================
rapido.plone
====================

**Happy hacking on Plone**

|travisstatus|_

.. |travisstatus| image:: https://secure.travis-ci.org/plomino/rapido.plone.png?branch=master
.. _travisstatus:  http://travis-ci.org/plomino/rapido.plone

What for?
=========

Creating a small form able to send an email, or to store some data, generating
an extra information about a page and insert it wherever we want; with Plone
that kind of tasks are complex for experts, and almost impossible for beginners.

**rapido.plone** allows any developer having a little knowledge of HTML and a
little knowledge of Python to implement custom elements and insert them anywhere
they want in their Plone site.

How?
====

The unique interface to build applications with rapido.plone is the **Plone
theming tool**.

It implies it can be achieved in the *file system* (in the /static folder like
the rest of the theming elements), or through the theming *inline editor*.

A Rapido applications are just a piece of our current theme, it can be
imported, exported, copied, modified, etc. like the rest of the theme.

Moreover, we can use `Diazo <http://docs.diazo.org/en/latest/>`_ extensively to
inject our application in the Plone layout easily.

Creating a Rapido app
=====================

Here are the basic steps to create a Rapido app:

- go to the theme folder (``static`` folder in the theme module if we want to
  work in thefile system, or in Plone setup / Theme if we prefer inline),
- add a new folder named ``rapido``,
- in ``rapido``, add a new folder named ``myapp``.

That's it.

Now, we can implement our application in this folder.
Here is a typical layout for a rapido app::

    /rapido
        /myapp
            settings.yaml
            /blocks
                stats.html
                stats.py
                stats.yaml
                tags.html
                tags.py
                tags.yaml

Note: ``settings.yaml`` is not mandatory, it allows to define access rights if
needed.

The app components are `blocks`. A block is defined by a set of 3 files (HTML,
Python, and YAML files) located in the ``blocks`` folder.

The **YAML file** defines the elements. An element is any dynamically generated
element in a block, it can be a form field (input, select, etc.), but
also a button (``ACTION``), or even just a piece of generated HTML (``BASIC``).

The **HTML file** contains the layout of the block. The templating mechanism is
super simple, elements are just enclosed in brackets, like this:
``{my_element}``.

The **Python file** contains the application logic. It is a set of functions
which names refer to the element or the event they are related to.

For a ``BASIC`` element for instance, we are supposed to provide a function having
the same name as the element, its returned value will be inserted in the block at
the location of the element.

For an ``ACTION``, we are supposed to provide a function having the same name as
the element, it will be executed when a user clicks on the action button.

Here is a basic example:

- rapido/myapp/blocks/simpleblock.yaml::

    id: simpleblock
    title: A simple block
    elements:
        result:
            type: BASIC
        do_something:
            type: ACTION
            label: Do something

- rapido/myapp/blocks/simpleblock.html::

    <p>the answer to life, the universe, and everything is {result}</p>
    {do_something}

- rapido/myapp/blocks/simpleblock.py::

    def result(context):
        return "<strong>42</strong>"

    def do_something(context):
        context.portal.plone_log("Hello")

We can see our block by visiting the following URL::

    http://localhost:8080/Plone/@@rapido/myapp/blocks/simpleblock

It works fine, but where is our Plone site now??

Inserting a block in a Plone page
================================

To put our block somewhere in the Plone site, we use a Diazo rule::

    <before css:content="#content-core">
        <include css:content="form" href="/@@rapido/myapp/block/simpleblock" />
    </before>

Now, if we visit any page of our site, we will see our block.
But unfortunately, when we click on our "Do something" button, we are redirected
to the original bare block.

To remain in the Plone page, we need to activate the ``ajax`` target in
rapido/myapp/blocks/simpleblock.yaml::

    id: simpleblock
    title: A simple block
    target: ajax
    elements:
        result:
            type: BASIC
        do_something:
            type: ACTION
            label: Do something

Now, when we click our button, the rapido block is reloaded inside the Plone
page.

Instead of adding a block to an existing Plone view, we might need to provide a
new rendering, answering for a specific URL.
We can do that by adding ``@@rapido/view`` to the content URL. It will just
display the default view of our content, but it allows us to define a specific
Diazo rule for this path::

    <rules if-path="@@rapido/view">
        <replace css:content="#content">
            <include css:content="form" href="/@@rapido/myapp/block/simpleblock" />
        </replace>      
    </rules>

We might add an extra name to our path, which will be ignored in term of
rendering, but it will allow us to define different rules for different use
cases (like ``path_to_content/@@rapido/view/subscribe``, ``path_to_content/@@rapido/view/unsubscribe``, ``path_to_content/@@rapido/view/stats``, ...).

Note: adding a lot of rapido rules in our main ``rules.xml`` is not ideal.
We might prefer to create a ``rules.xml`` file into our ``rapido/myapp``
folder, and include it in our main ``rules.xml`` file like this::

    <xi:include href="rapido/myapp/rules.xml" />


Running Python code
===================

Every function in our Python files takes a parameter named ``context``.
The context gives access to useful objects:

- ``context.app``: the current rapido app,
- ``context.request``: the current request to rapido (the sub-request, if called
  from Diazo),
- ``context.parent_request``: the current page request (when called from Diazo),
- ``context.portal``: the Plone portal object,
- ``context.content``: the current Plone content object,
- ``context.api``: the `Plone API
  <http://docs.plone.org/external/plone.api/docs/>`_.

It allows us to interact with Plone in very various ways, for instance we can
run catalog queries, create contents, change workflow status, etc.

Nevertheless, it will behave as expected:

- the code will always be executed with the current user access right, so the
  appropriate Plone access restrictions will be applied,
- the CSRF policy will also be applied (for instance, a Plone operation marked
  as ``PostOnly`` would fail if performed in a GET request).

Note: The code we put in our Python files is compiled and executed in a
sandboxed environment (provided by `zope.untrustedpython.interpreter 
<https://github.com/zopefoundation/zope.untrustedpython/blob/master/docs/narr.rst>`_).

Storing and retrieving data
===========================

A rapido app provides a builtin storage service, based on
`Souper <https://pypi.python.org/pypi/souper>`_.

Note: Souper is designed to store (and index) huge amounts of small data (it can
easily store survey results, comments, ratings, etc., but it will not be
appropriate for attached files for instance)

The Rapido storage service stores **records**, and records contain **items**.

There are 3 ways to create records in Rapido:
- we can create records by submitting a block: if a
  block contain some fields elements (like `TEXT` or `NUMBER` elements for
  instance), and if the block contains a save button (by adding `{_save}` in its
  layout), everytime the user will enter values in the fields and click save,
  the submitted values will be saved in a new record,
- we can create records by code::
    
    record = context.app.create_record(id='myrecord')

- we can create records using the Rapido JSON REST API::

    POST /:site_id/@@rapido/:app_id
    Accept: application/json
    {'item1': 'value1'}

  or::

    PUT /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json
    {'item1': 'value1'}

The same goes for accessing data:
- we can display records by calling their URL, and they will be rendered using
  the block they have been created with:

    /@@rapido/myapp/record/myrecord

- we can get a record by code::

    record = context.app.get_record(id='myrecord')
    some_records = context.app.search('author=="JOSEPH CONRAD"')

- we can get records using the Rapido JSON REST API::

    GET /:site_id/@@rapido/:app_id/record/:record_id
    Accept: application/json

Integration in Plone
====================

In addition to the Diazo injection of Rapido blocks in our theme, we can also
integrate our Rapido developments in Plone using:

- Mosaic: Rapido provides a Mosaic tile which enable to insert a Rapido block in
  our page layout.

- Content Rules: Rapido provides a Plone content rule action allowing to call a
  Python function from a block when a given Plone event happens.


Installation
============

Rapido packages are not released yet, plus it depends on an unmerged PR in
Diazo.
So for now, we need to checkout the following repositories::

    eggs =
        ...
        rapido.plone

    auto-checkout =
        rapido.core
        rapido.plone
        rapido.souper
        diazo

    [sources]
    rapido.core = git https://github.com/plomino/rapido.core.git
    rapido.plone = git https://github.com/plomino/rapido.plone.git
    rapido.souper = git https://github.com/plomino/rapido.souper.git
    diazo = git https://github.com/plone/diazo.git branch=include-content-refactor