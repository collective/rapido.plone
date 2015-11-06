Application
===========

A Rapido application is defined by a folder in the ``rapido`` folder in the
current theme.

The application folder might contain a ``settings.yaml`` file in its root but
that is not mandatory. It allows to define the access control settings
(see :doc:`./access`), or to enable the ``debug`` mode.

It always contains a ``blocks`` folder containing its blocks (see :doc:`./blocks`).

It might also contain regular theme items (rules.xml, CSS, Javascript, etc.).
