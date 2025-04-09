import os
from random import randint
from gladius import create_app, run_app

import client.app
import client.components.App # type: ignore

print(client.app)
print(client.components.App)


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
    # npm_post_bundle=[
    #     [
    #         'esbuild',
    #         'client/components/App.tsx',
    #         '--jsx-factory=h',
    #         # '--jsx-fragment=Fragment',
    #         '--format=esm',
    #         '--platform=node',
    #         '--bundle',
    #         '--sourcemap',
    #         '--loader:.jsx=jsx',
    #         '--loader:.tsx=tsx',
    #         f'--outfile={os.path.join(os.getcwd(), 'static/__app__/components/App.js')}',
    #     ]
    # ],
    # client_ready=client.components.App,
    # ready=[client.app, client.components.App],
    # ready=client.app,
    ready=client.components.App,
)

# # server-side structure
# with page['head']:
#     g.script(f'''
#         import * as App from '/static/__app__/components/App.js?v={randint(0, 2 ** 32)}';
#     ''', type='module', defer=None)

# start application
if __name__ == '__main__':
    run_app(app, host='0.0.0.0', port=5000)
