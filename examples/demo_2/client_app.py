# to learn more about Alpine visit https://alpinejs.dev/
from pyscript import document, window # type: ignore
from pyscript.web import page # type: ignore
from pyscript.ffi import to_js # type: ignore
from pyscript.js_modules.alpinejs import Alpine # type: ignore
from pyscript.js_modules.pinecone_router import default as PineconeRouter # type: ignore

window.Alpine = Alpine


def export(func):
    setattr(window, func.__name__, func)

    def wraps(*args, **kwargs):
        return func(*args, **kwargs)

    return wraps


def alpine_init(event):
    print('alpine:init', event)

    #
    # messages
    #
    def notify_messages(message):
        items: 'Array' = Alpine.store('messages').items
        items.push(message)

    Alpine.store('messages', to_js({
      'items': to_js([]),
      'notify': notify_messages,
    }))


@export
def send(event):
    if not (event.type == 'click' or (event.type == 'keydown' and event.key == 'Enter')):
        return

    if event and event.preventDefault:
        event.preventDefault()

    notify = Alpine.store('messages').notify
    message_input = page['input#message'][0]
    notify(message_input.value)
    message_input.value = ''
    message_input.focus()


@export
def f1(x: int) -> int:
    return int(x ** 2)



document.addEventListener('alpine:init', alpine_init)
Alpine.plugin(PineconeRouter)
Alpine.start()
