Import/export and source management
===================================

Rapido applications are implemented in the `/rapido` folder of a Diazo theme.
So all the known development procedures for theming apply to Rapido
development.

ZIP import/export
-----------------

The Plone theming editor allows to export a Diazo theme as a ZIP file, or to
import a new theme from a ZIP file.

That is the way we will import/export our Rapido applications between our sites.

Direct source editing
---------------------

We might also store our Diazo themes on our server in the Plone installation
folder::

    $INSTALL_FOLDER/resources/theme/my-theme

That way, we can develop our Rapido applications using our usual development
tools (text editor or IDE, Git, etc.).

Plone add-on
------------

We can also create our own Plone add-on (see `Plone documentation <http://docs.plone.org/develop/addons/index.html>`_,
and `Plone training <http://training.plone.org/5/theming/theme-package.html>`_)
and manage our Rapido applications in its theme folder.
