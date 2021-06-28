from starlette.routing import Route, WebSocketRoute
from websocket.consumers import FollowersFollowingCountWebsocket

routes = [
    WebSocketRoute("/ws/followers", FollowersFollowingCountWebsocket),
]
