Content rules
=============

Content rules allows to trigger specific actions (for instance, send an email)
when an given event (for instance, when a new content is created in such folder)
happens in our Plone site.

Rapido provides a content rule action, so we can execute a Rapido function when
an given event happens.

The action to take is defined in the Plone content rules editor (see the `Plone content rules documentation <http://docs.plone.org/working-with-content/managing-content/contentrules.html>`_), and requires the following parameter:

- the app id,
- the block id,
- the function name.

The ``context.content`` received by the function will be the content where the
event happened.