from gladius import create_app, run_app, h

import client.app
import client.App # type: ignore


page, app = create_app(
    npm={
        '@picocss/pico': ['css/pico.css', 'css/pico.colors.css'],
        'lodash': ['index.js'],
    },
    # ready=client.app,
    # ready=client.App,
    ready=[
        client.app,
        client.App,
    ],
)

with page['head']:
    h.meta({'name': 'color-scheme', 'content': 'light dark'})

if __name__ == '__main__':
    run_app(app)
