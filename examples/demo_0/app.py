from aiohttp import web
from gladius.starter import create_aiohttp_app


npm_packages = {
    '@pyscript/core': '*',
    '@micropython/micropython-webassembly-pyscript': '*',
    '@picocss/pico': ['*', 'css/pico.css'],
    'alpinejs': '*',
    'nprogress': '*',
}

g, page, app = create_aiohttp_app(npm_packages=npm_packages)

with page:
    with g.body(x_data=None):
        pass

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
