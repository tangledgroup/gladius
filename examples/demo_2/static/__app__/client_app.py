from pyscript import document, window # type: ignore
from pyscript.js_modules.alpinejs import Alpine # type: ignore
from pyscript.js_modules.pinecone_router import default as PineconeRouter # type: ignore


window.Alpine = Alpine


def alpine_init(event):
    print('alpine:init', event)


document.addEventListener('alpine:init', alpine_init)
Alpine.plugin(PineconeRouter)
Alpine.start()

document.body.append('Hello from PyScript')
