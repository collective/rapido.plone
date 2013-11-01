from five import grok
from zope.lifecycleevent.interfaces import IObjectAddedEvent,\
    IObjectModifiedEvent
from plone import api

from rapido.core.interfaces import IFormable, IForm, IDatabasable, IStorage
from rapido.plone.field import IField

@grok.subscribe(IFormable, IObjectAddedEvent)
@grok.subscribe(IFormable, IObjectModifiedEvent)
def update_html(obj, event=None):
    form = IForm(obj)
    form.set_layout(obj.html)

@grok.subscribe(IField, IObjectAddedEvent)
@grok.subscribe(IField, IObjectModifiedEvent)
def update_field(obj, event=None):
    form = IForm(obj.getParentNode())
    form.set_field(obj.id, {
        'type': obj.type
    })

@grok.subscribe(IDatabasable, IObjectAddedEvent)
def initialize_storage(obj, event=None):
    storage = IStorage(obj)
    storage.initialize(api.portal.get())