from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from .views import hello

from apis.urls import routes as api_routes
from websocket.routes import routes as ws_routes

routes = [
    Route('/', hello),
    # Mount('/', app=StaticFiles(directory="static"), name='static'),
    Mount('/api', routes=api_routes),
    # Mount('/ws', routes=ws_routes)
] + ws_routes
