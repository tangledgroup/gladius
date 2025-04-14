from gladius import h, render
from rich import print


def App():
    return Todo()


def Todo():
    with h.div({'class': 'flex flex-col w-full h-screen justify-center items-center'}) as el:
        with h.div():
            TodoHeader()
            TodoList()

    return el


def TodoHeader():
    with h.div({'class': 'flex'}) as el:
        h.input({'type': 'text', 'class': 'input', 'placeholder': 'Title...'})

        with h.button({'class': 'btn btn-primary'}):
            h.i({'data-feather': 'plus'})

    return el


def TodoList():
    with h.ul({'class': 'w-full list bg-base-100 rounded-box shadow-md'}) as el:
        TodoItem({'i': 0})
        TodoItem({'i': 1})
        TodoItem({'i': 2})
        TodoItem({'i': 3})

    return el


def TodoItem(props):
    with h.li({'class': 'flex list-row items-center justify-between', 'key': f'todo-item-{props["i"]}'}) as el:
        h.div({'class': 'flex-1'}, 'Dio Lupa'))

        with h.button({'class': 'btn btn-square btn-ghost'}):
            h.i({'data-feather': 'trash'})

    return el


with App() as app:
    print(app)


html = render(app)
print(html)
