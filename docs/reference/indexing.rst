Indexing and searching
======================

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

.. code-block:: python

    context.app.search(
        "author == 'Conrad' and 'Lord Jim' in title",
        sort_index="price")

Records are indexed at the time they are saved. We can force reindexing using
the Python API:

.. code-block:: python

    myrecord.reindex()

We can also reindex all the records using the ``refresh`` URL command::

    http://localhost:8080/Plone/@@rapido/<app-id>/refresh

or using the REST API (see :doc:`../rest`).
