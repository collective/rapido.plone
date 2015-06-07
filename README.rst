====================
rapido.plone
====================

**Happy hacking on Plone**

What for?
=========

Creating a small form able to send an email, or to store some data, generating
an extra information about a page and insert it wherever we want; with Plone
that kind of tasks are complex for experts, and almost impossible for beginners.

rapido.plone allows any developer having a little knowledge of HTML and a little
knowledge of Python to implement custom elements and insert them anywhere they
want in their Plone site.

How?
====

The unique interface to build applications with rapido.plone is the **Plone
theming tool**.

It implies it can be achieved in the *file system* (in the /static folder like
the rest of the theming elements), or through the theming *inline editor*.

The rapido applications are just a piece of the current theme, they can be
imported, exported, copied, modified, etc. like the rest of the theme.

Moreover, we will use Diazo extensively to inject our application in the Plone
layout.

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

The YAML file defines the fields. A field is any dynamically generated element
in a form, it can be an actual form fields (input, select, etc.), but also can
be a button (``ACTION``), or even just a piece of generated HTML (``BASIC``).

The HTML file contains the layout of the form. The templating mechanism is super
simple, fields are just enclosed in brackets, like this: ``{my_field}``.

The Python file contains functions which implement everything the form and its
fields might need. It can be many things.

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

It works fine, but where is our Plone site??

Inserting a form in a Plone page
================================

To put our form somewhere in the Plone site, we use a Diazo rule::

    <before css:content="#content-core">
        <include css:content="form" href="/@@rapido/myapp/forms/simpleform" />
    </before>

Now, if we visit any page of our site, we will see our form.
But unfortunately, when we click on our "Do something" button, we are redirected
to the original bare form.

To remain in the Plone page, we need to activate the ``AJAX`` target in
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