from gladius import create_app, run_app, h

import client.app


page, app = create_app(
    npm={
        '@picocss/pico': ['css/pico.css', 'css/pico.colors.css'],
        'lodash': ['index.js'],
    },
    ready=[
        client.app,
    ],
)

with page['head']:
    h.meta({'name': 'color-scheme', 'content': 'light dark'})

if __name__ == '__main__':
    run_app(app)
