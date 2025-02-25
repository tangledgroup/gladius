from aiohttp import web
from gladius.starter import create_aiohttp_app

# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'alpinejs': ['dist/module.esm.js'],
    'pinecone-router': ['dist/router.esm.js'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

# create simple aiohttp web server
g, page, app = create_aiohttp_app(
    npm_packages=npm_packages, # type: ignore
    use_brython=True,
    ready='client_app.py',
)

# server-side structure
with page:
    with g.body(x_data=None):
        with g.main(class_='container'):
            g.h1('Gladius Demo - Messages')

            with g.div(class_='form'):
                with g.fieldset(role='group'):
                    g.input(name='message', type='text', placeholder='Enter your message', autocomplete='off', id='message', x_on__c__keydown='send')
                    g.input(type='submit', value='Send', x_on__c__click='send')

            with g.template(x_for='m in $store.messages.items'):
                g.p(x_text='m')

# start application
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
