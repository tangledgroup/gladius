from aiohttp import web
from gladius import Element
from gladius.starter import create_aiohttp_app

# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
    'alpinejs': ['dist/module.esm.js'],
    'pinecone-router': ['dist/router.esm.js'],
}

# create simple aiohttp web server
g, page, app = create_aiohttp_app(
    npm_packages=npm_packages, # type: ignore
    ready='client_app.py',
)

# server-side structure
with page:
    with g.body(class_='container', x_data=None):
        with g.header():
            with g.nav():
                with g.ul():
                    with g.li():
                        with g.a(class_='secondary', href='/', native=True, style='text-decoration: none;'):
                            g.img(src='/static/img/favicon.png', width='24px', height='24px')
                            g.strong('Notes Manager')

                with g.ul():
                    with g.li():
                        g.a('Notes', href='/notes')

                    with g.li():
                        g.a('Tags', href='/tags')

        with g.main():
            g.div(id='app')

        with g.footer():
            pass

#
# templates
#
routes = web.RouteTableDef()


@routes.get('/api/1.0/templates/notes') # type: ignore
async def api_1_0_templates_notes(request: web.Request) -> Element:
    with g.div() as el:
        g.h1('Notes')

        with g.div(class_='form'):
            with g.fieldset(role='group'):
                g.input(
                    id='title',
                    type='text',
                    name='title',
                    placeholder='Enter title',
                    autocomplete='off',
                    x_on__c__keydown='add_note_cb', # x-on:keydown
                )

                g.input(
                    type='submit',
                    value='Add',
                    x_on__c__click='add_note_cb', # x-on:click
                )

        with g.template(x_for='(n, i) in $store.notes.items'):
            with g.div(class_='form'):
                with g.fieldset(role='group'):
                    g.input(type='text', x_model='n.title', disabled=True)

                    g.button(
                        'Remove',
                        class_='secondary',
                        x_bind__c__i='i', # x-bind:i
                        x_on__c__click='remove_note_cb', # x-on:click
                    )

                    g.button(
                        'View',
                        class_='contrast',
                        x_bind__c__i='i', # x-bind:i
                        x_on__c__click='view_note_cb', # x-on:click
                    )

    return el


@routes.get('/api/1.0/templates/note') # type: ignore
async def api_1_0_templates_note(request: web.Request) -> Element:
    with g.div() as el:
        g.h1('Note')

        g.h5('Title:')

        g.input(
            id='title',
            name='title',
            x_model='$store.note.title'
        )

        g.h5('Content:')

        g.textarea(
            id='content',
            name='content',
            x_model='$store.note.content'
        )

        g.h5('Tags:')

        with g.details(class_='dropdown'):
            g.summary(
                x_text='$store.note.tags.length ? $store.note.tags.join(\', \') : \'Tags\'',
            )

            with g.ul():
                with g.template(x_for='(t, i) in $store.tags.items'):
                    with g.li():
                        with g.label():
                            g.input(
                                type='checkbox',
                                x_bind__c__name='t',
                                x_bind__c__value='$store.note.tags.includes(t)',
                                x_on__c__click='note_tag_checkbox_cb',
                            )

                            g.span(x_text='t')

        g.button(
            'Update',
            x_bind__c__i='$router.params.index', # x-bind:i
            x_on__c__click='update_note_cb', # x-on:click
        )


    return el


@routes.get('/api/1.0/templates/tags') # type: ignore
async def api_1_0_templates_tags(request: web.Request) -> Element:
    with g.div() as el:
        g.h1('Tags')

        with g.div(class_='form'):
            with g.fieldset(role='group'):
                g.input(
                    id='tag',
                    type='text',
                    name='tag',
                    placeholder='Enter tag',
                    autocomplete='off',
                    x_on__c__keydown='add_tag_cb', # x-on:keydown
                )

                g.input(
                    type='submit',
                    value='Add',
                    x_on__c__click='add_tag_cb', # x-on:click
                )

        with g.template(x_for='(t, i) in $store.tags.items'):
            with g.div(class_='form'):
                with g.fieldset(role='group'):
                    g.input(type='text', x_model='t', disabled=True)

                    g.button(
                        'Remove',
                        class_='secondary',
                        x_bind__c__i='i', # x-bind:i
                        x_on__c__click='remove_tag_cb', # x-on:click
                    )

    return el


app.add_routes(routes)

# start application
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
