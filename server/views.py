from starlette.responses import JSONResponse
from server import settings

from utils import db



async def hello(request):
    # raise Exception("Custom Exception")
    with db.Connect() as client:
        profiles = client.auth.profile.delete_many({})
        print(profiles)


    # await settings.groups.group_send("followers", data={"async message received": "Noice work aditya", "type": "websocket.accept"})
    return JSONResponse({"message": "Hello World", "status": True})
