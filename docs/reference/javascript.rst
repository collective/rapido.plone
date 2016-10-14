Javascript
==========

We can add Javascript files to our theme that will interact with our Rapido blocks.

There are no specific constraints on these scripts.
Nevertheless, it might be handy to use the Javascript dependencies already provided by Plone, such as ``jQuery`` and ``require``.

As Rapido allows to load block content dynamically (using the ``ajax`` mode), we might need to know when a Rapido block has been loaded dynamically.

To do that we can use the ``rapidoLoad`` event, which receives the block id as parameter. Example:

.. code-block:: javascript

    require(['jquery'], function($) {
        $(document).on('rapidoLoad', function(event, block_id) {
            console.log(block_id + ' has been loaded!');
        });
    });
