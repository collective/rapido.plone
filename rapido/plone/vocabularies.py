from five import grok
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from rapido.core import interfaces as core
from .database import IDatabase

class RulesVocabulary(grok.GlobalUtility):
    grok.name('rapido.plone.rules')
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        if IDatabase.providedBy(context.getParentNode()):
            db = core.IDatabase(context.getParentNode())
        elif IDatabase.providedBy(context):
            db = core.IDatabase(context)
        else:
            return SimpleVocabulary([])
        terms = [SimpleVocabulary.createTerm(
                     value,
                     value,
                     value)
                 for value in db.rules().keys()]
        return SimpleVocabulary(terms)


class FieldsVocabulary(grok.GlobalUtility):
    grok.name('rapido.plone.fields')
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        if IDatabase.providedBy(context.getParentNode()):
            db = core.IDatabase(context.getParentNode())
        elif IDatabase.providedBy(context):
            db = core.IDatabase(context)
        else:
            return SimpleVocabulary([])
        terms = []
        for form in db.forms:
            for id in form.fields.keys():
                terms.append(SimpleVocabulary.createTerm(id, id, id))
        return SimpleVocabulary(terms)