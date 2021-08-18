from sys import path
import perspective
import tornado
import logging
from threading import Thread
from schemas import *
from table_setup import MANAGER


class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def get(self):
        self.render("index.html")

app = tornado.web.Application(
    [
        # create a websocket endpoint that the client Javascript can access
        (
            r"/websocket",
            perspective.PerspectiveTornadoHandler,
            {"manager": MANAGER, "check_origin": True},
        ),
        (r"/", MainHandler),
        (r"/(.*)",tornado.web.StaticFileHandler,{"path":'./',"default_filename": "index.css"})
    ]
)

app.listen(8888)
logging.critical("Listening on http://localhost:8888")
loop = tornado.ioloop.IOLoop.current()