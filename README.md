# gladius

<!--
[![Build][build-image]]()
[![Status][status-image]][pypi-project-url]
[![Stable Version][stable-ver-image]][pypi-project-url]
[![Coverage][coverage-image]]()
[![Python][python-ver-image]][pypi-project-url]
[![License][mit-image]][mit-url]
-->
[![Downloads](https://img.shields.io/pypi/dm/gladius)](https://pypistats.org/packages/gladius)
[![Supported Versions](https://img.shields.io/pypi/pyversions/gladius)](https://pypi.org/project/gladius)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

<img src="https://github.com/mtasic85/gladius/raw/main/misc/logo-1.png" alt="" style="display: block; margin: auto;" />

**Gladius** aka "gladius" is a library facilitating web application development exclusively in pure **Python**, eliminating the need for HTML, CSS, or JavaScript/TypeScript.

Built for developers who want to leverage Python across the entire stack, Gladius provides access to modern web framework features while mirroring patterns familiar to full-stack Python developers. These developers often blend Python on the server with traditional JavaScript/CSS tools for frontend UI—Gladius simplifies this workflow by enabling Python-driven UI development, reducing context-switching between languages.

For traditional frontend developers, Gladius offers a comfortable transition by exposing all standard Web APIs available in browsers. This ensures compatibility with existing NPM packages (from npmjs), allowing seamless integration of JavaScript libraries when needed.

By unifying frontend and backend development under Python, Gladius delivers a cohesive, intuitive experience—ideal for developers seeking a Python-centric approach without sacrificing access to the broader web ecosystem.


## Install
```bash
pip install gladius[all]
```

## Hello World

Create `app.py` file with content:

```python
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
def load_cb():
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
        g.script(load_cb)


# run server
if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
```

Run python app with simple server in background:

```bash
python -B app.py
```

Or, in case you want to rebuild on code change:

```bash
watchmedo auto-restart --directory=./ --pattern="*.py" --recursive -- python -B app.py
```

<!--
**Gladius** aka "gladius" is a **full-stack web framework** facilitating web application development exclusively in pure **Python**, eliminating the need for HTML, CSS, or JavaScript. It is built for those who prefer to use Python, providing access to features typically found in modern web frameworks.

In essence, gladius offers a simplified and cohesive development experience, making it a practical choice for developers seeking a Python-centric approach to both frontend and backend development.

## Hello World

```python
# ...
```

## Install
```bash
pip install gladius
```

## Run Examples

```bash
git clone https://github.com/tangledgroup/gladius.git
cd gladius
python -m venv venv
source venv/bin/activate
pip install -U -r requirements.txt
```

```bash
watchmedo auto-restart --directory=./ --pattern="*.py;*.html;*.hbs;*.css;*.js" --recursive -- python -B examples/pico_preview/app.py
watchmedo auto-restart --directory=./ --pattern="*.py;*.html;*.hbs;*.css;*.js" --recursive -- python -B examples/pico_tailwind_lite/app.py
watchmedo auto-restart --directory=./ --pattern="*.py;*.html;*.hbs;*.css;*.js" --recursive -- python -B examples/pico_demo_0/app.py
watchmedo auto-restart --directory=./ --pattern="*.py;*.html;*.hbs;*.css;*.js" --recursive -- python -B examples/pico_demo_1/app.py
watchmedo auto-restart --directory=./ --pattern="*.py;*.html;*.hbs;*.css;*.js" --recursive -- python -B examples/pico_demo_2/app.py
watchmedo auto-restart --directory=./ --pattern="*.py;*.html;*.hbs;*.css;*.js" --recursive -- python -B examples/pico_demo_3/app.py
watchmedo auto-restart --directory=./ --pattern="*.py;*.html;*.hbs;*.css;*.js" --recursive -- python -B examples/pico_demo_4/app.py
watchmedo auto-restart --directory=./ --pattern="*.py;*.html;*.hbs;*.css;*.js" --recursive -- python -B examples/pico_demo_5/app.py
```

```bash
python -B -u -m gunicorn --reload --bind '0.0.0.0:5000' --timeout 300 --workers 1 --worker-class aiohttp.GunicornWebWorker 'examples.pico_demo_1.app:app'
python -B -u -m gunicorn --reload --bind '0.0.0.0:5000' --timeout 300 --workers 1 --worker-class aiohttp.GunicornWebWorker 'examples.pico_demo_2.app:app'
python -B -u -m gunicorn --reload --bind '0.0.0.0:5000' --timeout 300 --workers 1 --worker-class aiohttp.GunicornWebWorker 'examples.pico_demo_3.app:app'
python -B -u -m gunicorn --reload --bind '0.0.0.0:5000' --timeout 300 --workers 1 --worker-class aiohttp.GunicornWebWorker 'examples.pico_demo_4.app:app'
python -B -u -m gunicorn --reload --bind '0.0.0.0:5000' --timeout 300 --workers 1 --worker-class aiohttp.GunicornWebWorker 'examples.pico_demo_5.app:app'
```
-->
