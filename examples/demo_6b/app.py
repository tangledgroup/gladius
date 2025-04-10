from gladius import create_app, run_app

import client.app
import client.components.App # type: ignore


# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'alpinejs': [],
    'pinecone-router': [],
    'nprogress': [],
    'vhtml': [],
    '@types/vhtml': [],
}

# create simple aiohttp web server
g, page, app = create_app(
    npm_packages=npm_packages,
    ready=[
        client.app,
        client.components.App,
    ],
)

# start application
if __name__ == '__main__':
    run_app(app, host='0.0.0.0', port=5000)
