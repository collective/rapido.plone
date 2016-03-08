def display_quote(context):
    doc = context.app.get_record('doc1')
    if doc:
        return doc.get('quote', '')
    else:
        return "No quote"


def create(context):
    doc = context.app.create_record('doc1')
    doc['block'] = 'action'
    doc["quote"] = "Knowledge is power, France is bacon."
    doc.save()


def boom(context):
    context.wrong()


def log_me(context):
    context.app.log("Hello!")
    context.app.log([1, 2, {'a': 3}])
    context.app.log(context)


def create_content(context):
    context.api.content.create(
        container=context.api.portal.get(),
        type='Document',
        title='My Content',
    )
