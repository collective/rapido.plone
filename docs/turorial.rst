Rapido tutorial
===============

How to build a content rating system in Plone in 5 minutes

Objective
---------

We want to offer tor our visitors the ability to click on "Like" button on any
Plone content, and the total of votes must be displayed next to the button.

Prerequisites
-------------

Run buildout to deploy Rapido and its dependencies (see README).

Install the `rapido.plone` add-on from Plone site setup.

Initializing the Rapido app
---------------------------

We go to Plone Site setup, and then Theming.

If our current active theme is not editable inline through the Plone web
interface (i.e. there is no "Modify theme" button), we will first need to create
an editable copy:
- click on "Copy",
- enter a name,
- check "Immediately enable new theme".

Else, we just click on the "Modify theme" button.

We can see our theme structure, containing CSS files, images, HTML, and Diazo
rules.

To initialize our Rapido app named "rating", we need to:
- create a folder maned `rapido` in the theme root,
- in this `rapido` folder, create a folder named `rating`.

The application is now ready.

Creating the "Like" button
--------------------------

Rapido apps are composed of **blocks**. Let's create a block that will render
our button:
- go to the `rating` folder and create a new folder named `blocks`,
- in this `blocks` folder, let's create a new block named `rate`. It implies to
  create 3 files:

The `rate.html` file:

.. code:: html

    <i>If you like what you read, say it! {like}</i>

It allows us to implement the block layout. It is a regular HTML file, but it
may contain Rapido **elements**, enclosed in brackets. In our case, we have
one element, noted `{like}`, in charge of rendering the "Like" button.

The `rate.py` file

.. code:: python

    def like(context):
        # nothing for now
        pass

It provides the elements implementation. Each element in the blockhas a
corresponding Python function having the same id.
In our case, that is the code that will be executed when a user click on "Like".
Right now, it makes nothing, but we will change it later.

The `rate.yaml` file:

.. code:: yaml

    elements:
        like:
            type: ACTION
            label: Like

This file contains all the needed settings for our block. Here we declare our
block contains one element named `like`, which is an **action** (i.e. it will
be rendered as a button), and its displayed label is "Like".

Now our block is ready, we can see it using the following URL:

http://localhost:8080/Plone/@@rapido/rating/block/rate

The next step is to put our block in our Plone pages.

Inserting the block in Plone pages
----------------------------------

To include our block somewhere in Plone, we will use a Diazo rule.
Let's open our `rules.xml` file in the root of our theme, and add the following
lines:

.. code:: xml

    <after css:content=".documentFirstHeading">
        <include css:content="form" href="/@@rapido/rating/block/rate" />
    </after>

The `include` directive allows to retrieve a piece of content, in our case, the
HTML form produces by our block. And the `after` directive inserts it after the
main title in our page.

So, now if we visit any page of our Plone site, we see our block displayed just
under the title.

That is nice, but there is a small problem: when we like on the "Like" button,
we are redirected to the raw block content, and we loose our current Plone page.

let's fix that.

Keeping in our Plone page
-------------------------

If we want to keep in our current page after submitting our block, we need to
enable to **AJAX** mode.

Let's just change our `rate.yaml` file like this:

.. code:: yaml

    target: ajax
    elements:
        like:
            type: ACTION
            label: Like

Now, if we click on the "Like" button, the block is just reloaded dynamically,
and we keep in our current page.

Counting the votes
------------------

Let's go back to `rate.py`, and focus on the `like` function implementation.

When a user clicks on the "Like" button, we need to get the current content the
user voted for, check how many votes it already has, and add one new vote.

Rapido allows to create **records**, so we will create a record for each content
and we will use the content path as an id.

So let's repalce our current implementation with:

.. code:: python

    def like(context):
        content_path = context.content.absolute_url_path()
        record = context.app.get_record(content_path)
        if not record:
            record = context.app.create_record(id=content_path)
        total = record.get_item('total', 0)
        total += 1
        record.set_item('total', total)

`context.content` returns the current Plone content, and `absolute_url_path` is
a Plone method returning the path of a Plone object.

`context.app` allows to access to the current Rapido app, so we can easily use
the Rapido API, like `create_record` or `get_record`.

A Rapido record contains **items**. The `get_item(item, default=None)` method
returns the value of the requested item or the default value if the item does
not exist.

Displaying the votes
--------------------

We are able to store votes, we want now to display the total of votes.

Fist, let's change the block layout in `rate.html`:

.. code:: html

    <p>{display}</p>
    <p></p><i>If you like what you read, say it! {like}</i></p>

So we have now a new `display` element in our block.

Let's declare it in `rate.yaml`:

.. code:: yaml

    target: ajax
    elements:
        like:
            type: ACTION
            label: Like
        display:
            type: BASIC

And let's implement it in `rate.py`:

.. code:: python

    def display(context):
        content_path = context.content.absolute_url_path()
        record = context.app.get_record(content_path)
        if not record:
            return ''
        return "❤" * record.get_item('total', 0)

We get the record corresponding to the current content, and we return as many ❤
as votes we have stored.

That's it! Our rating feature is ready to be used.