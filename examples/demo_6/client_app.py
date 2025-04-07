# to learn more about Alpine visit https://alpinejs.dev/
from gladius import window, document, JSObject, export # type: ignore

NProgress = window.nprogress.default
Alpine = window.alpinejs.Alpine
PineconeRouter = window.pinecone_router.default
Handlebars = window.handlebars.default

window.Alpine = Alpine


def alpine_init(event):
    print('alpine:init', event)

    #
    # messages
    #
    def notify_messages(message):
        items: JSObject = Alpine.store('messages').items
        items.push(message)

    Alpine.store('messages', {
      'items': [],
      'notify': notify_messages,
    })

    #
    # handlebars
    #
    for el in document.querySelectorAll('script[type="handlebars"]'):
        Handlebars.registerPartial(el.getAttribute('name'), el.innerHTML)

    template: JSObject = Handlebars.compile('{{> Main }}')
    document.body.innerHTML = template()


# creates `window.send = send`, so it can be used in JavaScript
@export
def send(event):
    if not (event.type == 'click' or (event.type == 'keydown' and event.key == 'Enter')):
        return

    if event and event.preventDefault:
        event.preventDefault()

    notify: JSObject = Alpine.store('messages').notify
    message_input = document.querySelector('input#message')
    notify(message_input.value)
    message_input.value = ''
    message_input.focus()


document.addEventListener('alpine:init', alpine_init)
Alpine.plugin(PineconeRouter)
Alpine.start()
