Changelog
=========


1.1.1 (2017-04-22)
------------------

New features:

- Added Spanish translation for the rapido.plone documentation.
  [macagua]

- Added i18n support for the rapido.plone documentation.
  [macagua]

Bug fixes:

- Updated the source code from the rapido.plone tutorial about the rating app.
  [macagua]

- Updated the rapido.plone tutorial documentation about the rating app.
  [macagua]

- Make it work in an Archetypes free environment:
  Bind event handlers directly on the OFS.Image.File class,
  because there is no specific interface in OFS.
  The additional set interface from plone.app.blob was Archetypes only.
  It is no longer availabe if Archetypes and its dependencies is not available.
  [jensens]

- Fix content rules Rapido app call
  [ebrehault]


1.1 (2016-12-18)
----------------

Breaking changes:

- rapido.plone requires plone.resource 1.2

New features:

- Allow to locate a Rapido app outside the current theme
  [ebrehault]

- Expose Rapido blocks as first-class Plone views
  [jpgimenez, ebrehault]


1.0.3 (2016-09-19)
------------------

- Add book use case
  [sverbois]

- Return unicode when loading templates
  [ebrehault]


1.0.2 (2016-04-09)
------------------

- Add rapidoLoad Javascript event
  [ebrehault]

- Allow to inject parent request path in Rapido path
  [ebrehault]

- Support TAL templates
  [ebrehault]

- Set content properly when calling block from content rule
  [ebrehault]

- External call to Rapido elements using @@rapido-call
  [ebrehault]

- API to access an external Rapido app
  [ebrehault]


1.0.1 (2016-01-06)
------------------

- Ajax links
  [ebrehault]

- Better context.content computing and reinjection
  [ebrehault]


1.0 (2015-11-17)
----------------

- Initial release.
  [ebrehault]

