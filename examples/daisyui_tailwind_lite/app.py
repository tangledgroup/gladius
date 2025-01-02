from aiohttp import web
from gladius import Gladius

g = Gladius()

# home page
with g.html() as home_page:
    with g.head():
        g.meta(charset="UTF-8")
        g.title('daisyUI and Tailwind Lite')
        g.meta(name="viewport", content="width=device-width, initial-scale=1.0")
        g.link(rel='icon', href='/img/favicon.png', type='image/png')
        g.link(href="css/tailwind.css", rel="stylesheet", type="text/css")
        g.link(href="css/daisyui.full.css", rel="stylesheet", type="text/css")

    with g.body():
        with g.div(class_="navbar bg-base-100"):
            with g.div(class_="flex-none"):
                with g.button(class_="btn btn-square btn-ghost drawer-toggle drawer-button", for_="my-drawer-2"):
                    with g.svg(
                        xmlns="http://www.w3.org/2000/svg",
                        fill="none",
                        viewBox="0 0 24 24",
                        class_="inline-block h-5 w-5 stroke-current"
                    ):
                        g.path(
                            stroke_linecap="round",
                            stroke_linejoin="round",
                            stroke_width="2",
                            d="M4 6h16M4 12h16M4 18h16"
                        )

            with g.div(class_="flex-1"):
                g.a('daisyUI', class_="btn btn-ghost text-xl")

            with g.div(class_="flex-none"):
                with g.button(class_="btn btn-square btn-ghost"):
                    with g.svg(
                        xmlns="http://www.w3.org/2000/svg",
                        fill="none",
                        viewBox="0 0 24 24",
                        class_="inline-block h-5 w-5 stroke-current"
                    ):
                        g.path(
                            stroke_linecap="round",
                            stroke_linejoin="round",
                            stroke_width="2",
                            d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"
                        )

        # with g.div(class_="drawer lg:drawer-open"):
        with g.div(class_="drawer lg:drawer-open"):
            # g.input(id="my-drawer-2", type="checkbox", class_="drawer-toggle")

            # with g.div(class_="drawer-content flex flex-col items-center justify-center"):
            with g.div(class_="drawer-content flex flex-col items-center justify-center"):
                # Main content area
                # with g.div(class_="p-4 w-full lg:w-3/4"):
                with g.div(class_="p-4 w-full"):
                # with g.div(class_="p-4"):
                    g.h1('Main Content Area', class_="text-2xl font-bold mb-4")
                    g.p('Here is where your main logic and content would go. You can add forms, cards, or any interactive elements here.')
                    # Placeholder for main content
                    g.div('Your main content logic goes here', class_="bg-white shadow-lg rounded-lg p-6")

                # Button to open drawer on mobile view
                # g.label('Open drawer', for_="my-drawer-2", class_="btn btn-primary drawer-button lg:hidden")

            with g.div(class_="drawer-side"):
                g.label(for_="my-drawer-2", aria_label="close sidebar", class_="drawer-overlay")

                with g.ul(class_="menu bg-base-200 text-base-content min-h-full w-80 p-4"):
                    # Sidebar content here
                    with g.li():
                        g.a('Sidebar Item 1')

                    with g.li():
                        g.a('Sidebar Item 2')



# server
app = web.Application()
routes = web.RouteTableDef()
routes.static('/js', 'examples/daisyui_tailwind_lite/js')
routes.static('/css', 'examples/daisyui_tailwind_lite/css')


@routes.get('/')
async def variable_handler(request):
    text = home_page.render()
    headers = {'content-type': 'text/html'}
    return web.Response(status=200, text=text, headers=headers)


app.add_routes(routes)
web.run_app(app, host='0.0.0.0', port=5000)
