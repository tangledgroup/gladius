from gladius import create_app, run_app

import client.app # type: ignore
import client.style # type: ignore


# required npm packages
npm_packages = {
    'tailwindcss': [],
    'daisyui': [],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

# create simple aiohttp web server
g, page, app = create_app(
    npm_packages=npm_packages,
    ready=[
        client.app,
        client.style,
    ],
)

with page['body']:
    g.h1('Gladius Demo')
    g.button('Click me!', id='hello-button', class_='btn btn-primary') # create button on server

# start application
if __name__ == '__main__':
    run_app(app)
