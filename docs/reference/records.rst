Records
=======

Rapido records can be created by saving a block containing field elements.
The value of each submitted element will be stored in a corresponding item.

In that case, the record has an associated block (the block id is stored in an
item named ``block``). When the record is rendered for display (when we load its
URL in our browser), it uses the layout of the named block.

Records can also be created manually (without any associated block) using the
Python API or the REST API. Such records cannot be rendered automatically by
calling their URL, but their item values can be used in a block if we know how
to find the record (in the :doc:`../tutorial` for instance, our records are
created manually from the ``like`` function, they are not associated with the
``rate`` block, but we use the stored items to produce our element contents).
