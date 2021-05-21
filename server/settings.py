from pathlib import Path
from .local_settings import *

from starlette.applications import Starlette
from starlette.middleware import Middleware

from starlette.middleware.errors import ServerErrorMiddleware
from starlette.responses import HTMLResponse

from server.urls import routes
from .websocket import Groups
import traceback


BASE_DIR = Path(__file__).resolve().parent.parent

MIDDLEWARE = [
    Middleware(ServerErrorMiddleware, debug=SERVER.DEBUG),
]

app = Starlette(routes=routes, debug=SERVER.DEBUG, middleware=MIDDLEWARE,)

groups = Groups()



