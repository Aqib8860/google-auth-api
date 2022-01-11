from pathlib import Path
from .local_settings import *

from starlette.applications import Starlette
from starlette.middleware import Middleware

from starlette.middleware.errors import ServerErrorMiddleware
from starlette.responses import HTMLResponse

#from server.urls import routes
from .websocket import Groups
import traceback


BASE_DIR = Path(__file__).resolve().parent.parent

MIDDLEWARE = [
    Middleware(ServerErrorMiddleware, debug=SERVER.DEBUG),
]



#app = Starlette(routes=routes, debug=SERVER.DEBUG, middleware=MIDDLEWARE,)


"""class Groups:
    def __init__(self):
        self.groups = {}

    def group_add(self, group_name, websocket_endpoint):
        if group := self.groups.get(group_name):

            group.append(websocket_endpoint)
        else:
            self.groups.update({group_name: [websocket_endpoint, ]})

    def group_discard(self, group_name, websocket_endpoint):
        if group_name in self.groups:
            self.groups[group_name].remove(websocket_endpoint)

    async def group_send(self, group_name, data):
        if group := self.groups.get(group_name):
            for i in group:
                await i.broadcast(data=data)"""
                        
groups = Groups()
