from gladius import h, render, define
from rich import print


@define
def App():
    return h.Todo()


@define
def Todo():
    with h.div({'class': 'flex flex-col w-full h-screen justify-center items-center'}) as el:
        with h.div():
            h.TodoHeader()
            h.TodoList()

    return el


@define
def TodoHeader():
    with h.div({'class': 'flex'}) as el:
        h.input({'type': 'text', 'class': 'input', 'placeholder': 'Title...'})

        with h.button({'class': 'btn btn-primary'}):
            h.i({'data-feather': 'plus'})

    return el


@define
def TodoList():
    with h.ul({'class': 'w-full list bg-base-100 rounded-box shadow-md'}) as el:
        h.TodoItem({'i': 0})
        h.TodoItem({'i': 1})
        h.TodoItem({'i': 2})
        h.TodoItem({'i': 3})

    return el


@define
def TodoItem(props):
    with h.li({'class': 'flex list-row items-center justify-between', 'key': f'todo-item-{props["i"]}'}) as el:
        h.div({'class': 'flex-1'}, 'Dio Lupa')

        with h.button({'class': 'btn btn-square btn-ghost'}):
            h.i({'data-feather': 'trash'})

    return el


# with h.App() as app:
#     print(app)
app = h.App()
print(f'{callable(app)=}')
from contextlib import AbstractContextManager, contextmanager
print(f'{isinstance(app, AbstractContextManager)=}')
print(app)

html = render(app)
print(html)
