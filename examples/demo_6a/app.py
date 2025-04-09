import os
from random import randint
from gladius import create_app, run_app, capture_imports

with capture_imports() as module_map:
    import client_app


# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'alpinejs': ['dist/module.esm.js'],
    'pinecone-router': ['dist/router.esm.js'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
    'vhtml': ['src/vhtml.js'],
}

# create simple aiohttp web server
g, page, app = create_app(
    npm_packages=npm_packages,
    npm_post_bundle=[
        [
            'esbuild',
            'components/App.jsx',
            '--jsx-factory=h',
            # '--jsx-fragment=Fragment',
            '--bundle',
            '--loader:.jsx=jsx',
            f'--outfile={os.path.join(os.getcwd(), 'static/__app__/App.js')}',
            '--global-name=app',
        ]
    ],
    module_map=module_map,
    ready=client_app,
)

# server-side structure
with page['head']:
    g.script(src=f'static/__app__/App.js?v={randint(0, 2 ** 32)}', defer=None)

# start application
if __name__ == '__main__':
    run_app(app, host='0.0.0.0', port=5000)
