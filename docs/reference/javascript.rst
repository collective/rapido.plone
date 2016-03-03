Javascript
==========

We can add Javascript files in our theme that will interact with our Rapido blocks.

There is no specific constraint about how those scripts. Nevertheless, it might be handy to use the Javascript dependencies already provided by Plone, like ``jQuery`` and ``require``.

As Rapido allows to load block content dynamically (using the ``ajax`` mode), we might need to know when a rapido block has been loaded dynamically.

To do that we can use the ``rapidoLoad`` event, which receive the block id as parameter. Example:

.. code-block:: javascript

    require(['jquery'], function($) {
        $(document).on('rapidoLoad', function(event, block_id) {
            console.log(block_id + ' has been loaded!');
        });
    });