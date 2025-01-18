import js
import json
from pyscript import window, WebSocket
from pyscript.ffi import to_js
from pyscript.js_modules.alpinejs import Alpine


def load_messages():
    def onopen(event):
        window.console.log('onopen: WebSocket connection established.')
        window.NProgress.start()
        ws.send(json.dumps({}))

    def onclose(event):
        window.console.log('onclose: WebSocket connection closed.')
        window.NProgress.done()

    def onmessage(event):
        window.console.log('onmessage:', event)
        data = json.loads(event.data)
        add_message(data)

    def onerror(error):
        window.console.error('on_error: WebSocket error:', error)
        window.NProgress.done()

    ws = WebSocket(url=f'ws://{window.location.host}/api/live-data-stream')
    ws.onopen = onopen
    ws.onclose = onclose
    ws.onmessage = onmessage
    ws.onerror = onerror

def add_message(message: dict):
    js_message = to_js(message)
    Alpine.store('messages').items.push(js_message)

Alpine.store('messages', to_js({
    'items': js.Array.new(),
    'load': load_messages,
    'add': add_message,
}))
