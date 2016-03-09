Associated Python functions
===========================

For a ``BASIC`` element, the associated Python function (having the same id)
will return the content of the element.

For field elements (``TEXT``, ``NUMBER``, ``DATETIME``), the associated Python
function will return its default value.

For an ``ACTION`` element, the associated Python function will be executed when
the action is triggered.

Special Python functions
------------------------

``on_save``
    Executed when a record is saved with the block.
    If it returns a value, it must be a string, and it will be used as a
    redirection URL for the current request.

``on_delete``
    Executed when a record is deleted.
    If it returns a value, it must be a string, and it will be used as a
    redirection URL for the current request.

``record_id``
    Executed at creation time to compute the record id.
