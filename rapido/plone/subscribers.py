from five import grok
from zope.lifecycleevent.interfaces import IObjectAddedEvent,\
    IObjectModifiedEvent, IObjectRemovedEvent
from Products.statusmessages.interfaces import IStatusMessage

from rapido.core.interfaces import (
    IFormable,
    IForm,
    IDatabasable,
    IStorage,
    IDatabase
)
from rapido.plone.field import IField
from rapido.plone.rule import IRule
from rapido.core.events import ICompilationErrorEvent, IExecutionErrorEvent

@grok.subscribe(IFormable, IObjectAddedEvent)
@grok.subscribe(IFormable, IObjectModifiedEvent)
def update_html(obj, event=None):
    form = IForm(obj)
    if obj.html:
        html = obj.html.output
    else:
        html = ''
    form.set_layout(html)

@grok.subscribe(IFormable, IObjectAddedEvent)
@grok.subscribe(IFormable, IObjectModifiedEvent)
def update_assigned_rules(obj, event=None):
    form = IForm(obj)
    form.assign_rules(obj.assigned_rules)

@grok.subscribe(IField, IObjectAddedEvent)
@grok.subscribe(IField, IObjectModifiedEvent)
def update_field(obj, event=None):
    # TODO: this is called twice, we need to test if already executed
    form = IForm(obj.getParentNode())
    form.set_field(obj.id, {
        'type': obj.type,
        'index_type': obj.index_type,
    })

@grok.subscribe(IField, IObjectRemovedEvent)
def remove_field(obj, event=None):
    # TODO: this is called twice, we need to test if already executed
    form = IForm(obj.getParentNode())
    form.remove_field(obj.id)

@grok.subscribe(IRule, IObjectAddedEvent)
@grok.subscribe(IRule, IObjectModifiedEvent)
def update_rule(obj, event=None):
    db = IDatabase(obj.getParentNode())
    db.set_rule(obj.id, {
        'code': obj.code,
    })

@grok.subscribe(IRule, IObjectRemovedEvent)
def remove_rule(obj, event=None):
    db = IDatabase(obj.getParentNode())
    db.remove_rule(obj.id)

@grok.subscribe(IDatabasable, IObjectAddedEvent)
def initialize_storage(obj, event=None):
    storage = IStorage(obj)
    storage.initialize()

@grok.subscribe(ICompilationErrorEvent)
def on_compilation_error(event):
    request = getattr(event.container.context, 'REQUEST', None)
    if request:
        IStatusMessage(request).addStatusMessage(event.message, type="error")

@grok.subscribe(IExecutionErrorEvent)
def on_execution_error(event):
    request = getattr(event.container.context, 'REQUEST', None)
    if request:
        IStatusMessage(request).addStatusMessage(event.message, type="error")