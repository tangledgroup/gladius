from aiohttp import web
from gladius.starter import create_aiohttp_app

# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

# initialize gladius
g, page, app = create_aiohttp_app(npm_packages=npm_packages)

# client-side click handler
def load_cb():
    from pyscript import when
    from pyscript.web import page
    from pyscript.js_modules.nprogress import default as NProgress

    btn = page['#hello-button'][0]  # get server-created button
    clicked = 0                     # track clicks

    @when('click', btn)
    def on_click(event):
        global clicked
        NProgress.start()
        clicked += 1
        btn.innerText = f'Clicked {clicked} time{"s" if clicked !=1 else ""}!'
        NProgress.done()

# server-side structure
with page:
    with g.body(x_data=None):
        with g.main(class_='container'):
            g.h1('Gladius Demo')
            g.button('Click me!', id='hello-button')    # create button on server

        g.script(load_cb)                               # attach client logic

# start application
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
