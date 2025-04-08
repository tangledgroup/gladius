from gladius import create_app, run_app, capture_imports

with capture_imports() as module_map:
    from client_utils import f0 # noqa


# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

# client-side click handler
def ready():
    from gladius import window, document, bind # type: ignore
    from client_utils import f0

    NProgress = window.nprogress.default

    btn = document.getElementById('hello-button') # get server-created button
    clicked = 0                                   # track clicks # noqa


    @bind(btn, 'click')
    def on_click(event):
        global clicked
        NProgress.start()
        clicked += 1 # type: ignore
        btn.innerText = f'Clicked {clicked} time{"s" if clicked !=1 else ""}!'
        print(f0(clicked, clicked))
        NProgress.done()


# create simple aiohttp web server
g, page, app = create_app(
    npm_packages=npm_packages,
    module_map=module_map,
    ready=ready,
    app_init_args={
        'client_max_size': 1024 ** 3,
    }
)

# server-side structure
with page:
    with g.body():
        with g.main(class_='container'):
            g.h1('Gladius Demo')
            g.button('Click me!', id='hello-button')    # create button on server

# start application
if __name__ == '__main__':
    run_app(app, host='0.0.0.0', port=5000)
