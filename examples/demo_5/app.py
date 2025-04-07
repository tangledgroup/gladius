from gladius import create_app, run_app, capture_imports

with capture_imports() as module_map:
    import client_app


# required npm packages
npm_packages = {
    '@picocss/pico': ['css/pico.css'],
    'alpinejs': ['dist/module.esm.js'],
    'pinecone-router': ['dist/router.esm.js'],
    'nprogress': ['nprogress.js', 'nprogress.css'],
}

# create simple aiohttp web server
g, page, app = create_app(
    npm_packages=npm_packages, # type: ignore
    module_map=module_map,
    ready=client_app,
)

# server-side structure
with page:
    message_content = '''
        <p x-text="m"></p>
    '''

    messages_content = f'''
        <template x-for="m in $store.messages.items">
            {message_content}
        </template>
    '''

    main_content = f'''
        <main class="container">
            <h1>Gladius Demo - Messages</h1>
            <div class="form">
                <fieldset role="group">
                    <input name="message" type="text" placeholder="Enter your message" autocomplete="off" id="message" x-on:keydown="send">
                    <input type="submit" value="Send" x-on:click="send">
                </fieldset>
            </div>

            {messages_content}
        </main>
    '''

    body_content = f'''
        <body x-data>
            {main_content}
        </body>
    '''

    g.text(body_content)


# start application
if __name__ == '__main__':
    run_app(app, host='0.0.0.0', port=5000)
