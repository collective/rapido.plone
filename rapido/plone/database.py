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
from plone import api
from plone.app.textfield import RichText

from rapido.core.interfaces import IDatabasable
from rapido.plone import MessageFactory as _


class IDatabase(form.Schema, IImageScaleTraversable):
    """
    Rapido database
    """

class Database(Container):
    grok.implements(IDatabase, IDatabasable)

    @property
    def uid(self):
        return self.UID()

    @property
    def root(self):
        return api.portal.get()

    def url(self):
        return self.absolute_url()

    @property
    def forms(self):
        return self.objectValues(spec='Form')

    def current_user(self):
        """ Returns the current user id
        """
        return api.user.get_current().getUserName()

    def current_user_groups(self):
        """ Get the current user groups
        """
        member = api.user.get_current()
        return member.getGroups()