# https://github.com/picocss/examples/blob/master/v2-html/index.html
from aiohttp import web
from gladius import h, define, render, run_app


with h.html({'lang': 'en'}) as html_root:
    with h.head():
        h.script({'type': 'text/javascript', 'src': 'https://codesandbox.io/public/sse-hooks/sse-hooks.e15ace8ccace5398a721ffec81f121de.js'})
        h.script({'type': 'text/javascript', 'src': 'https://codesandbox.io/static/js/banner.d9cb10a38.js'})
        h.meta({'charset': 'utf-8'})
        h.meta({'name': 'viewport', 'content': 'width=device-width, initial-scale=1'})
        h.meta({'name': 'color-scheme', 'content': 'light dark'})
        h.title({}, 'Preview • Pico CSS')
        h.meta({'name': 'description', 'content': 'A pure HTML example, without dependencies.'})
        h.link({'rel': 'stylesheet', 'href': 'https://cdn.jsdelivr.net/npm/@picocss/pico@2.1.1/css/pico.min.css'})

    with h.body():
        with h.header({'class': 'container'}):
            with h.hgroup():
                h.h1({}, 'Pico')
                h.p({}, 'A pure HTML example, without dependencies.')

            with h.nav():
                with h.ul():
                    with h.li():
                        with h.details({'class': 'dropdown'}):
                            h.summary({'role': 'button', 'class': 'secondary'}, 'Theme')

                            with h.ul():
                                h.li({}, h.a({'href': '#', 'data-theme-switcher': 'auto'}, 'Auto'))
                                h.li({}, h.a({'href': '#', 'data-theme-switcher': 'light'}, 'Light'))
                                h.li({}, h.a({'href': '#', 'data-theme-switcher': 'dark'}, 'Dark'))

        with h.main({'class': 'container'}):
            with h.section({'id': 'preview'}):
                h.h2({}, 'Preview')
                h.p({}, 'Sed ultricies dolor non ante vulputate hendrerit. Vivamus sit amet suscipit sapien. Nulla iaculis eros a elit pharetra egestas.')

                with h.form():
                    with h.div({'class': 'grid'}):
                        h.input({'type': 'text', 'name': 'firstname', 'placeholder': 'First name', 'aria-label': 'First name', 'required': ''})
                        h.input({'type': 'email', 'name': 'email', 'placeholder': 'Email address', 'aria-label': 'Email address', 'autocomplete': 'email', 'required': ''})
                        h.button({'type': 'submit'}, 'Subscribe')

                    with h.fieldset():
                        with h.label({'for': 'terms'}):
                            h.input({'type': 'checkbox', 'role': 'switch', 'id': 'terms', 'name': 'terms'})
                            h.text('I agree to the ')
                            h.a({'href': '#', 'onclick': 'event.preventDefault()'}, 'Privacy Policy')

            with h.section({'id': 'typography'}):
                h.h2({}, 'Typography')
                h.p({}, 'Aliquam lobortis vitae nibh nec rhoncus. Morbi mattis neque eget efficitur feugiat. Vivamus porta nunc a erat mattis, mattis feugiat turpis pretium. Quisque sed tristique felis.')

                with h.blockquote():
                    h.text('"Maecenas vehicula metus tellus, vitae congue turpis hendrerit non. Nam at dui sit amet ipsum cursus ornare."')

                    with h.footer():
                        h.cite({}, '- Phasellus eget lacinia')

                h.h3({}, 'Lists')

                with h.ul():
                    h.li({}, 'Aliquam lobortis lacus eu libero ornare facilisis.')
                    h.li({}, 'Nam et magna at libero scelerisque egestas.')
                    h.li({}, 'Suspendisse id nisl ut leo finibus vehicula quis eu ex.')
                    h.li({}, 'Proin ultricies turpis et volutpat vehicula.')

                h.h3({}, 'Inline text elements')

                with h.div({'class': 'grid'}):
                    h.p({}, h.a({'href': '#', 'onclick': 'event.preventDefault()'}, 'Primary link'))
                    h.p({}, h.a({'href': '#', 'class': 'secondary', 'onclick': 'event.preventDefault()'}, 'Secondary link'))
                    h.p({}, h.a({'href': '#', 'class': 'contrast', 'onclick': 'event.preventDefault()'}, 'Contrast link'))

                with h.div({'class': 'grid'}):
                    h.p({}, h.strong({}, 'Bold'))
                    h.p({}, h.em({}, 'Italic'))
                    h.p({}, h.u({}, 'Underline'))

                with h.div({'class': 'grid'}):
                    h.p({}, h.del_({}, 'Deleted')) # 'del' is a Python keyword, use 'del_' instead
                    h.p({}, h.ins({}, 'Inserted'))
                    h.p({}, h.s({}, 'Strikethrough'))

                with h.div({'class': 'grid'}):
                    h.p({}, h.small({}, 'Small '))
                    h.p({}, 'Text ', h.sub({}, 'Sub'))
                    h.p({}, 'Text ', h.sup({}, 'Sup'))

                with h.div({'class': 'grid'}):
                    h.p({}, h.abbr({'title': 'Abbreviation', 'data-tooltip': 'Abbreviation'}, 'Abbr.'))
                    h.p({}, h.kbd({}, 'Kbd'))
                    h.p({}, h.mark({}, 'Highlighted'))

                h.h3({}, 'Heading 3')
                h.p({}, 'Integer bibendum malesuada libero vel eleifend. Fusce iaculis turpis ipsum, at efficitur sem scelerisque vel. Aliquam auctor diam ut purus cursus fringilla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.')
                h.h4({}, 'Heading 4')
                h.p({}, 'Cras fermentum velit vitae auctor aliquet. Nunc non congue urna, at blandit nibh. Donec ac fermentum felis. Vivamus tincidunt arcu ut lacus hendrerit, eget mattis dui finibus.')
                h.h5({}, 'Heading 5')
                h.p({}, 'Donec nec egestas nulla. Sed varius placerat felis eu suscipit. Mauris maximus ante in consequat luctus. Morbi euismod sagittis efficitur. Aenean non eros orci. Vivamus ut diam sem.')
                h.h6({}, 'Heading 6')
                h.p({}, 'Ut sed quam non mauris placerat consequat vitae id risus. Vestibulum tincidunt nulla ut tortor posuere, vitae malesuada tortor molestie. Sed nec interdum dolor. Vestibulum id auctor nisi, a efficitur sem. Aliquam sollicitudin efficitur turpis, sollicitudin hendrerit ligula semper id. Nunc risus felis, egestas eu tristique eget, convallis in velit.')

                with h.figure():
                    h.img({'src': 'img/aleksandar-jason-a562ZEFKW8I-unsplash-2000x1000.jpg', 'alt': 'Minimal landscape'})

                    with h.figcaption():
                        h.text('Image from ')
                        h.a({'href': 'https://unsplash.com/photos/a562ZEFKW8I', 'target': '_blank'}, 'unsplash.com')

            with h.section({'id': 'buttons'}):
                h.h2({}, 'Buttons')

                with h.p({'class': 'grid'}):
                    h.button({}, 'Primary')
                    h.button({'class': 'secondary'}, 'Secondary')
                    h.button({'class': 'contrast'}, 'Contrast')

                with h.p({'class': 'grid 2'}):
                    h.button({'class': 'outline'}, 'Primary outline')
                    h.button({'class': 'outline secondary'}, 'Secondary outline')
                    h.button({'class': 'outline contrast'}, 'Contrast outline')

            with h.section({'id': 'form'}):
                with h.form():
                    h.h2({}, 'Form elements')
                    h.label({'for': 'search'}, 'Search')
                    h.input({'type': 'search', 'id': 'search', 'name': 'search', 'placeholder': 'Search'})
                    h.label({'for': 'text'}, 'Text')
                    h.input({'type': 'text', 'id': 'text', 'name': 'text', 'placeholder': 'Text'})
                    h.small({}, 'Curabitur consequat lacus at lacus porta finibus.')
                    h.label({'for': 'select'}, 'Select')

                    with h.select({'id': 'select', 'name': 'select', 'required': ''}):
                        h.option({'value': '', 'selected': ''}, 'Select…')
                        h.option({}, '…')

                    with h.label({'for': 'file'}):
                        h.text('File browser')
                        h.input({'type': 'file', 'id': 'file', 'name': 'file'})

                    with h.label({'for': 'range'}):
                        h.text('Range slider')
                        h.input({'type': 'range', 'min': '0', 'max': '100', 'value': '50', 'id': 'range', 'name': 'range'})

                    with h.div({'class': 'grid'}):
                        with h.label({'for': 'valid'}):
                            h.text('Valid')
                            h.input({'type': 'text', 'id': 'valid', 'name': 'valid', 'placeholder': 'Valid', 'aria-invalid': 'false'})

                        with h.label({'for': 'invalid'}):
                            h.text('Invalid')
                            h.input({'type': 'text', 'id': 'invalid', 'name': 'invalid', 'placeholder': 'Invalid', 'aria-invalid': 'true'})

                        with h.label({'for': 'disabled'}):
                            h.text('Disabled')
                            h.input({'type': 'text', 'id': 'disabled', 'name': 'disabled', 'placeholder': 'Disabled', 'disabled': ''})

                    with h.div({'class': 'grid'}):
                        with h.label({'for': 'date'}):
                            h.text('Date')
                            h.input({'type': 'date', 'id': 'date', 'name': 'date'})

                        with h.label({'for': 'time'}):
                            h.text('Time')
                            h.input({'type': 'time', 'id': 'time', 'name': 'time'})

                        with h.label({'for': 'color'}):
                            h.text('Color')
                            h.input({'type': 'color', 'id': 'color', 'name': 'color', 'value': '#0eaaaa'})

                    with h.div({'class': 'grid'}):
                        with h.fieldset():
                            h.legend({}, h.strong({}, 'Checkboxes'))

                            with h.label({'for': 'checkbox-1'}):
                                h.input({'type': 'checkbox', 'id': 'checkbox-1', 'name': 'checkbox-1', 'checked': ''})
                                h.text('Checkbox')

                            with h.label({'for': 'checkbox-2'}):
                                h.input({'type': 'checkbox', 'id': 'checkbox-2', 'name': 'checkbox-2'})
                                h.text('Checkbox')
                        with h.fieldset():
                            h.legend({}, h.strong({}, 'Radio buttons'))

                            with h.label({'for': 'radio-1'}):
                                h.input({'type': 'radio', 'id': 'radio-1', 'name': 'radio', 'value': 'radio-1', 'checked': ''})
                                h.text('Radio button')

                            with h.label({'for': 'radio-2'}):
                                h.input({'type': 'radio', 'id': 'radio-2', 'name': 'radio', 'value': 'radio-2'})
                                h.text('Radio button')
                        with h.fieldset():
                            h.legend({}, h.strong({}, 'Switches'))

                            with h.label({'for': 'switch-1'}):
                                h.input({'type': 'checkbox', 'id': 'switch-1', 'name': 'switch-1', 'role': 'switch', 'checked': ''})
                                h.text('Switch')

                            with h.label({'for': 'switch-2'}):
                                h.input({'type': 'checkbox', 'id': 'switch-2', 'name': 'switch-2', 'role': 'switch'})
                                h.text('Switch')

                    h.input({'type': 'reset', 'value': 'Reset', 'onclick': 'event.preventDefault()'})
                    h.input({'type': 'submit', 'value': 'Submit', 'onclick': 'event.preventDefault()'})

            with h.section({'id': 'tables'}):
                h.h2({}, 'Tables')

                with h.div({'class': 'overflow-auto'}):
                    with h.table({'class': 'striped'}):
                        with h.thead():
                            with h.tr():
                                h.th({'scope': 'col'}, '#')
                                h.th({'scope': 'col'}, 'Heading')
                                h.th({'scope': 'col'}, 'Heading')
                                h.th({'scope': 'col'}, 'Heading')
                                h.th({'scope': 'col'}, 'Heading')
                                h.th({'scope': 'col'}, 'Heading')
                                h.th({'scope': 'col'}, 'Heading')
                                h.th({'scope': 'col'}, 'Heading')

                        with h.tbody():
                            with h.tr():
                                h.th({'scope': 'row'}, '1')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')

                            with h.tr():
                                h.th({'scope': 'row'}, '2')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')

                            with h.tr():
                                h.th({'scope': 'row'}, '3')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')
                                h.td({}, 'Cell')

            with h.section({'id': 'modal'}):
                h.h2({}, 'Modal')
                h.button({'class': 'contrast', 'data-target': 'modal-example', 'onclick': 'toggleModal(event)'}, 'Launch demo modal')

            with h.section({'id': 'accordions'}):
                h.h2({}, 'Accordions')

                with h.details():
                    h.summary({}, 'Accordion 1')
                    h.p({}, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque urna diam, tincidunt nec porta sed, auctor id velit. Etiam venenatis nisl ut orci consequat, vitae tempus quam commodo. Nulla non mauris ipsum. Aliquam eu posuere orci. Nulla convallis lectus rutrum quam hendrerit, in facilisis elit sollicitudin. Mauris pulvinar pulvinar mi, dictum tristique elit auctor quis. Maecenas ac ipsum ultrices, porta turpis sit amet, congue turpis.')

                with h.details({'open': ''}):
                    h.summary({}, 'Accordion 2')

                    with h.ul():
                        h.li({}, 'Vestibulum id elit quis massa interdum sodales.')
                        h.li({}, 'Nunc quis eros vel odio pretium tincidunt nec quis neque.')
                        h.li({}, 'Quisque sed eros non eros ornare elementum.')
                        h.li({}, 'Cras sed libero aliquet, porta dolor quis, dapibus ipsum.')

            with h.article({'id': 'article'}):
                h.h2({}, 'Article')
                h.p({}, 'Nullam dui arcu, malesuada et sodales eu, efficitur vitae dolor. Sed ultricies dolor non ante vulputate hendrerit. Vivamus sit amet suscipit sapien. Nulla iaculis eros a elit pharetra egestas. Nunc placerat facilisis cursus. Sed vestibulum metus eget dolor pharetra rutrum.')

                with h.footer({}):
                    h.small({}, 'Duis nec elit placerat, suscipit nibh quis, finibus neque.')

            with h.section({'id': 'group'}):
                h.h2({}, 'Group')

                with h.form():
                    with h.fieldset({'role': 'group'}):
                        h.input({'name': 'email', 'type': 'email', 'placeholder': 'Enter your email', 'autocomplete': 'email'})
                        h.input({'type': 'submit', 'value': 'Subscribe'})

            with h.section({'id': 'progress'}):
                h.h2({}, 'Progress bar')
                h.progress({'id': 'progress-1', 'value': '25', 'max': '100'})
                h.progress({'id': 'progress-2'})

            with h.section({'id': 'loading'}):
                h.h2({}, 'Loading')
                h.article({'aria-busy': 'true'})
                h.button({'aria-busy': 'true'}, 'Please wait…')

        with h.footer({'class': 'container'}):
            with h.small({}):
                h.text('Built with ')
                h.a({'href': 'https://picocss.com'}, 'Pico')
                h.text(' • ')
                h.a({'href': 'https://github.com/picocss/examples/blob/master/v2-html/index.html'}, 'Source code')

        with h.dialog({'id': 'modal-example'}):
            with h.article():
                with h.header():
                    h.button({'aria-label': 'Close', 'rel': 'prev', 'data-target': 'modal-example', 'onclick': 'toggleModal(event)'})
                    h.h3({}, 'Confirm your action!')

                h.p({}, 'Cras sit amet maximus risus. Pellentesque sodales odio sit amet augue finibus pellentesque. Nullam finibus risus non semper euismod.')

                with h.footer():
                    h.button({'role': 'button', 'class': 'secondary', 'data-target': 'modal-example', 'onclick': 'toggleModal(event)'}, 'Cancel')
                    h.button({'autofocus': '', 'data-target': 'modal-example', 'onclick': 'toggleModal(event)'}, 'Confirm')

        h.script({'src': 'js/minimal-theme-switcher.js'})
        h.script({'src': 'js/modal.js'})


# server
app = web.Application()
routes = web.RouteTableDef()
routes.static('/js', './js')
routes.static('/css', './css')
routes.static('/img', './img')


@routes.get('/')
async def variable_handler(request):
    text = render(html_root)
    headers = {'content-type': 'text/html'}
    return web.Response(status=200, text=text, headers=headers)


app.add_routes(routes)

if __name__ == '__main__':
    run_app(app)
