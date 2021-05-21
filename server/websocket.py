import json
import typing

from starlette.endpoints import WebSocketEndpoint
from starlette.types import Scope, Receive, Send
from starlette.websockets import WebSocket, WebSocketState


class Groups:
    def __init__(self):
        self.groups = {}

    def group_add(self, group_name: str, websocket_endpoint: WebSocketEndpoint):
        if group := self.groups.get(group_name):
            group.append(websocket_endpoint)
        else:
            self.groups.update({group_name: [websocket_endpoint, ]})

    def group_discard(self, group_name: str, websocket_endpoint: WebSocketEndpoint):
        if group_name in self.groups:
            self.groups["group_name"].remove(websocket_endpoint)

    async def group_send(self, group_name: str, data: dict):
        if group := self.groups.get(group_name):
            for i in group:
                await i.broadcast(data=data)


class BaseWebsocket(WebSocketEndpoint):

    def __init__(self, scope: Scope, receive: Receive, send: Send):
        super().__init__(scope, receive, send)
        self.group_name = "default_group"
        self.ws = WebSocket(scope, receive, send)

    async def on_connect(self, websocket: WebSocket) -> None:
        """Override to handle an incoming websocket connection"""
        self.ws = websocket
        self.ws.application_state = WebSocketState.CONNECTING
        await self.connect()

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        await self.disconnect()
        if await self.is_connected():
            await self.ws.close()

    async def connect(self):
        await self.ws.accept()

    async def disconnect(self):
        pass

    async def receive_json(self, data):
        raise NotImplemented

    async def send_json(self, data):
        await self.ws.send(message={
            "type": "websocket.send",
            "text": json.dumps(data)
        })

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        try:
            if isinstance(data, (str, )):
                await self.receive_json(json.loads(data))
        except Exception as e:
            await self.ws.close(500)

    async def is_connected(self):
        return self.ws.application_state == WebSocketState.CONNECTED

    async def broadcast(self, data: dict):
        if await self.is_connected():
            await self.ws.send(message={
                "type": "websocket.send",
                "text": json.dumps(data)
            })
            return True
        else:
            return False
