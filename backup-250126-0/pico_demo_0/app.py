from aiohttp import web
from gladius import Gladius

g = Gladius()

# server
app = web.Application()
routes = web.RouteTableDef()
routes.static('/js', 'examples/pico_demo_0/js')
routes.static('/css', 'examples/pico_demo_0/css')


@routes.get('/')
async def index(request):
    # home page
    with g.html(lang='en') as home_page:
        with g.head():
            g.meta(charset="utf-8")
            g.meta(name="viewport", content="width=device-width, initial-scale=1")
            g.meta(name="color-scheme", content="light dark")
            g.title("Pico CSS - Demo")
            g.meta(name="description", content="A pure HTML example, without dependencies.")
            g.link(rel='icon', href='/img/favicon.png', type='image/png')
            g.link(rel="stylesheet", href="css/pico.min.css")

        with g.body():
            with g.main(class_="container"):
                with g.section():
                    g.button(
                        'Populate table',
                        hx_post='/api/1.0/planet-table',
                        hx_trigger='click',
                        hx_target='section#planet-table',
                        hx_swap='innerHTML',
                    )

                with g.section(id="planet-table"):
                    with g.table():
                        pass

            g.script(src="js/htmx.min.js")

    text = home_page.render()
    headers = {'content-type': 'text/html'}
    return web.Response(status=200, text=text, headers=headers)


@routes.post('/api/1.0/planet-table')
async def api_1_0_planet_table(request):
    with g.table() as table:
        with g.thead():
            with g.tr():
                g.th('Planet', scope="col")
                g.th('Diameter (km)', scope="col")
                g.th('Distance to Sun (AU)', scope="col")
                g.th('Orbit (days)', scope="col")

        with g.tbody():
            with g.tr():
                g.th('Mercury', scope="row")
                g.td('4,880')
                g.td('0.39')
                g.td('88')

            with g.tr():
                g.th('Venus', scope="row")
                g.td('12,104')
                g.td('0.72')
                g.td('225')

            with g.tr():
                g.th('Earth', scope="row")
                g.td('12,742')
                g.td('1.00')
                g.td('365')

            with g.tr():
                g.th('Mars', scope="row")
                g.td('6,779')
                g.td('1.52')
                g.td('687')

        with g.tfoot():
            with g.tr():
                g.th('Average', scope="row")
                g.td('9,126')
                g.td('0.91')
                g.td('341')

    text = table.render()
    headers = {'content-type': 'text/html'}
    return web.Response(status=200, text=text, headers=headers)


app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=5000)
