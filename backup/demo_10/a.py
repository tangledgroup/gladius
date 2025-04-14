null = None

def h(type, props, *children):
    return {'type': type, 'props': props, 'children': children}

# app = <App />
app = h('div', {'class': 'w-full'},
    h('h1', null, 'asada'),
    h('p', null, 'asdasda')
)

print(app)
