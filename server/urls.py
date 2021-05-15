from starlette.routing import Route, Mount
from .views import hello

from apis.urls import routes as api_routes


routes=[
    Route('/hello', hello),
    Mount('/api', routes=api_routes)
]