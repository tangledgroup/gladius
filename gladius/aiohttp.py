__all__ = [
    # 'element_middleware',
    'html_middleware',
    'json_middleware',
    'aiohttp_middlewares',
    'run_app',
]

import os
import sys
# import subprocess

from aiohttp import web
from aiohttp.web import middleware

# from .element import Element


# @middleware
# async def element_middleware(request, handler):
#     resp = await handler(request)
#
#     if isinstance(resp, Element):
#         text: str = resp.render()
#         headers = {'content-type': 'text/html'}
#         resp = web.Response(status=200, text=text, headers=headers)
#
#     return resp


@middleware
async def html_middleware(request, handler):
    resp = await handler(request)

    if isinstance(resp, str):
        headers = {'content-type': 'text/html'}
        resp = web.Response(status=200, text=resp, headers=headers)

    return resp


@middleware
async def json_middleware(request, handler):
    resp = await handler(request)

    if isinstance(resp, (list, dict)):
        resp = web.json_response(resp)

    return resp


aiohttp_middlewares = [
    # element_middleware,
    html_middleware,
    json_middleware,
]


def run_app(app, host='0.0.0.0', port=5000, workers=1, timeout=300, reload=True):
    if reload:
        cmd = [
            sys.executable,
            '-B',
            '-u',
            '-m',
            'gunicorn',
            '--reload',
            '--reload-engine', 'inotify', # NOTE: probably linux only
            '--bind', f'{host}:{port}',
            '--timeout', f'{timeout}',
            '--workers', f'{workers}',
            '--worker-class', 'aiohttp.GunicornWebWorker',
            'app:app'
        ]

        # subprocess.run(cmd, check=True)
        os.execvp(sys.executable, cmd)
    else:
        web.run_app(app, host='0.0.0.0', port=5000)
