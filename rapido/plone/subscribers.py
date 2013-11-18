from five import grok
from zope.lifecycleevent.interfaces import IObjectAddedEvent,\
    IObjectModifiedEvent, IObjectRemovedEvent
from Products.statusmessages.interfaces import IStatusMessage

from rapido.core.interfaces import IFormable, IForm, IDatabasable, IStorage
from rapido.plone.field import IField
from rapido.core.events import ICompilationErrorEvent, IExecutionErrorEvent

@grok.subscribe(IFormable, IObjectAddedEvent)
@grok.subscribe(IFormable, IObjectModifiedEvent)
def update_html(obj, event=None):
    form = IForm(obj)
    form.set_layout(obj.html.output)

@grok.subscribe(IField, IObjectAddedEvent)
@grok.subscribe(IField, IObjectModifiedEvent)
def update_field(obj, event=None):
    form = IForm(obj.getParentNode())
    form.set_field(obj.id, {
        'type': obj.type,
        'index_type': obj.index_type,
    })

@grok.subscribe(IField, IObjectRemovedEvent)
def remove_field(obj, event=None):
    form = IForm(obj.getParentNode())
    form.remove_field(obj.id)

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