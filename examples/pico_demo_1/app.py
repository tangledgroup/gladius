import os
import asyncio
from random import randint

from gladius import Gladius
from aiohttp import web, WSMsgType

g = Gladius()

# server
app = web.Application()
routes = web.RouteTableDef()

# static
root_dir: str = os.path.split(__file__)[0]
routes.static('/js', os.path.join(root_dir, 'js'))
routes.static('/css', os.path.join(root_dir, 'css'))
routes.static('/img', os.path.join(root_dir, 'img'))


def get_home_page(content=None):
    # home page
    with g.html(lang='en') as home_page:
        with g.head():
            g.meta(charset='utf-8')
            g.meta(name='viewport', content='width=device-width, initial-scale=1')
            g.meta(name='color-scheme', content='light dark')
            g.title('Pico CSS - Demo')
            g.meta(name='description', content='A pure HTML example, without dependencies.')
            g.link(rel='icon', href='/img/favicon.png', type='image/png')
            g.link(rel='stylesheet', href='css/pico.min.css')

        with g.body(hx_boost='true'):
            with g.main(class_='container'):
                with g.section(id='nav'):
                    g.a('Users', href='/users', role='button')
                    g.a('Books', href='/books', role='button')
                    g.a('Rentals', href='/rentals', role='button')
                    g.a('Live Data', href='/live-data', role='button')

                with g.section(id='content') as el:
                    if content is not None:
                        el.add(content)

            g.script(src='js/htmx.min.js')
            g.script(src='js/ws.js')

            g.script('''
                document.addEventListener('DOMContentLoaded', function() {
                    document.body.addEventListener('htmx:wsOpen', function(event) {
                        console.log(event);
                        var data = {"content": "demo"};
                        event.detail.socketWrapper.send(JSON.stringify(data));
                    });
                });
            ''')

    return home_page


@routes.get('/')
async def index(request):
    home_page = get_home_page()
    text = home_page.render()
    headers = {'content-type': 'text/html'}
    return web.Response(status=200, text=text, headers=headers)


@routes.get('/users')
async def users_page(request):
    with g.table() as table:
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


    home_page = get_home_page(table)
    text = home_page.render()
    headers = {'content-type': 'text/html'}
    return web.Response(status=200, text=text, headers=headers)


@routes.get('/books')
async def books_page(request):
    with g.table() as table:
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

    home_page = get_home_page(table)
    text = home_page.render()
    headers = {'content-type': 'text/html'}
    return web.Response(status=200, text=text, headers=headers)


@routes.get('/rentals')
async def rentals_page(request):
    with g.table() as table:
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

    home_page = get_home_page(table)
    text = home_page.render()
    headers = {'content-type': 'text/html'}
    return web.Response(status=200, text=text, headers=headers)


@routes.get('/live-data')
async def live_data_page(request):
    with g.table(hx_ext='ws', ws_connect='/api/live-data-stream') as table:
        with g.thead():
            with g.tr():
                g.th('Planet', scope='col')
                g.th('Diameter (km)', scope='col')
                g.th('Distance to Sun (AU)', scope='col')
                g.th('Orbit (days)', scope='col')

        with g.tbody(id='live-data'):
            pass

    home_page = get_home_page(table)
    text = home_page.render()
    headers = {'content-type': 'text/html'}
    return web.Response(status=200, text=text, headers=headers)


async def send_live_data(ws):
    for i in range(10):
        if ws.closed:
            break

        with g.tbody(id='live-data', hx_swap_oob='beforeend') as tbody:
            with g.tr():
                g.th(f'{randint(0, 100)}', scope='row')
                g.td(f'{randint(0, 100)}')
                g.td(f'{randint(0, 100)}')
                g.td(f'{randint(0, 100)}')

        text = tbody.render()

        try:
            await ws.send_str(text)
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
