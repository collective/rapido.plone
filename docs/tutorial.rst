Tutorial
========

How to build a content rating system in Plone in few minutes.

Objective
---------

We want to offer to our visitors the ability to click on "Like" button on any
Plone content, and the total of votes must be displayed next to the button.

Prerequisites
-------------

Run buildout to deploy Rapido and its dependencies (see :doc:`./installation`).

Install the ``rapido.plone`` add-on from Plone site setup.

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

- create a folder maned ``rapido`` in the theme root,
- in this ``rapido`` folder, create a folder named ``rating``.

The application is now ready.

Creating the "Like" button
--------------------------

Rapido apps are composed of **blocks**. Let's create a block that will render
our button:

- go to the ``rating`` folder and create a new folder named ``blocks``,
- in this ``blocks`` folder, let's create a new block named ``rate``. It implies to
  create 3 files:

The ``rate.html`` file:

.. code-block:: html

    <i>If you like what you read, say it! {like}</i>

It allows us to implement the block layout. It is a regular HTML file, but it
may contain Rapido **elements**, enclosed in brackets. In our case, we have
one element, noted ``{like}``, in charge of rendering the "Like" button.

The ``rate.py`` file

.. code-block:: python

    def like(context):
        # nothing for now
        pass

It provides the elements implementation. Each element in the blockhas a
corresponding Python function having the same id.
In our case, that is the code that will be executed when a user click on "Like".
Right now, it makes nothing, but we will change it later.

The ``rate.yaml`` file:

.. code-block:: yaml

    elements:
        like:
            type: ACTION
            label: Like

This file contains all the needed settings for our block. Here we declare our
block contains one element named ``like``, which is an **action** (i.e. it will
be rendered as a button), and its displayed label is "Like".

Now our block is ready, we can see it using the following URL:

http://localhost:8080/Plone/@@rapido/rating/block/rate

The next step is to put our block in our Plone pages.

Inserting the block in Plone pages
----------------------------------

To include our block somewhere in Plone, we will use a Diazo rule.
Let's open our ``rules.xml`` file in the root of our theme, and add the following
lines:

.. code-block:: xml

    <after css:content=".documentFirstHeading">
        <include css:content="form" href="/@@rapido/rating/block/rate" />
    </after>

The ``include`` directive allows to retrieve a piece of content, in our case, the
HTML form produces by our block. And the ``after`` directive inserts it after the
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

Let's just change our ``rate.yaml`` file like this:

.. code-block:: yaml

    target: ajax
    elements:
        like:
            type: ACTION
            label: Like

Now, if we click on the "Like" button, the block is just reloaded dynamically,
and we keep in our current page.

Counting the votes
------------------

Let's go back to ``rate.py``, and focus on the ``like`` function implementation.

When a user clicks on the "Like" button, we need to get the current content the
user voted for, check how many votes it already has, and add one new vote.

Rapido allows to create **records**, so we will create a record for each content
and we will use the content path as an id.

So let's repalce our current implementation with:

.. code-block:: python

    def like(context):
        content_path = context.content.absolute_url_path()
        record = context.app.get_record(content_path)
        if not record:
            record = context.app.create_record(id=content_path)
        total = record.get_item('total', 0)
        total += 1
        record.set_item('total', total)

``context.content`` returns the current Plone content, and ``absolute_url_path`` is
a Plone method returning the path of a Plone object.

``context.app`` allows to access to the current Rapido app, so we can easily use
the Rapido API, like ``create_record`` or ``get_record``.

A Rapido record contains **items**. The ``get_item(item, default=none)`` method
returns the value of the requested item or the default value if the item does
not exist.

Displaying the votes
--------------------

We are able to store votes, we want now to display the total of votes.

Fist, let's change the block layout in ``rate.html``:

.. code-block:: html

    <p>{display}</p>
    <p><i>If you like what you read, say it! {like}</i></p>

So we have now a new ``display`` element in our block.

We must declare it in ``rate.yaml``:

.. code-block:: yaml

    target: ajax
    elements:
        like:
            type: ACTION
            label: Like
        display:
            type: BASIC

And let's implement it in ``rate.py``:

.. code-block:: python

    def display(context):
        content_path = context.content.absolute_url_path()
        record = context.app.get_record(content_path)
        if not record:
            return ''
        return "❤" * record.get_item('total', 0)

We get the record corresponding to the current content, and we return as many ❤
as votes we have stored.

That's it! Our rating feature is ready to be used.

Listing the top 5 contents
--------------------------

We would also like to see the top 5 rated contents on the site home page.

First we need is to index the ``total`` element.

We declare its indexing mode in ``rate.yaml``:

.. code-block:: yaml

    target: ajax
        elements:
            like:
                type: ACTION
                label: Like
            display:
                type: BASIC
            total:
                type: NUMBER
                index_type: field

And then we have to refresh the storage index by calling the following URL::

    http://localhost:8080/Plone/@@rapido/rating/refresh

We are now able to build a block to display the top 5 contents:

- ``top5.html``:

.. code-block:: html

    <h3>Our current Top 5!</h3>
    {top}

- ``top5.yaml``:

.. code-block:: yaml

    elements:
        top:
            type: BASIC

- ``top5.py``:

.. code-block:: python

    def top(context):
        search = context.app.search("total>0", sort_index="total", reverse=True)[:5]
        html = "<ul>"
        for record in search:
            content = context.api.content.get(path=record.get_item("id"))
            html += '<li><a href="%s">%s</a> %d ❤</li>' % (
                content.absolute_url(),
                content.title,
                record.get_item("total")) 
        html += "</ul>"
        return html

