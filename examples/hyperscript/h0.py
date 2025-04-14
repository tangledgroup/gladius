from gladius import h, render
from rich import print


def App(props):
    return h(Todo, None)


def Todo(props):
    return h('div', {'class': 'flex flex-col w-full h-screen justify-center items-center'},
        h('div', None,
            h(TodoHeader, None),
            h(TodoList, None)))


def TodoHeader(props):
    return h('div', {'class': 'flex'},
        h('input', {'type': 'text', 'class': 'input', 'placeholder': 'Title...'}),
        h('button', {'class': 'btn btn-primary'},
            h('i', {'data-feather': 'plus'})))


def TodoList(props):
    return h('ul', {'class': 'w-full list bg-base-100 rounded-box shadow-md'},
        h(TodoItem, {'i': 0}),
        h(TodoItem, {'i': 1}),
        h(TodoItem, {'i': 2}),
        h(TodoItem, {'i': 3}))


def TodoItem(props):
    return h('li', {'class': 'flex list-row items-center justify-between', 'key': f'todo-item-{props["i"]}'},
        h('div', {'class': 'flex-1'}, 'Dio Lupa'),
        h('button', {'class': 'btn btn-square btn-ghost'},
            h('i', {'data-feather': 'trash'})))


app = App({})
print(app)

html = render(app)
print(html)
