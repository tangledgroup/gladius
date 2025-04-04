from aiohttp import web
from gladius.starter import create_aiohttp_app

# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
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
    with g.body():
        with g.main(class_='container'):
            g.h1('Gladius Demo')
            g.button('Click me!', id='hello-button')    # create button on server

# start application
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
