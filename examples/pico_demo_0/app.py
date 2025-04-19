from gladius import create_app, run_app, h

import client.app
import client.App # type: ignore


page, app = create_app(
    npm={
        # 'spellcaster': ['dist/index.js'],
        '@picocss/pico': ['css/pico.css', 'css/pico.colors.css'],
        'lodash': ['index.js'],
        # 'alpinejs': [],
        'sinuous': ['src/index.js', 'src/observable.js'],
    },
    ready=[
        client.app,
        client.App,
    ],
)

with page['head']:
    h.meta({'name': 'color-scheme', 'content': 'light dark'})

# with page['body']:
#     with h.div({'class': 'container'}):
#         h.h1({}, 'Hello there')
#         h.button({}, 'Click me')

if __name__ == '__main__':
    run_app(app)
