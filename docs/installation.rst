Installation
============

Install Plone, then modify ``buildout.cfg`` to add Rapido as a dependency::

    eggs =
        ...
        rapido.plone

Rapido packages are not released yet, so for now, we need to checkout the
following repositories::

    auto-checkout =
        rapido.core
        rapido.plone
        rapido.souper

    [sources]
    rapido.core = git https://github.com/plomino/rapido.core.git
    rapido.plone = git https://github.com/plomino/rapido.plone.git
    rapido.souper = git https://github.com/plomino/rapido.souper.git

    # IF PLONE 5.0 (useless with >= 5.0.1)
    [versions]
    diazo = 1.2.2

Then, run your buildout::

    $ bin/buildout -N
