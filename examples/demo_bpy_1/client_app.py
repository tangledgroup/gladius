# import sys; sys.path = ['static/__app__']

from browser import window, document, bind # type: ignore
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
    NProgress.done()
