from gladius import h, render, define
from rich import print


@define
def App():
    return h.Todo()


@define
def Todo():
    return h.div({'class': 'flex flex-col w-full h-screen justify-center items-center'},
        h.div(None,
            h.TodoHeader(),
            h.TodoList()))


@define
def TodoHeader():
    return h.div({'class': 'flex'},
        h.input({'type': 'text', 'class': 'input', 'placeholder': 'Title...'}),
        h.button({'class': 'btn btn-primary'},
            h.i({'data-feather': 'plus'})))


@define
def TodoList():
    return h.ul({'class': 'w-full list bg-base-100 rounded-box shadow-md'},
        h.TodoItem({'i': 0}),
        h.TodoItem({'i': 1}),
        h.TodoItem({'i': 2}),
        h.TodoItem({'i': 3}))


@define
def TodoItem(props):
    return h.li({'class': 'flex list-row items-center justify-between', 'key': f'todo-item-{props["i"]}'},
        h.div({'class': 'flex-1'}, 'Dio Lupa'),
        h.button({'class': 'btn btn-square btn-ghost'},
            h.i({'data-feather': 'trash'})))


app = h.App()
print(app)

html = render(app)
print(html)
