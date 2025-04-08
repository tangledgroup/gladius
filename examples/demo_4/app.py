from gladius import create_app, run_app, capture_imports

with capture_imports() as module_map:
    import client_app


# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'alpinejs': ['dist/module.esm.js'],
    'pinecone-router': ['dist/router.esm.js'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

# create simple aiohttp web server
g, page, app = create_app(
    npm_packages=npm_packages,
    module_map=module_map,
    ready=client_app,
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
    run_app(app, host='0.0.0.0', port=5000)
