from gladius import create_app, run_app, h

import client.App # type: ignore
import client.style # type: ignore


page, app = create_app(
    npm={
        '@picocss/pico': [],
        'lodash': [],
    },
    ready=[
        client.App,
        client.style,
    ],
)

with page['head']:
    h.meta({'name': 'color-scheme', 'content': 'light dark'})

if __name__ == '__main__':
    run_app(app)
