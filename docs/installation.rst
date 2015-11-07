Installation
============

Install Plone, then modify ``buildout.cfg`` to add Rapido as a dependency::

    eggs =
        ...
        rapido.plone

rapido.plone is not released yet, so for now, we need to checkout its repository::

    auto-checkout =
        rapido.plone

    [sources]
    rapido.plone = git https://github.com/plomino/rapido.plone.git

    # IF PLONE 5.0 (useless with >= 5.0.1)
    [versions]
    diazo = 1.2.2

Then, run your buildout::

    $ bin/buildout -N
