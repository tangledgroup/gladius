from gladius import create_app, run_app

import client.app


# npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

# create simple aiohttp web app
g, page, app = create_app(
    npm_packages=npm_packages,
    ready=client.app,
)

# server-side structure
with page['body']:
    with g.main(class_='container'):
        g.h1('Gladius Demo')
        g.button('Click me!', id='hello-button') # create button on server

# start web server running application
if __name__ == '__main__':
    run_app(app, host='0.0.0.0', port=5000)
