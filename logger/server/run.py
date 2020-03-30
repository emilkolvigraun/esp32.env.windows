from handlers import Handlers
from server import WebServer


handler = Handlers()
server = WebServer(handler.routes)
server.run()