from pyscript import when
from pyscript.web import page
from pyscript.js_modules.nprogress import default as NProgress

from client_utils import f0

btn = page['#hello-button'][0]  # get server-created button
clicked = 0                     # track clicks

@when('click', btn)
def on_click(event):
    global clicked
    NProgress.start()
    clicked += 1
    print(f0(clicked, clicked))
    btn.innerText = f'Clicked {clicked} time{"s" if clicked !=1 else ""}!'
    NProgress.done()
