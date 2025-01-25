from aiohttp import web
from gladius.starter import create_aiohttp_app


npm_packages = {
    '@pyscript/core': ['dist/core.js', 'dist/core.css'],
    '@micropython/micropython-webassembly-pyscript': ['micropython.mjs', 'micropython.wasm'],
    '@picocss/pico': ['css/pico.css'],
    'alpinejs': ['dist/cdn.js'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

g, page, app = create_aiohttp_app(npm_packages=npm_packages)

# print(page['head'])

with page:
    with g.body(x_data=None):
        with g.main(class_='container'):
              g.h1('Hello world!')

        g.script('''
from pyscript import document

document.body.append("Hello from PyScript")
''', type='mpy')


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
