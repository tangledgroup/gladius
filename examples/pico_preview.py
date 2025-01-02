from aiohttp import web
from gladius import Gladius, Element

g = Gladius()

# home page
with g.html(lang='en') as home_page:
    with g.head():
        g.meta(charset="utf-8")
        g.meta(name="viewport", content="width=device-width, initial_scale=1")
        g.meta(name="color-scheme", content="light dark")
        g.title("Preview • Pico CSS")
        g.meta(name="description", content="A pure HTML example, without dependencies.")

        g.link(rel="stylesheet",
               href="https://cdn.jsdelivr.net/npm/@picocss/pico@2.0.6/css/pico.min.css")

    with g.body():
        with g.header(class_="container"):
            with g.hgroup():
                g.h1('Pico')
                g.p('A pure HTML example, without dependencies.')

            with g.nav():
                with g.ul():
                    with g.li():
                        with g.details(class_="dropdown"):
                            g.summary('Theme', role="button", class_="secondary")

                            with g.ul():
                                with g.li():
                                    g.a('Auto', href="#", data_theme_switcher="auto")
                                    g.a('Light', href="#", data_theme_switcher="light")
                                    g.a('Dark', href="#", data_theme_switcher="dark")

        with g.main(class_="container"):
            with g.section(id="preview"):
                g.h2('Preview')
                g.p('''Sed ultricies dolor non ante vulputate hendrerit. Vivamus sit amet suscipit sapien. Nulla
                          iaculis eros a elit pharetra egestas.''')

                with g.form():
                    with g.div(class_="grid"):
                        g.input(
                            type="text",
                            name="firstname",
                            placeholder="First name",
                            aria_label="First name",
                            required="required",
                        )

                        g.input(
                            type="email",
                            name="email",
                            placeholder="Email address",
                            aria_label="Email address",
                            autocomplete="email",
                            required="required",
                        )

                        g.button('Subscribe', type="submit")

                    with g.fieldset():
                        with g.label(for_="terms"):
                            g.input(type="checkbox", role="switch", id="terms", name="terms")
                            g.text('I agree to the')


# print(home_page)
print(home_page.render())

# # server
# app = web.Application()
# routes = web.RouteTableDef()

# # async def

# app.add_routes(routes)
# web.run_app(app, host='0.0.0.0', port=5000)
