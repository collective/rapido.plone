Installation
============

Install Plone, then modify ``buildout.cfg`` to add Rapido as a dependency::

    eggs =
        ...
        rapido.plone

Rapido packages are not released yet, plus it depends on an unreleased
Diazo feature.
So for now, we need to checkout the following repositories::

    auto-checkout =
        rapido.core
        rapido.plone
        rapido.souper
        diazo

    [sources]
    rapido.core = git https://github.com/plomino/rapido.core.git
    rapido.plone = git https://github.com/plomino/rapido.plone.git
    rapido.souper = git https://github.com/plomino/rapido.souper.git
    diazo = git https://github.com/plone/diazo.git

Then, run your buildout::

    $ bin/buildout -N
