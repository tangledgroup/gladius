# from aiohttp import web
from gladius.starter import create_aiohttp_app


npm_packages = {
    # '@pyscript/core': {
    #     # 'version': '*',
    #     # 'copy': {
    #     #     'dist/core.js': '@pyscript/core/',
    #     #     'dist/core.css': '@pyscript/core/',
    #     # },
    #     'copy': ['dist/core.js', 'dist/core.css']
    # },
    '@pyscript/core': ['dist/core.js', 'dist/core.css'],
    # '@micropython/micropython-webassembly-pyscript': {
    #     # 'version': '*',
    #     # 'copy': {
    #     #     'micropython.mjs': '@micropython/micropython-webassembly-pyscript/',
    #     #     'micropython.wasm': '@micropython/micropython-webassembly-pyscript/',
    #     # }
    #     'copy': ['micropython.mjs', 'micropython.wasm']
    # },
    '@micropython/micropython-webassembly-pyscript': ['micropython.mjs', 'micropython.wasm'],
    # '@picocss/pico': {
    #     # 'version': '*',
    #     # 'bundle': {
    #     #     'css/pico.css': '@picocss/pico/',
    #     # }
    #     'bundle': ['css/pico.css']
    # },
    '@picocss/pico': ['css/pico.css'],
    # 'alpinejs': {
    #     # 'version': '*',
    #     # 'bundle': {
    #     #     'dist/cdn.js': 'alpinejs/alpinejs.js',
    #     # },
    #     'bundle': ['dist/cdn.js']
    # },
    'alpinejs': ['dist/cdn.js'],
    # 'nprogress': {
    #     # 'version': '*',
    #     # 'copy': {
    #     #     'nprogress.js': 'nprogress/',
    #     #     'nprogress.css': 'nprogress/',
    #     # }
    #     'copy': ['nprogress.js', 'nprogress.css']
    # },
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

g, page, app = create_aiohttp_app(npm_packages=npm_packages)

# with page:
#     with g.body(x_data=None):
#         pass

# if __name__ == '__main__':
#     web.run_app(app, host='0.0.0.0', port=5000)
