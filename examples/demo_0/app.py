# from aiohttp import web
from gladius.starter import create_aiohttp_app


npm_packages = {
    '@pyscript/core': {
        'version': '*',
        'copy': {
            'dist/core.js': 'pyscript/',
            'dist/core.css': 'pyscript/',
        }
    },
    '@micropython/micropython-webassembly-pyscript': {
        'version': '*',
        'copy': {
            'micropython.mjs': 'pyscript/',
            'micropython.wasm': 'pyscript/',
        }
    },
    '@picocss/pico': {
        'version': '*',
        'bundle': {
            'css/pico.css': 'pico/',
        }
    },
    'alpinejs': {
        'version': '*',
        'bundle': {
            'dist/cdn.js': 'alpinejs/alpinejs.js',
        },
    },
    'nprogress': {
        'version': '*',
        'copy': {
            'nprogress.js': 'nprogress/',
            'nprogress.css': 'nprogress/',
        }
    },
}

g, page, app = create_aiohttp_app(npm_packages=npm_packages)

# with page:
#     with g.body(x_data=None):
#         pass

# if __name__ == '__main__':
#     web.run_app(app, host='0.0.0.0', port=5000)
