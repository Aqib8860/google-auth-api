from starlette.routing import Route, Mount
from .views import hello

from apis.urls import routes as api_routes
from websocket.routes import routes as ws_routes

routes = [
    Route('/hello', hello),
    Mount('/api', routes=api_routes),
    # Mount('/ws', routes=ws_routes)
] + ws_routes
