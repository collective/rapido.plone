Specific Python functions
=========================

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
