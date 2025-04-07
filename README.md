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

<img src="https://github.com/mtasic85/gladius/raw/main/misc/logo/logo-1.png" alt="" style="display: block; margin: auto; width: 128px; height: 128px;" />

**Gladius** aka "gladius" is a library facilitating web application development exclusively in pure **Python**, eliminating the need for HTML, CSS, or JavaScript/TypeScript.

Built for developers who want to leverage Python across the entire stack, Gladius provides access to modern web framework features while mirroring patterns familiar to full-stack Python developers.

For traditional frontend developers, Gladius offers a comfortable transition by exposing all standard Web APIs available in browsers. This ensures compatibility with modern browsers and existing NPM packages (from npmjs), allowing seamless integration of JavaScript (and TypeScript) libraries when needed.

By unifying frontend and backend development under Python, Gladius delivers a cohesive, intuitive experience, ideal for developers seeking a Python, centric approach without sacrificing access to the broader web ecosystem.


## Install
```bash
pip install gladius[all]
```

## Hello World

Create `app.py` file with content:

```python
from gladius import create_app, run_app


# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
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
    npm_packages=npm_packages, # type: ignore
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
```

Run python app with simple server in background:

```bash
python -B app.py
```

Or, in case you want to rebuild on code change:

```bash
python -B -u -m gunicorn --reload --bind '0.0.0.0:5000' --timeout 300 --workers 1 --worker-class aiohttp.GunicornWebWorker 'app:app'
```
