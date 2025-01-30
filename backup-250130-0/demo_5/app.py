from aiohttp import web
from gladius.starter import create_aiohttp_app

# Tailwind Lite configuration
npm_packages = {
    # 'tailwind-lite': ['index.css'],
    'nprogress': ['nprogress.js', 'nprogress.css']
}

# Client-side form handling
def ready():
    from pyscript import when
    from pyscript.web import page
    from pyscript.js_modules.nprogress import default as NProgress

    form = page['#signin-form'][0]
    email_input = page['#email'][0]
    password_input = page['#password'][0]
    error_div = page['#error-message'][0]
    success_div = page['#success-message'][0]

    @when('submit', form)
    async def on_submit(event):
        event.preventDefault()
        NProgress.start()

        error_div.innerText = ''
        success_div.innerText = ''

        # Client-side validation
        if not email_input.value or '@' not in email_input.value:
            error_div.innerText = 'Please enter a valid email address'
            email_input.classList.add('border-red-500')
            NProgress.done()
            return

        if len(password_input.value) < 6:
            error_div.innerText = 'Password must be at least 6 characters'
            password_input.classList.add('border-red-500')
            NProgress.done()
            return

        try:
            response = await fetch('/login', {
                'method': 'POST',
                'headers': {'Content-Type': 'application/json'},
                'body': JSON.stringify({
                    'email': email_input.value,
                    'password': password_input.value
                })
            })

            result = await response.json()
            if result.success:
                success_div.innerText = f'Welcome {result.email}!'
                form.reset()
                success_div.classList.remove('hidden')
            else:
                error_div.innerText = result.message
                error_div.classList.remove('hidden')

        except Exception as e:
            error_div.innerText = 'Login failed. Please try again later.'

        NProgress.done()

# Create aiohttp app
g, page, app = create_aiohttp_app(
    links=['https://cdn.tailwind-lite.com/1.0.2.css'],
    npm_packages=npm_packages,
    ready=ready,
)

# Server routes
async def handle_login(request):
    data = await request.json()
    if data['email'] == 'user@example.com' and data['password'] == 'password123':
        return web.json_response({'success': True, 'email': data['email']})
    return web.json_response({'success': False, 'message': 'Invalid credentials'}, status=401)

app.router.add_post('/login', handle_login)

# Tailwind-styled form structure
with page:
    with g.body(class_="bg-gray-100 min-h-screen"):
        with g.main(class_="max-w-md mx-auto mt-20 bg-white rounded-lg shadow-md p-8"):
            g.h1('Sign In to Your Account', class_="text-2xl font-bold text-gray-800 mb-6 text-center")

            with g.form(id='signin-form', class_="space-y-6"):
                g.div(id='error-message', class_="hidden p-3 bg-red-100 text-red-700 rounded-lg")
                g.div(id='success-message', class_="hidden p-3 bg-green-100 text-green-700 rounded-lg")

                with g.div(class_="space-y-4"):
                    with g.div():
                        g.label('Email Address', class_="block text-sm font-medium text-gray-700 mb-1")
                        g.input(type='email', id='email', name='email',
                               class_="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                               placeholder='you@example.com')

                    with g.div():
                        g.label('Password', class_="block text-sm font-medium text-gray-700 mb-1")
                        g.input(type='password', id='password', name='password',
                               class_="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                               placeholder='••••••••')

                g.button('Sign In',
                        type='submit',
                        class_="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200")

            g.p('Don\'t have an account? ',
               class_="text-center mt-6 text-gray-600",
               children=[
                   g.a('Sign up', href='#', class_="text-blue-600 hover:underline")
               ])

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5000)
