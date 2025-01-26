import os
import asyncio
from random import randint

from aiohttp import web, WSMsgType
from gladius.starter import make_mpy_pico


#
# client elements / templates
#
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
            with g.template(x_init='$store.messages.load()', x_for='message in $store.messages.items', c_key='message.id'):
                with g.tr():
                    g.th(x_text='message.row[0]')
                    g.th(x_text='message.row[1]')
                    g.th(x_text='message.row[2]')
                    g.th(x_text='message.row[3]')

    return el


#
# server app
#
root_dir = os.path.split(__file__)[0]
g, app, routes, page = make_mpy_pico(root_dir)

with page:
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

    await ws.close()


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
