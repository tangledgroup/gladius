from aiohttp import web
from gladius.starter import create_aiohttp_app


npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'alpinejs': ['dist/module.esm.js'],
    'pinecone-router': ['dist/router.esm.js'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

g, page, app = create_aiohttp_app(npm_packages=npm_packages) # type: ignore


def load_cb():
    from pyscript import document, window # type: ignore
    from pyscript.js_modules.alpinejs import Alpine # type: ignore
    from pyscript.js_modules.pinecone_router import default as PineconeRouter # type: ignore


    window.Alpine = Alpine


    def alpine_init(event):
        print('alpine:init', event)


    document.addEventListener('alpine:init', alpine_init)
    Alpine.plugin(PineconeRouter)
    Alpine.start()

    document.body.append('Hello from PyScript')


with page:
    with g.body(x_data=None):
        with g.main(class_='container'):
              g.h1('Hello world!')

        g.script(load_cb)


if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
