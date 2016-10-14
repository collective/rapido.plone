Access control
==============

Access control list
-------------------

The ACL defined in the app applies to records, not to blocks.
Blocks are always accessible, if we do not want a block to render some
information, we have to implement this in its Python file or use the
``view_permission`` setting.

Moreover, access control only impacts direct HTTP access to records (like opening
a record URL, deleting a record via the JSON API, etc.), and it does **not**
impact what happens in block Python files.

For instance in the :doc:`../tutorial`, if an anonymous visitor clicks on the
*"Like"* button on a page nobody had voted for yet, the ``like`` function
will create a record.

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

Roles do not grant any specific rights on records, they can be defined freely.
They are used in our Python functions to change the app behavior depending on
the user.

For instance, we might have a role named 'PurchaseManager', and in our block we
would display a "Validate purchase" button if the current user has the
'PurchaseManager' role.

Permissions on blocks
---------------------

By default, blocks are accessible by anyone (including anonymous visitors).

By setting the ``view_permission`` attribute in a block's YAML file, we can control access to this block.

Its value is a list of users or groups.

Example:

.. code-block:: yaml

    elements:
      whatever: BASIC
    view_permission:
      PurchaseDepartment
      eric

This block will be accessible only by the 'PurchaseDepartment' group members and Eric.

This restriction applies to direct block rendering and element calls, including REST calls.
