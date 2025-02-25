# to learn more about Alpine visit https://alpinejs.dev/
from typing import TypedDict

from pyscript import document, window # type: ignore
from pyscript.web import page # type: ignore
from pyscript.ffi import to_js # type: ignore
from pyscript.js_modules.nprogress import default as NProgress # type: ignore
from pyscript.js_modules.alpinejs import Alpine # type: ignore
from pyscript.js_modules.pinecone_router import default as PineconeRouter # type: ignore

window.Alpine = Alpine


def export(func):
    setattr(window, func.__name__, func)

    def wraps(*args, **kwargs):
        return func(*args, **kwargs)

    return wraps


class Note(TypedDict):
    title: str
    content: str
    tags: list[str]


#
# note
#
@export
def add_note_cb(event):
    if not (event.type == 'click' or (event.type == 'keydown' and event.key == 'Enter')):
        return

    if event and event.preventDefault:
        event.preventDefault()

    add = Alpine.store('notes').add
    title_input = page['input#title'][0]
    title: str = title_input.value
    content: str = ''
    tags: list[str] = []
    note: Note = {'title': title, 'content': content, 'tags': tags}
    add(note)
    title_input.value = ''
    title_input.focus()


@export
def remove_note_cb(event):
    if not event.type == 'click':
        return

    if event and event.preventDefault:
        event.preventDefault()

    remove = Alpine.store('notes').remove
    remove_button = event.target
    i = int(remove_button.getAttribute('i'))
    remove(i)


@export
def view_note_cb(event):
    if not event.type == 'click':
        return

    if event and event.preventDefault:
        event.preventDefault()

    items = Alpine.store('notes').items
    view_button = event.target
    i = int(view_button.getAttribute('i'))
    note = items[i]
    set_note = Alpine.store('note').set
    set_note(note.title, note.content, note.tags)
    path = f'/notes/{i}'
    window.PineconeRouter.context.redirect(path)


@export
def update_note_cb(event):
    if not event.type == 'click':
        return

    if event and event.preventDefault:
        event.preventDefault()

    title_input = page['input#title'][0]
    content_textarea = page['textarea#content'][0]

    tags: 'Array' = window.Array['from'](document.querySelectorAll('input[type=checkbox]:checked'))
    tags: 'Array' = tags.map(lambda n, *_: n.name)

    items = Alpine.store('notes').items
    update = Alpine.store('notes').update
    update_button = event.target
    i = int(update_button.getAttribute('i'))

    note: 'Object' = items[i]
    note: 'Object' = window.Object.assign({}, note)
    note['title'] = title_input.value
    note['content'] = content_textarea.value
    note['tags'] = tags
    # print(f'{i=} {note=}, {window.JSON.stringify(note)}')
    update(i, note)
    path = '/notes'
    window.PineconeRouter.context.redirect(path)


@export
def note_tag_checkbox_cb(event):
    if not event.type == 'click':
        return

    window.console.log(event.target.name)
    window.console.log(event.target.checked)
    note = Alpine.store('note')
    tags = note.tags

    if event.target.checked:
        tags.push(event.target.name)
    else:
        if tags.includes(event.target.name):
            i = tags.indexOf(event.target.name)
            tags.splice(i, 1)

    set_note = Alpine.store('note').set
    set_note(note.title, note.content, note.tags)


#
# tag
#
@export
def add_tag_cb(event):
    if not (event.type == 'click' or (event.type == 'keydown' and event.key == 'Enter')):
        return

    if event and event.preventDefault:
        event.preventDefault()

    add = Alpine.store('tags').add
    tag_input = page['input#tag'][0]
    add(tag_input.value)
    tag_input.value = ''
    tag_input.focus()


@export
def remove_tag_cb(event):
    if not event.type == 'click':
        return

    if event and event.preventDefault:
        event.preventDefault()

    remove = Alpine.store('tags').remove
    tag_button = event.target
    i = int(tag_button.getAttribute('i'))
    remove(i)


def alpine_init(event):
    print('alpine:init', event)

    #
    # notes
    #
    def add_note(note: Note):
        items: 'Array' = Alpine.store('notes').items
        items.push(to_js(note))

    def remove_note(index: int):
        items: 'Array' = Alpine.store('notes').items
        items.splice(index, 1)

    def update_note(index: int, note: Note):
        items: 'Array' = Alpine.store('notes').items
        items[index] = to_js(note)

    Alpine.store('notes', to_js({
      'items': to_js([]),
      'add': add_note,
      'remove': remove_note,
      'update': update_note,
    }))

    #
    # note
    #
    def set_note(title, content, tags):
        note = Alpine.store('note')
        note.title = title
        note.content = content
        note.tags = tags

    Alpine.store('note', to_js({
      'title': '',
      'content': '',
      'tags': [],
      'set': set_note,
    }))

    #
    # tags
    #
    def add_tag(tag: str):
        items: 'Array' = Alpine.store('tags').items
        items.push(tag)

    def remove_tag(index: int):
        items: 'Array' = Alpine.store('tags').items
        items.splice(index, 1)

    Alpine.store('tags', to_js({
      'items': to_js([]),
      'add': add_tag,
      'remove': remove_tag,
    }))

    window.PineconeRouter.settings.templateTargetId = 'app'
    window.PineconeRouter.add('/notes', to_js({'templates': to_js(['/api/1.0/templates/notes'])}))
    window.PineconeRouter.add('/notes/:index', to_js({'templates': to_js(['/api/1.0/templates/note'])}))
    window.PineconeRouter.add('/tags', to_js({'templates': to_js(['/api/1.0/templates/tags'])}))

    document.addEventListener('pinecone-start', NProgress.start)
    document.addEventListener('pinecone-end', NProgress.done)
    # document.addEventListener('fetch-error', print)


document.addEventListener('alpine:init', alpine_init)
Alpine.plugin(PineconeRouter)
Alpine.start()
