from pyscript import window, document
from pyscript.ffi import to_js
from pyscript.js_modules.pinecone_router import default as PineconeRouter
from pyscript.js_modules.alpinejs import Alpine

import stores.messages

def alpine_init(event):
    print('alpine:init', event)

document.addEventListener('alpine:init', alpine_init)

window.Alpine = Alpine
Alpine.plugin(PineconeRouter)
Alpine.start()
print('start')
