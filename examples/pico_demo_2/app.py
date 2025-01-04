import os
import asyncio
from random import randint

from gladius import Gladius
from aiohttp import web, WSMsgType
from aiohttp.web import middleware


g = Gladius()


# server
@middleware
async def html_middleware(request, handler):
    resp = await handler(request)

    if isinstance(resp, str):
        headers = {'content-type': 'text/html'}
        resp = web.Response(status=200, text=resp, headers=headers)

    return resp


@middleware
async def json_middleware(request, handler):
    resp = await handler(request)

    if isinstance(resp, (list, dict)):
        resp = web.json_response(resp)

    return resp


app = web.Application(middlewares=[html_middleware, json_middleware])
routes = web.RouteTableDef()

# static
root_dir: str = os.path.split(__file__)[0]
routes.static('/js', os.path.join(root_dir, 'js'))
routes.static('/css', os.path.join(root_dir, 'css'))
routes.static('/img', os.path.join(root_dir, 'img'))


def home_page(parent):
    return g.div('Home')


def users_page(parent):
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


def books_page(parent):
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


def rentals_page(parent):
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


def live_data_page(parent):
    with g.table(id='live-data') as el:
        with g.thead():
            with g.tr():
                g.th('Planet', scope='col')
                g.th('Diameter (km)', scope='col')
                g.th('Distance to Sun (AU)', scope='col')
                g.th('Orbit (days)', scope='col')

        with g.tbody():
            pass

    return el


def app_page(parent=None):
    # home page
    with g.html(lang='en') as el:
        with g.head():
            g.meta(charset='utf-8')
            g.meta(name='viewport', content='width=device-width, initial-scale=1')
            g.meta(name='color-scheme', content='light dark')
            g.title('Pico CSS - Demo')
            g.meta(name='description', content='A pure HTML example, without dependencies.')
            g.link(rel='icon', href='/img/favicon.png', type='image/png')
            g.link(rel='stylesheet', href='/css/pico.min.css')
            g.link(rel='stylesheet', href='/css/nprogress.css')

            g.script(src='/js/router.min.js') # https://github.com/pinecone-router/router
            g.script(src='/js/alpine.min.js', defer=None)
            g.script(src='/js/nprogress.js')

        with g.body(x_data=None):
            with g.main(class_='container'):
                with g.section(id='nav'):
                    g.a('Home', href='/', role='button')
                    g.a('Users', href='/users', role='button')
                    g.a('Books', href='/books', role='button')
                    g.a('Rentals', href='/rentals', role='button')
                    g.a('Live Data', href='/live-data', role='button')

                with g.section(id='main'):
                    g.template(x_route='/', children=[home_page])
                    g.template(x_route='/users', children=[users_page])
                    g.template(x_route='/books', children=[books_page])
                    g.template(x_route='/rentals', children=[rentals_page])
                    g.template(x_route='/live-data', children=[live_data_page])

                    g.template(x_route='notfound', children=[
                        lambda parent: g.h1('Not found')
                    ])

    return el


@routes.get('/{tail:.*}')
async def index(request):
    el = app_page()
    return el.render()


async def send_live_data(ws):
    for i in range(10):
        if ws.closed:
            break

        data = [
            randint(0, 100),
            randint(0, 100),
            randint(0, 100),
            randint(0, 100),
        ]

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
