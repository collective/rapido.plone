from five import grok
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from rapido.core import interfaces as core
from .database import IDatabase

class RulesVocabulary(grok.GlobalUtility):
    grok.name('rapido.plone.rules')
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        if not IDatabase.providedBy(context.getParentNode()):
            return SimpleVocabulary([])
        db = core.IDatabase(context.getParentNode())
        terms = [SimpleVocabulary.createTerm(
                     value,
                     value,
                     value)
                 for value in db.rules().keys()]
        return SimpleVocabulary(terms)