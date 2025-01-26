from aiohttp import web
from gladius.starter import create_aiohttp_app

# list packages from https://npmjs.com, and files that need to be transpiled
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

# create simple aiohttp web server
g, page, app = create_aiohttp_app(npm_packages=npm_packages) # type: ignore

# client-side code, never executed on server-side
def on_load():
    # this code is run on client-side only
    from pyscript import document, window, when # type: ignore
    from pyscript.web import page, button # type: ignore

    # import nprogress package
    # https://github.com/rstacruz/nprogress
    from pyscript.js_modules.nprogress import default as NProgress # type: ignore

    # get main element and append a button
    main = page['main'][0]

    main.append(
        button('Hello from PyScript', id='hello-button'),
    )

    # get button element
    btn = page['#hello-button'][0]
    clicked: int = 0

    # listen for the click event on the button element
    # and keep updating how many times it was clicked
    # additionally start/stop NProgress
    @when('click', btn)
    def my_button_click_handler(event):
        global clicked
        NProgress.start()
        clicked += 1
        btn.innerText = f'The button has been clicked {clicked} time{"" if clicked == 1 else "s"}!'
        NProgress.done()


# create page, body, main, h1 elements
# and attach client-side script which pysciprt will execute once page is loaded
with page:
    with g.body(x_data=None):
        with g.main(class_='container'):
              g.h1('Hello world!')

        # attach client-side python script
        g.script(on_load)


# run server
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
