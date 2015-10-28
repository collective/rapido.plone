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

A Rapido application is just a piece of our current theme, it can be
imported, exported, copied, modified, etc. like the rest of the theme.

Moreover, we can use `Diazo <http://docs.diazo.org/en/latest/>`_ extensively to
inject our application in the Plone layout easily.

Documentation
=============

See the full `Rapido documentation <http://http://rapido.readthedocs.org/en/latest/>`_.