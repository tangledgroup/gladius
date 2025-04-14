from gladius import export


print('Hello from app.py')


@export
def f0(x, y):
    return x + y
