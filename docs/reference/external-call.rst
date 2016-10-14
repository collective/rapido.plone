External call to Rapido
=======================

By traversing to ``@@rapido-call``, we can call a Rapido element as a Python function.

It might be very useful when we want to use Rapido from a PythonScript,
a Plone page template,
or any Plone mechanism offering to run a small script (Plone workflow, ``collective.easyform``, etc.).

``@@rapido-call`` accepts the following parameters:

- ``path`` (mandatory, string): Rapido path to the element to call (format: ``app/blocks/element``),
- ``content`` (optional, object): the content to provide to the Rapido context,
- any other named parameters: those named parameters will be available to the Python implementation of the element in the ``context.params`` dictionary.

Example:

PythonScript:

.. code-block:: python

    visitors = container.restrictedTraverse('@@rapido-call')(
        'myapp/stats/analyse',
        content=portal.news,
        min_duration=2,
        client='smartphone')

Rapido element in ``myapp/stats.py``:

.. code-block:: python

    def analyse(context):
        filtered = get_filtered_visitors(
            duration=context.params['min_duration'],
            type=context.params['client'])
        return len(filtered)
