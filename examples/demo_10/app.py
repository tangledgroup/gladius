from gladius import create_app, run_app

import client.App # type: ignore
import client.style # type: ignore


g, page, app = create_app(
    npm_packages=[
      'tailwindcss',
      'daisyui',
      'feather-icons',
      '@types/feather-icons',
    ],
    ready=[
        client.App,
        client.style,
    ],
)

'''
with g.div(class_='w-full') as el:
    g.h1('asada')
    g.p('asdasda')

def h(type, props, *children):
  return {'type': type, 'props': props, 'children': children}

h('div', {'class': 'w-full'},
    h('h1', None, 'asada'),
    h('p', None, 'asdasda')
)

from gladius import h, create_app, run_app

g, app = create_app(
    npm_packages=[
      'tailwindcss',
      'daisyui',
      'feather-icons',
      '@types/feather-icons',
    ],
    ready=[
        client.App,
        client.style,
    ],
)

g.head
    .append_child(
        h('script', {'src': "https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js"})
    )
    .append_child(
        h('script', {'src': "https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js"})
    )

with g['head']:
    g.script(src="https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js")
    g.script(src="https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js")
'''

if __name__ == '__main__':
    run_app(app)
