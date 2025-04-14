from gladius import create_app, run_app

# import client.app # type: ignore
import client.App # type: ignore
import client.style # type: ignore

npm_packages = {
    'tailwindcss': [],
    'daisyui': [],
}

g, page, app = create_app(
    npm_packages=npm_packages,
    ready=[
        client.App,
        client.style,
    ],
)

if __name__ == '__main__':
    run_app(app)
