from gladius import h, render
from rich import print


def App(props):
    return h(Todo, None)


def Todo(props):
    with h('div', {'class': 'flex flex-col w-full h-screen justify-center items-center'}) as el:
        with h('div', None):
            h(TodoHeader, None)
            h(TodoList, None)

    return el


def TodoHeader(props):
    with h('div', {'class': 'flex'}) as el:
        h('input', {'type': 'text', 'class': 'input', 'placeholder': 'Title...'})

        with h('button', {'class': 'btn btn-primary'}):
            h('i', {'data-feather': 'plus'})

    return el


def TodoList(props):
    with h('ul', {'class': 'w-full list bg-base-100 rounded-box shadow-md'}) as el:
        h(TodoItem, {'i': 0})
        h(TodoItem, {'i': 1})
        h(TodoItem, {'i': 2})
        h(TodoItem, {'i': 3})

    return el


def TodoItem(props):
    with h('li', {'class': 'flex list-row items-center justify-between', 'key': f'todo-item-{props["i"]}'}) as el:
        with h('div', {'class': 'flex-1'}):
            h.text('Dio Lupa')

        with h('button', {'class': 'btn btn-square btn-ghost'}):
            h('i', {'data-feather': 'trash'})

    return el


app = App({})
print(app)

html = render(app)
print(html)
