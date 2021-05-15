from starlette.responses import JSONResponse

from abc import ABC

async def hello(request):
    raise Exception("Custom Exception")
    return JSONResponse({"message":"Hello World","status":True})



