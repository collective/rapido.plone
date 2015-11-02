Records
=======

Rapido records can be created by saving a block containing field elements.
the value of each submitted elements will be stored in corresponding items.

In that case, the record has an associated block (the block id is stored in an
item named ``block``), when the record is rendered for display (when we load its
URL in our browser), it uses the block layout.

Records can also be created manually (without any associated block) using the
Python API or the REST API. Such records cannot be rendered automatically by
calling their URL, but their items values can be used in a block if we know how
to find the record (in the :doc:`../tutorial` for instance, our records are
created manually from the ``like`` function, they are not associated to the
``rate`` block, but we use the stored items to produce our elements content).
