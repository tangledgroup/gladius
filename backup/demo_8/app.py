import os
from random import randint
from gladius import create_app, run_app


# required npm packages
npm_packages = {
    'tailwindcss@4.1.3': [],
    '@tailwindcss/cli': [],
    'daisyui': [],
    'nprogress': ['nprogress.js', 'nprogress.css'],
    'lodash@4.17.21': ['index.js'],
    # 'lodash@3.10.1': ['index.js'],
}

# client-side click handler
def ready():
    from gladius import window, document, bind # type: ignore

    NProgress = window.nprogress.default

    btn = document.getElementById('hello-button') # get server-created button
    clicked = 0                                   # track clicks # noqa


    @bind(btn, 'click')
    def on_click(event):
        global clicked
        NProgress.start()
        clicked += 1 # type: ignore
        btn.innerText = f'Clicked {clicked} time{"s" if clicked !=1 else ""}!'
        NProgress.done()


# create simple aiohttp web server
g, page, app = create_app(
    npm_packages=npm_packages,
    npm_post_bundle=[
        ['@tailwindcss/cli', '-i', 'style.css', '-o', os.path.join(os.getcwd(), 'static/__app__/style.css')],
    ],
    ready=ready,
    app_init_args={
        'client_max_size': 1024 ** 3,
    }
)

# server-side structure
with page['head']:
    g.link(rel='stylesheet', href=f'static/__app__/style.css?v={randint(0, 2 ** 32)}')

with page['body']:
    g.h1('Gladius Demo')
    g.button('Click me!', id='hello-button', class_='btn btn-primary') # create button on server

# start application
if __name__ == '__main__':
    run_app(app, host='0.0.0.0', port=5000)
