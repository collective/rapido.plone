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
from plone.app.textfield import RichText, RichTextValue

from rapido.core.interfaces import IDatabasable, IForm
from .subscribers import update_html, update_field, update_assigned_rules
from rapido.plone import MessageFactory as _


class IDatabase(form.Schema, IImageScaleTraversable):
    """
    Rapido database
    """

class Database(Container):
    grok.implements(IDatabase, IDatabasable)

    meta_type = "Rapido database"

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
        return self.objectValues(spec='Rapido form')

    def current_user(self):
        """ Returns the current user id
        """
        return api.user.get_current().getUserName()

    def current_user_groups(self):
        """ Get the current user groups
        """
        member = api.user.get_current()
        return member.getGroups()

    def create_form(self, settings, code, html):
        """ Create a form 
        (used by the importation mechanism)
        Note: it first deletes the form if it was existing
        """
        form_id = settings['id']
        # if the form exists, we remove it first
        if form_id in self.objectIds():
            self.manage_delObjects([form_id])
        self.invokeFactory('rapido.plone.form', form_id,
            title=settings['title'])
        form_obj = self[form_id]
        form = IForm(form_obj)
        form_obj.assigned_rules = settings['assigned_rules']
        update_assigned_rules(form_obj)
        form_obj.code = code
        form.set_code(code)
        form_obj.html = RichTextValue(html)
        update_html(form_obj)
        for (field_id, field_settings) in settings['fields'].items():
            form_obj.invokeFactory('rapido.plone.field', field_id)
            field = form_obj[field_id]
            field.type = field_settings['type']
            field.index_type = field_settings.get('index_type', None)
            update_field(field)
