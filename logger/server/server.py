#!/usr/bin/env python3.7.4

import asyncio, base64, jinja2, os, json
from aiohttp import web
from aiohttp_jinja2 import render_template

class WebServer():


    def __init__(self, routes):
        self.loop = asyncio.new_event_loop()
        self.application = web.Application()
        self.host = '0.0.0.0'
        self.port = 8000
        self.routes = routes
    
    def run(self):
        from aiohttp_session import setup
        from aiohttp_session.cookie_storage import EncryptedCookieStorage
        from cryptography.fernet import Fernet
        from aiohttp_jinja2 import setup as jinja_setup
        import aiohttp_jinja2
    
        asyncio.set_event_loop(self.loop)

        # Setting up symmetric cookie encryption using  
        # Fernet that guarantees that a message encrypted
        # using it cannot be manipulated or read without the key
        setup(self.application, EncryptedCookieStorage(base64.urlsafe_b64decode(Fernet.generate_key())))

        self.application.add_routes(self.routes)

        # Running the webserver using the host
        # and port configurations, and the web application
        server = self.loop.create_server(self.application.make_handler(), self.host, self.port)

        print('========== Webserver running on: http://%s:%d/ ==========' % (self.host, self.port))

        # using asyncio to gather the processes as tasks and run 
        # them separately in foreground and background
        try:
            self.loop.run_until_complete(asyncio.gather(server))
            self.loop.run_forever()
        except:
            exit('Failed at startup.')

