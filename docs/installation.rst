Installation
============

Install Plone, then modify ``buildout.cfg`` to add Rapido as a dependency::

    eggs =
        ...
        rapido.plone

    # IF PLONE 5.0 (useless with >= 5.0.1)
    [versions]
    diazo = 1.2.2

Then, run your buildout::

    $ bin/buildout -N
