from gladius import create_app, run_app, h

# import client.app
import client.App # type: ignore
import client.style # type: ignore


page, app = create_app(
    npm={
        '@picocss/pico': [],
        'lodash': ['index.js'], # 'index.js' is required if used in python
    },
    ready=[
        # client.app,
        client.App,
        client.style,
    ],
)

with page['head']:
    h.meta({'name': 'color-scheme', 'content': 'light dark'})

if __name__ == '__main__':
    run_app(app)
