from gladius import create_app, run_app

import client.App # type: ignore
import client.style # type: ignore


g, page, app = create_app(
    npm_packages=[
        'tailwindcss',
        'daisyui',
    ],
    ready=[
        client.App,
        client.style,
    ],
)

if __name__ == '__main__':
    run_app(app)
