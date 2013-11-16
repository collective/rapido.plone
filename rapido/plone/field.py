from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.textfield import RichText


from rapido.plone import MessageFactory as _

field_types = SimpleVocabulary([
    SimpleTerm(value=u'TEXT', title=_(u'Text')),
    SimpleTerm(value=u'NUMBER', title=_(u'Number')),
])

index_types = SimpleVocabulary([
    SimpleTerm(value=u'', title=_(u'Not indexed')),
    SimpleTerm(value=u'field', title=_(u'Field index')),
    SimpleTerm(value=u'keyword', title=_(u'Keyword index')),
    SimpleTerm(value=u'text', title=_(u'Full-text index')),
])

class IField(form.Schema, IImageScaleTraversable):
    """
    Field
    """

    id = schema.TextLine(
        title=_("Id"),
        required=True
        )

    type = schema.Choice(
            title=_(u"Type"),
            vocabulary=field_types,
            required=True,
        )

    index_type = schema.Choice(
            title=_(u"Index type"),
            vocabulary=index_types,
            required=True,
        )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Field(Container):
    grok.implements(IField)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# field_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IField)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
