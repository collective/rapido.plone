Installation
============

Install Plone, then modify ``buildout.cfg`` to add Rapido as a dependency::

    eggs =
        ...
        rapido.plone

    [versions]
    plone.resource = 1.2

Then, run your buildout::

    $ bin/buildout -N
