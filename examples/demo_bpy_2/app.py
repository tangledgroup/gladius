# to learn more about Alpine visit https://alpinejs.dev/
from browser import window, document # type: ignore

NProgress = window.nprogress.default
Alpine = window.alpinejs.Alpine
PineconeRouter = window.pinecone_router.default


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

from aiohttp import web
from gladius.starter import create_aiohttp_app

# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'alpinejs': ['dist/module.esm.js'],
    'pinecone-router': ['dist/router.esm.js'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

# create simple aiohttp web server
g, page, app = create_aiohttp_app(
    npm_packages=npm_packages, # type: ignore
    use_brython=True,
    ready='client_app.py',
)

# server-side structure
with page:
    with g.body(x_data=None):
        with g.main(class_='container'):
            g.h1('Gladius Demo - Messages')

            with g.div(class_='form'):
                with g.fieldset(role='group'):
                    g.input(name='message', type='text', placeholder='Enter your message', autocomplete='off', id='message', x_on__c__keydown='send')
                    g.input(type='submit', value='Send', x_on__c__click='send')

            with g.template(x_for='m in $store.messages.items'):
                g.p(x_text='m')

# start application
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)

@export
def f1(x: int) -> int:
    return int(x ** 2)



document.addEventListener('alpine:init', alpine_init)
Alpine.plugin(PineconeRouter)
Alpine.start()
