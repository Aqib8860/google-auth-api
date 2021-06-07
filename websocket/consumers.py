from starlette.websockets import WebSocket

from server.websocket import BaseWebsocket
from server import settings


class FollowersFollowingCountWebsocket(BaseWebsocket):
    async def connect(self):
        self.group_name = "followers"
        settings.groups.group_add(self.group_name, self)

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        settings.groups.group_discard(self.group_name, self)
        await self.ws.close()

