from gladius import document, define, h, signal, effect, render


count, set_count = signal(0)


def ClickedButton(props):
    def fn():
        print(f'Clicked {count()} time(s)')

        def fn2():
            print('cleanup from ClickedButton when current ClickedButton instance is released and unused anymore')

        return fn2

    effect(fn)

    def button_onclick(e):
        set_count(count() + 1)

    with h.div() as el:
        with h.button({'class': 'primary', 'onlick': button_onclick}):
            h.text('Click me' if count() == 0 else 'Clicked {count()} time(s)')

        h.br()

    return el


def App(props):
    def fn():
        print('cleanup from App called when current App instance is released and unused anymore')

    effect(fn)

    with h.div({'class': 'container'}) as el:
        h.h1('Hello there')
        ClickedButton({})
        ClickedButton({})
        ClickedButton({})
        ClickedButton({})
        ClickedButton({})

    return el


def fn():
    render(App({}), document.body)

    def fn2():
        print('cleanup from top-level when document.body instance is released and unused anymore')

    return f2

effect(fn)
