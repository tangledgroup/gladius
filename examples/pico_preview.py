from gladius import Gladius, Element

g = Gladius()

# home page
home_page: Element = g.html(lang='en').add(
    g.head().add(
        g.meta(charset="utf-8"),
        g.meta(name="viewport", content="width=device-width, initial_scale=1"),
        g.meta(name="color-scheme", content="light dark"),
        g.title().add("Preview • Pico CSS"),
        g.meta(name="description", content="A pure HTML example, without dependencies."),

        g.link(rel="stylesheet",
               href="https://cdn.jsdelivr.net/npm/@picocss/pico@2.0.6/css/pico.min.css"),
    ),
    g.body().add(
        g.header(class_="container").add(
            g.hgroup().add(
                g.h1().add('Pico'),
                g.p().add('A pure HTML example, without dependencies.'),
            )
        ),
        g.nav().add(
            g.ul().add(
                g.li().add(
                    g.details(class_="dropdown").add(
                        g.summary(role="button", class_="secondary").add('Theme'),
                        g.ul().add(
                            g.li().add(
                                a0 := g.a(href="#", data_theme_switcher="auto").add('Auto'),
                                a1 := g.a(href="#", data_theme_switcher="light").add('Light'),
                                a2 := g.a(href="#", data_theme_switcher="dark").add('Dark'),
                            )
                        )
                    )
                )
            )
        ),
    )
)

print(home_page)
print(a0)
print(a1)
print(a2)

with g.html(lang='en') as home_page:
    with g.head():
        g.meta(charset="utf-8")
        g.meta(name="viewport", content="width=device-width, initial_scale=1")
        g.meta(name="color-scheme", content="light dark")
        g.title().add("Preview • Pico CSS")
        g.meta(name="description", content="A pure HTML example, without dependencies.")

        g.link(rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/@picocss/pico@2.0.6/css/pico.min.css")

    with g.body():
        with g.header(class_="container"):
            with g.hgroup():
                g.h1().add('Pico')
                g.p().add('A pure HTML example, without dependencies.')

        with g.nav():
            with g.ul():
                with g.li():
                    with g.details(class_="dropdown"):
                        g.summary(role="button", class_="secondary").add('Theme')

                        with g.ul():
                            with g.li():
                                a0 = g.a(href="#", data_theme_switcher="auto").add('Auto')
                                a1 = g.a(href="#", data_theme_switcher="light").add('Light')
                                a2 = g.a(href="#", data_theme_switcher="dark").add('Dark')

    print(home_page)
    print(a0)
    print(a1)
    print(a2)

# # router
# g.route('/', home_page)
# app = g.get_app()
#
# if __name__ == '__main__':
#     g.run_app(host='0.0.0.0', port=5000)
