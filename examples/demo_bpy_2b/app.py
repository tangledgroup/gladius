import os
from aiohttp import web
from gladius.starter import create_aiohttp_app

# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'alpinejs': ['dist/module.esm.js'],
    'pinecone-router': ['dist/router.esm.js'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
    'handlebars': ['dist/handlebars.js'],
}

# create simple aiohttp web server
g, page, app = create_aiohttp_app(
    npm_packages=npm_packages, # type: ignore
    use_brython=True,
    ready='client_app.py',
)

# server-side structure
with page:
    for root, dirs, files in os.walk(os.path.join('components')):
        for name in files:
            path = os.path.join(root, name)

            with open(path) as f:
                content: str = f.read()

            basename, ext = os.path.splitext(name)
            g.script(content, path=path, name=basename, type='handlebars')

    with g.body(x_data=None):
        pass


# start application
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
