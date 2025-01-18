import os
import asyncio
from random import randint

from aiohttp import web, WSMsgType
from gladius.util import make_page
from gladius.aiohttp import make_app


# server
root_dir = os.path.split(__file__)[0]
g, app, routes = make_app(root_dir)


def home_page():
    return g.div('Home')


def users_page():
    with g.div() as el:
        g.a('Home', href='/', role='button')

        with g.table():
            with g.thead():
                with g.tr():
                    g.th('Planet', scope='col')
                    g.th('Diameter (km)', scope='col')
                    g.th('Distance to Sun (AU)', scope='col')
                    g.th('Orbit (days)', scope='col')

            with g.tbody():
                with g.tr():
                    g.th('Mercury', scope='row')
                    g.td('4,880')
                    g.td('0.39')
                    g.td('88')

                with g.tr():
                    g.th('Venus', scope='row')
                    g.td('12,104')
                    g.td('0.72')
                    g.td('225')

                with g.tr():
                    g.th('Earth', scope='row')
                    g.td('12,742')
                    g.td('1.00')
                    g.td('365')

                with g.tr():
                    g.th('Mars', scope='row')
                    g.td('6,779')
                    g.td('1.52')
                    g.td('687')

            with g.tfoot():
                with g.tr():
                    g.th('Average', scope='row')
                    g.td('9,126')
                    g.td('0.91')
                    g.td('341')

    return el


def books_page():
    with g.table() as el:
        with g.thead():
            with g.tr():
                g.th('Planet', scope='col')
                g.th('Diameter (km)', scope='col')
                g.th('Distance to Sun (AU)', scope='col')
                g.th('Orbit (days)', scope='col')

        with g.tbody():
            with g.tr():
                g.th('Venus', scope='row')
                g.td('12,104')
                g.td('0.72')
                g.td('225')

            with g.tr():
                g.th('Earth', scope='row')
                g.td('12,742')
                g.td('1.00')
                g.td('365')

            with g.tr():
                g.th('Mars', scope='row')
                g.td('6,779')
                g.td('1.52')
                g.td('687')

        with g.tfoot():
            with g.tr():
                g.th('Average', scope='row')
                g.td('9,126')
                g.td('0.91')
                g.td('341')

    return el


def rentals_page():
    with g.table() as el:
        with g.thead():
            with g.tr():
                g.th('Planet', scope='col')
                g.th('Diameter (km)', scope='col')
                g.th('Distance to Sun (AU)', scope='col')
                g.th('Orbit (days)', scope='col')

        with g.tbody():
            with g.tr():
                g.th('Earth', scope='row')
                g.td('12,742')
                g.td('1.00')
                g.td('365')

            with g.tr():
                g.th('Mars', scope='row')
                g.td('6,779')
                g.td('1.52')
                g.td('687')

        with g.tfoot():
            with g.tr():
                g.th('Average', scope='row')
                g.td('9,126')
                g.td('0.91')
                g.td('341')

    return el


def live_data_page():
    with g.table(id='live-data') as el:
        with g.thead():
            with g.tr():
                g.th('Planet', scope='col')
                g.th('Diameter (km)', scope='col')
                g.th('Distance to Sun (AU)', scope='col')
                g.th('Orbit (days)', scope='col')

        with g.tbody():
            with g.template(x_for='message in $store.messages.messages', c_key='message.id'):
                # g.div(x_text='message')

                with g.tr():
                    g.th(x_text='message.row[0]')
                    g.th(x_text='message.row[1]')
                    g.th(x_text='message.row[2]')
                    g.th(x_text='message.row[3]')

    return el


app_page = make_page(
    g,
    title='Pico CSS - Demo',
    description='A pure HTML example, without dependencies.',
    favicon='/static/img/favicon.png',
    links=[
        '/static/css/pico.min.css',
        '/static/css/nprogress.css',
        '/static/pyscript/core.css',
    ],
    scripts=[
        dict(src='/static/js/nprogress.js', defer=None),
        dict(src='/static/pyscript/core.js', type='module', defer=None),
    ],
)

with app_page:
    with g.body(x_data=None):
        with g.main(class_='container'):
            with g.section(id='nav'):
                g.a('Home', href='/', role='button')
                g.a('Users', href='/users', role='button')
                g.a('Books', href='/books', role='button')
                g.a('Rentals', href='/rentals', role='button')
                g.a('Live Data', href='/live-data', role='button')

            with g.section(id='main'):
                with g.template(x_route='/'): home_page()
                with g.template(x_route='/users'): users_page()
                with g.template(x_route='/books'): books_page()
                with g.template(x_route='/rentals'): rentals_page()
                with g.template(x_route='/live-data'): live_data_page()
                with g.template(x_route='notfound'): g.h1('Not found')


        g.mpy_config('''
            interpreter = "/static/micropython/micropython.mjs"
            # experimental_create_proxy = "auto"

            [js_modules.main]
            "/static/pinecone-router/router.esm.js" = "pinecone_router"
            "/static/alpinejs/module.esm.js" = "alpinejs"
        ''')

        g.script('''
            import js
            import json
            from pyscript import window, document, WebSocket
            from pyscript.ffi import to_js, create_proxy
            from pyscript.js_modules.pinecone_router import default as PineconeRouter
            from pyscript.js_modules.alpinejs import Alpine


            def alpine_init(event):
                print('alpine:init', event)

                def init_messages():
                    def onopen(event):
                        window.console.log('onopen: WebSocket connection established.')
                        ws.send(json.dumps({}))

                    def onclose(event):
                        window.console.log('onclose: WebSocket connection closed.')

                    def onmessage(event):
                        window.console.log('onmessage:', event)
                        data = json.loads(event.data)
                        add_message(data)
                        # print(f'{messages=}', messages.length)

                    def onerror(error):
                        window.console.error('on_error: WebSocket error:', error)

                    ws = WebSocket(url=f'ws://{window.location.host}/api/live-data-stream')
                    ws.onopen = onopen
                    ws.onclose = onclose
                    ws.onmessage = onmessage
                    ws.onerror = onerror

                def add_message(message: dict):
                    Alpine.store('messages').messages.push(to_js(message))

                Alpine.store('messages', to_js({
                    'messages': js.Array.new(),
                    'init': init_messages,
                    'add': add_message,
                }))

            document.addEventListener('alpine:init', alpine_init)

            window.Alpine = Alpine
            Alpine.plugin(PineconeRouter)
            Alpine.start()
            print('start')
        ''', type='mpy', defer=None)


@routes.get('/{tail:.*}')
async def index(request):
    el = app_page
    return el.render()


async def send_live_data(ws):
    for i in range(10):
        if ws.closed:
            break

        data = {
            'id': str(randint(0, 100)),
            'row': [
                randint(0, 100),
                randint(0, 100),
                randint(0, 100),
                randint(0, 100),
            ]
        }

        try:
            await ws.send_json(data)
        except Exception:
            break

        await asyncio.sleep(1.0)


@routes.get('/api/live-data-stream')
async def api_live_data_stream(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            print(f'{msg.data=}')

            # send data in background
            coro = send_live_data(ws)
            asyncio.create_task(coro)
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())

    print('websocket connection closed')
    return ws


app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