The ``search`` method allows to query our stored records. The record ids are
the contents pathes, so using the Plone API (``context.api``), we can easily
get the corresponding contents, and then obtain their URLs and titles.

Our block works now::

    http://localhost:8080/tutorial/@@rapido/rating/block/top5

Finally, we have to insert our block in the home page. That will be done in
``rules.xml``:

.. code-block:: xml

    <rules css:if-content=".section-front-page">
        <before css:content=".documentFirstHeading">
            <include css:content="form" href="/@@rapido/rating/block/top5" />
        </before>
    </rules>

Creating a new page for reports
-------------------------------

For now, we have just added small chuncks of HTML in existing pages. But Rapido
also allows to create a new page (a Plone developer would name it a new `view`).

Let's imagine we want to create a report page about a folder's contents votes.

First, we need a block, ``report.html``:

.. code-block:: html

    <h2>Rating report</h2>
    <div id="chart"></div>

We want this block to be the main content of a new view.    
We will do that with a **neutral view** (see :doc:`./reference/display`).
By adding ``@@rapido/view/<any-name>`` to a content URL we get the content's
default view, and using a Diazo rule, we will replace the default content with
our block:

.. code-block:: xml

    <rules if-path="@@rapido/view/show-report">
        <replace css:content="#content">
            <include css:content="form" href="/@@rapido/rating/block/report" />
        </replace>      
    </rules>

Now if we visit for instance::

    http://localhost:8080/tutorial/news/@@rapido/view/show-report

we do see our block instead of the regular News page content.

Now we need to implement our report content. We could do it with a Rapido element
like we did in the Top 5 block.

Let's change our approach and implement a fancy pie chart using the `amazing D3js library <http://d3js.org/>`_ and the :doc:`Rapido REST API <./rest>`.

We need to create a Javascript file (``report.js``) in the ``/rapido/rating``
folder:

.. code-block:: javascript

    require(['mockup-utils', '//d3js.org/d3.v3.min.js'], function(utils, d3) {
        var authenticator = utils.getAuthenticator();
        var local_folder_path = location.pathname.split('/@@rapido')[0];
        var width = 960,
            height = 500,
            radius = Math.min(width, height) / 2;
        
        var arc = d3.svg.arc()
            .outerRadius(radius - 10)
            .innerRadius(0);
        
        var pie = d3.layout.pie()
            .sort(null)
            .value(function(d) { return d.value; });
        
        var svg = d3.select("#chart").append("svg")
            .attr("width", width)
            .attr("height", height)
          .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        d3.json("../../@@rapido/rating/search")
        .header("X-Csrf-Token", authenticator)
        .post(
            JSON.stringify({"query": "total>0"}),
            function(err, results) {
                console.log(results);
                var data = [];
                var color = d3.scale.linear().domain([0,results.length]).range(["#005880","#9abdd6"]);
                var index = 0;
                results.forEach(function(d) {
                    if(d.items.id.startsWith(local_folder_path)) {
                        var label = d.items.id.split('/')[d.items.id.split('/').length - 1];
                        data.push({
                            'i': index,
                            'value': d.items.total,
                            'label': label
                        });
                        index += 1;
                    }
                });
                var g = svg.selectAll(".arc")
                  .data(pie(data))
                .enter().append("g")
                  .attr("class", "arc");
                
                g.append("path")
                  .attr("d", arc)
                  .style("fill", function(d) { return color(d.data.i); });
                
                g.append("text")
                  .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
                  .attr("dy", ".35em")
                  .style("text-anchor", "middle")
                  .text(function(d) { return d.data.label; })
                  .style("fill", "white");
            }
        );
    });

That is a quite complex script, and we will not detailed here the D3js related
aspects (it is just a typical example to draw a pie chart), but we will focus on
the way we obtain the data.

The first thing to notice is the ``require`` function, it is a feature of the
RequireJS library (provided with Plone be default) to load our dependencies.

We have 2 dependencies:

- ``mockup-utils``, which is a Plone internal resource,
- D3js (and we load it by passing its remote URL to RequireJS).

``mockup-utils`` allows us to get the authenticator token (with the ``getAuthenticator``
method), we need it to use the Rapido REST API.

Notes:

- RequireJS or ``mockup-utils`` are not mandatory to use the Rapido REST API,
  if we were outside of Plone (using Rapido as a remote backend), we would have made
  a call to /tutorial/@@rapido/rating which returns the token in an HTTP header.
  We just use them because they are provided by Plone by default, and they make our
  work easier.
- Instead of loading D3 directly form its CDN, we could have put the ``d3.v3.min.js``
  in the ``/rapido/rating`` folder, and serve it locally.

The second interesting part is the ``d3.json()`` call:

- it calls the ``@@rapido/rating/search`` endpoint,
- it puts the authenticator token in the ``X-Csrf-Token`` header,
- and it passes the search query in the request BODY.

That is basically what we need to do whatever JS framework we would use (here we
use D3, but it could be a generalist framework like Angular, Backbone, Ember, etc.).


Now we just need to load this script from our block:

.. code-block:: html

    <h2>Rating report</h2>
    <div id="chart"></div>
    <script src="++theme++test/rapido/rating/report.js"></script>

And we can visit::

    http://localhost:8080/tutorial/news/@@rapido/view/show-report

to see a pie chart about the News items votes!!

Download the :download:`source files of this tutorial <files/tutorial.zip>`.