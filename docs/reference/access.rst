Access control
==============

Access control applies to records, not the blocks. Blocks are always accessible,
if we do not want a block to render an information, we have to implement it in
its Python file.

Moreover, access control only impacts direct HTTP access to records (like openning
a record URL, deleting a record from the JSON API, etc.), and it does **not**
impact what hapens in block Python files.

For instance in the :doc:`../tutorial`, if an anonymous visitor click on the Like
button on a page nobody had already vote for, the ``like`` function will create
a record.

But an anonymous visitor would not be able to modify this record or to delete it
using the JSON API.

The expected format is:

.. code-block:: yaml

    acl:
      rights:
        reader: [<list of users or groups>]
        author: [<list of users or groups>]
        editor: [<list of users or groups>]
      roles: {<role_id>: [<list of users or groups>]}

In the list of users or groups, ``'*'`` means everyone.

Access levels
-------------

The access levels are:

- ``reader``: can read all the records,
- ``author``: can read all the records, can create records, can modify/delete his
  own records,
- ``editor``: can read/modify/delete any record, can create records.

The access control settings are managed in the ``settings.yaml`` file in the app
root folder.

Roles
-----

Roles are not granting any specific rights on records, they can be defined freely,
they can be used in our Python functions to change the app behavior depending on
the user.

For instance, we might have a role named 'PurchaseManager', and if our block we
would display a "Validate purchase" button if the current user as the
'PurchaseManager' role.
