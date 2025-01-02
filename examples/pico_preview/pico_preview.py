from aiohttp import web
from gladius import Gladius, Element

g = Gladius()

# home page
with g.html(lang='en') as home_page:
    with g.head():
        g.meta(charset="utf-8")
        g.meta(name="viewport", content="width=device-width, initial-scale=1")
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
                                with g.li():
                                    g.a('Light', href="#", data_theme_switcher="light")
                                with g.li():
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
                            g.a('Privacy Policy', href="#", onclick="event.preventDefault()")

            with g.section(id="typography"):
                g.h2('Typography')
                g.p('''Aliquam lobortis vitae nibh nec rhoncus. Morbi mattis neque eget efficitur feugiat.
                          Vivamus porta nunc a erat mattis, mattis feugiat turpis pretium. Quisque sed tristique
                          felis.''')

                with g.blockquote():
                    g.text('''Maecenas vehicula metus tellus, vitae congue turpis hendrerit non. Nam at dui sit amet
                          ipsum cursus ornare.''')
                    with g.footer():
                        g.cite('- Phasellus eget lacinia')

                g.h3('Lists')
                with g.ul():
                    g.li('Aliquam lobortis lacus eu libero ornare facilisis.')
                    g.li('Nam et magna at libero scelerisque egestas.')
                    g.li('Suspendisse id nisl ut leo finibus vehicula quis eu ex.')
                    g.li('Proin ultricies turpis et volutpat vehicula.')

                g.h3('Inline text elements')
                with g.div(class_="grid"):
                    with g.p():
                        g.a('Primary link', href="#", onclick="event.preventDefault()")

                    with g.p():
                        g.a('Secondary link', href="#", class_="secondary", onclick="event.preventDefault()")

                    with g.p():
                        g.a('Contrast link', href="#", class_="contrast", onclick="event.preventDefault()")

                with g.div(class_="grid"):
                    with g.p():
                        g.strong('Bold')

                    with g.p():
                        g.em('Italic')

                    with g.p():
                        g.u('Underline')

                with g.div(class_="grid"):
                    with g.p():
                        g.del_('Deleted')

                    with g.p():
                        g.ins('Inserted')

                    with g.p():
                        g.s('Strikethrough')

                with g.div(class_="grid"):
                    with g.p():
                        g.small('Small')

                    with g.p('Text'):
                        g.sub('Sub')

                    with g.p('Text'):
                        g.sup('Sup')

                with g.div(class_="grid"):
                    with g.p():
                        g.abbr('Abbr.', title="Abbreviation", data_tooltip="Abbreviation")

                    with g.p():
                        g.kbd('Kbd')

                    with g.p():
                        g.mark('Highlighted')

                g.h3('Heading 3')
                g.p('''Integer bibendum malesuada libero vel eleifend. Fusce iaculis turpis ipsum, at efficitur
                          sem scelerisque vel. Aliquam auctor diam ut purus cursus fringilla. Class aptent taciti
                          sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.''')
                g.h4('Heading 4')
                g.p('''Cras fermentum velit vitae auctor aliquet. Nunc non congue urna, at blandit nibh. Donec ac
                          fermentum felis. Vivamus tincidunt arcu ut lacus hendrerit, eget mattis dui finibus.''')
                g.h5('Heading 5')
                g.p('''Donec nec egestas nulla. Sed varius placerat felis eu suscipit. Mauris maximus ante in
                          consequat luctus. Morbi euismod sagittis efficitur. Aenean non eros orci. Vivamus ut diam
                          sem.''')
                g.h6('Heading 6')
                g.p('''Ut sed quam non mauris placerat consequat vitae id risus. Vestibulum tincidunt nulla ut
                          tortor posuere, vitae malesuada tortor molestie. Sed nec interdum dolor. Vestibulum id
                          auctor nisi, a efficitur sem. Aliquam sollicitudin efficitur turpis, sollicitudin
                          hendrerit ligula semper id. Nunc risus felis, egestas eu tristique eget, convallis in
                          velit.''')

                with g.figure():
                    g.img(src="img/aleksandar-jason-a562ZEFKW8I-unsplash-2000x1000.jpg", alt="Minimal landscape")

                    with g.figcaption():
                        g.text('Image from')
                        g.a('unsplash.com', href="https://unsplash.com/photos/a562ZEFKW8I", target="_blank")

            with g.section(id="buttons"):
                g.h2('Buttons')

                with g.p(class_="grid"):
                    g.button('Primary')
                    g.button('Secondary', class_="secondary")
                    g.button('Contrast', class_="contrast")

                with g.p(class_="grid"):
                    g.button('Primary outline', class_="outline")
                    g.button('Secondary outline', class_="outline secondary")
                    g.button('Contrast outline', class_="outline contrast")

            with g.section(id="form"):
                with g.form():
                    g.h2('Form elements')

                    g.label('Search', for_="search")
                    g.input(type="search", id="search", name="search", placeholder="Search")

                    g.label('Text', for_="text")
                    g.input(type="text", id="text", name="text", placeholder="Text")
                    g.small('Curabitur consequat lacus at lacus porta finibus.')

                    g.label('Select', for_="select")

                    with g.select(id="select", name="select", required="required"):
                        g.option('Select…', value="", selected="selected")
                        g.option('…')

                    with g.label('File browser', for_="file"):
                        g.input(type="file", id="file", name="file")

                    with g.label('Range slider', for_="range"):
                        g.input(type="range", min="0", max="100", value="50", id="range", name="range")

                    with g.div(class_="grid"):
                        with g.label('Valid', for_="valid"):
                            g.input(type="text", id="valid", name="valid", placeholder="Valid", aria_invalid="false")

                        with g.label('Invalid', for_="invalid"):
                            g.input(type="text", id="invalid", name="invalid", placeholder="Invalid", aria_invalid="true")

                        with g.label('Disabled', for_="disabled"):
                            g.input(type="text", id="disabled", name="disabled", placeholder="Disabled", disabled="disabled")

                    with g.div(class_="grid"):
                        with g.label('Date', for_="date"):
                            g.input(type="date", id="date", name="date")

                        with g.label('Time', for_="time"):
                            g.input(type="time", id="time", name="time")

                        with g.label('Color', for_="color"):
                            g.input(type="color", id="color", name="color", value="#0eaaaa")

                    with g.div(class_="grid"):
                        with g.fieldset():
                            with g.legend():
                                g.strong('Checkboxes')

                            with g.label(for_="checkbox-1"):
                                g.input(type="checkbox", id="checkbox-1", name="checkbox-1", checked="checked")
                                g.text('Checkbox')

                            with g.label(for_="checkbox-2"):
                                g.input(type="checkbox", id="checkbox-2", name="checkbox-2")
                                g.text('Checkbox')

                        with g.fieldset():
                            with g.legend():
                                g.strong('Radio buttons')

                            with g.label(for_="radio-1"):
                                g.input(type="radio", id="radio-1", name="radio", value="radio-1", checked="checked")
                                g.text('Radio button')

                            with g.label(for_="radio-2"):
                                g.input(type="radio", id="radio-2", name="radio", value="radio-2")
                                g.text('Radio button')

                        with g.fieldset():
                            with g.legend():
                                g.strong('Switches')

                            with g.label(for_="switch-1"):
                                g.input(type="checkbox", id="switch-1", name="switch-1", role="switch", checked="checked")
                                g.text('Switch')

                            with g.label(for_="switch-2"):
                                g.input(type="checkbox", id="switch-2", name="switch-2", role="switch")
                                g.text('Switch')

                    g.input(type="reset", value="Reset", onclick="event.preventDefault()")
                    g.input(type="submit", value="Submit", onclick="event.preventDefault()")

            with g.section(id="tables"):
                g.h2('Tables')

                with g.div(class_="overflow-auto"):
                    with g.table(class_="striped"):
                        with g.thead():
                            with g.tr():
                                g.th('#', scope="col")
                                g.th('Heading', scope="col")
                                g.th('Heading', scope="col")
                                g.th('Heading', scope="col")
                                g.th('Heading', scope="col")
                                g.th('Heading', scope="col")
                                g.th('Heading', scope="col")
                                g.th('Heading', scope="col")

                        with g.tbody():
                            with g.tr():
                                g.th('1', scope="row")
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')

                            with g.tr():
                                g.th('2', scope="row")
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')

                            with g.tr():
                                g.th('3', scope="row")
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')
                                g.td('Cell')

            with g.section(id="modal"):
                g.h2('Modal')
                g.button('Launch demo modal', class_="contrast", data_target="modal-example", onclick="toggleModal(event)")

            with g.section(id="accordions"):
                g.h2('Accordions')

                with g.details():
                    g.summary('Accordion 1')
                    g.p('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque urna diam,
                          tincidunt nec porta sed, auctor id velit. Etiam venenatis nisl ut orci consequat, vitae
                          tempus quam commodo. Nulla non mauris ipsum. Aliquam eu posuere orci. Nulla convallis
                          lectus rutrum quam hendrerit, in facilisis elit sollicitudin. Mauris pulvinar pulvinar
                          mi, dictum tristique elit auctor quis. Maecenas ac ipsum ultrices, porta turpis sit
                          amet, congue turpis.''')

                with g.details(open="open"):
                    g.summary('Accordion 2')

                    with g.ul():
                        g.li('Vestibulum id elit quis massa interdum sodales.')
                        g.li('Nunc quis eros vel odio pretium tincidunt nec quis neque.')
                        g.li('Quisque sed eros non eros ornare elementum.')
                        g.li('Cras sed libero aliquet, porta dolor quis, dapibus ipsum.')

            with g.article(id="article"):
                g.h2('Article')
                g.p('''Nullam dui arcu, malesuada et sodales eu, efficitur vitae dolor. Sed ultricies dolor non
                          ante vulputate hendrerit. Vivamus sit amet suscipit sapien. Nulla iaculis eros a elit
                          pharetra egestas. Nunc placerat facilisis cursus. Sed vestibulum metus eget dolor pharetra
                          rutrum.''')

                with g.footer():
                    g.small('Duis nec elit placerat, suscipit nibh quis, finibus neque.')

            with g.section(id="group"):
                g.h2('Group')

                with g.form():
                    with g.fieldset(role="group"):
                        g.input(name="email", type="email", placeholder="Enter your email", autocomplete="email")
                        g.input(type="submit", value="Subscribe")

            with g.section(id="progress"):
                g.h2('Progress bar')
                g.progress(id="progress-1", value="25", max="100")
                g.progress(id="progress-2")

            with g.section(id="loading"):
                g.h2('Loading')

                with g.article(aria_busy="true"):
                    pass

                g.button('Please wait…', aria_busy="true")

        with g.footer(class_="container"):
            with g.small():
                g.text('Built with')
                g.a('Pico', href="https://picocss.com")
                g.text('•')
                g.a('Source code', href="https://github.com/picocss/examples/blob/master/v2-html/index.html")

        with g.dialog(id="modal-example"):
            with g.article():
                with g.header():
                    g.button(rel="prev", aria_label="Close", data_target="modal-example", onclick="toggleModal(event)")
                    g.h3('Confirm your action!')

                g.p('''Cras sit amet maximus risus. Pellentesque sodales odio sit amet augue finibus
                          pellentesque. Nullam finibus risus non semper euismod.''')

                with g.footer():
                    g.button('Cancel', role="button", class_="secondary", data_target="modal-example", onclick="toggleModal(event)")
                    g.button('Confirm', autofocus="autofocus", data_target="modal-example", onclick="toggleModal(event)")

        # g.script(src="js/minimal-theme-switcher.js")
        with g.script():
            with open('examples/pico_preview/js/minimal-theme-switcher.js') as f:
                g.text(f.read())

        # g.script(src="js/modal.js")
        with g.script():
            with open('examples/pico_preview/js/modal.js') as f:
                g.text(f.read())


# print(home_page)
print(home_page.render())

# # server
# app = web.Application()
# routes = web.RouteTableDef()

# # async def

# app.add_routes(routes)
# web.run_app(app, host='0.0.0.0', port=5000)
