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

The rapido applications are just a piece of our current theme, they can be
imported, exported, copied, modified, etc. like the rest of the theme.

Moreover, we can use `Diazo <http://docs.diazo.org/en/latest/>`_ extensively to
inject our application in the Plone layout easily.

Creating a rapido app
=====================

Here are the basic steps to create a rapido app:

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
            /forms
                stats.html
                stats.py
                stats.yaml
                tags.html
                tags.py
                tags.yaml

Note: ``settings.yaml`` is not mandatory, it allows to define access rights if
needed.

The app building blocks are `forms`. A form is a set of 3 files (HTML, Python,
and YAML files) located in the ``forms`` folder.

The **YAML file** defines the fields. A field is any dynamically generated
element in a form, it can be an actual form fields (input, select, etc.), but
also a button (``ACTION``), or even just a piece of generated HTML (``BASIC``).

The **HTML file** contains the layout of the form. The templating mechanism is
super simple, fields are just enclosed in brackets, like this: ``{my_field}``.

The **Python file** contains the application logic. It is a set of functions
which names refer to the field or the event they are related to.

For a ``BASIC`` field for instance, we are supposed to provide a function having
the same name as the field, its returned value will be inserted in the form at
the location of the field.

For an ``ACTION``, we are supposed to provide a function having the same name as
the field, it will be executed when a user clicks on the action button.

Here is a basic example:

- rapido/myapp/forms/simpleform.yaml::

    id: simpleform
    title: A simple form
    fields:
        result:
            type: BASIC
        do_something:
            type: ACTION
            label: Do something

- rapido/myapp/forms/simpleform.html::

    <p>the answer to life, the universe, and everything is {result}</p>
    {do_something}

- rapido/myapp/forms/simpleform.py::

    def result(context):
        return "<strong>42</strong>"

    def do_something(context):
        context.portal.plone_log("Hello")

We can see our form by visiting the following URL::

    http://localhost:8080/Plone/@@rapido/myapp/forms/simpleform

It works fine, but where is our Plone site now??

Inserting a form in a Plone page
================================

To put our form somewhere in the Plone site, we use a Diazo rule::

    <before css:content="#content-core">
        <include css:content="form" href="/@@rapido/myapp/form/simpleform" />
    </before>

Now, if we visit any page of our site, we will see our form.
But unfortunately, when we click on our "Do something" button, we are redirected
to the original bare form.

To remain in the Plone page, we need to activate the ``ajax`` target in
rapido/myapp/forms/simpleform.yaml::

    id: simpleform
    title: A simple form
    target: ajax
    fields:
        result:
            type: BASIC
        do_something:
            type: ACTION
            label: Do something

Now, when we click our button, the rapido form is reloaded inside the Plone
page.

Instead of adding a form to an existing Plone view, we might need to provide a
new rendering, answering for a specific URL.
We can do that by adding ``@@rapido/view`` to the content URL. it will just
display the default view of our content, but it allows us to define a specific
Diazo rule for this path::

    <rules if-path="@@rapido/view">
        <replace css:content="#content">
            <include css:content="form" href="/@@rapido/myapp/form/simpleform" />
        </replace>      
    </rules>

We might add an extra name to our path, which will be ignored in term of
rendering, but it will allow us to define different rules for different use
cases (like ``path_to_content/@@rapido/view/subscribe``, ``path_to_content/@@rapido/view/unsubscribe``, ``path_to_content/@@rapido/view/stats``, ...).

Note: adding a lot of rapido rules in our main ``rules.xml`` is not ideal.
We might prefer to create a ``rules.xml`` file into our ``rapido/myapp``
folder, and include in in our main ``rules.xml`` file like this::

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