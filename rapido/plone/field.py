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
    SimpleTerm(value=u'DATETIME', title=_(u'Date/time')),
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


class Field(Container):
    grok.implements(IField)

    meta_type = "Rapido field"
