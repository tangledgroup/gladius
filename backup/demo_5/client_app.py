# to learn more about Alpine visit https://alpinejs.dev/
from gladius import window, document, JSObject, export # type: ignore

NProgress = window.nprogress.default
Alpine = window.alpinejs.Alpine
PineconeRouter = window.pinecone_router.default

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


@export
def send(event):
    if not (event.type == 'click' or (event.type == 'keydown' and event.key == 'Enter')):
        return

    if event and event.preventDefault:
        event.preventDefault()

    notify = Alpine.store('messages').notify
    message_input = document.querySelector('input#message')
    notify(message_input.value)
    message_input.value = ''
    message_input.focus()


@export
def f1(x: int) -> int:
    return int(x ** 2)


document.addEventListener('alpine:init', alpine_init)
Alpine.plugin(PineconeRouter)
Alpine.start()
