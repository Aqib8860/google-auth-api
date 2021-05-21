from bson.json_util import dumps, loads
from json import loads
import functools
from starlette.responses import JSONResponse


async def convert_to_json(obj) -> dict:
    data = loads(dumps(obj))
    if data.get("_id"):
        data['id'] = data["_id"]["$oid"]
        del data['_id']

    return dict(data)

def check_request_data(fields: list, req_type="json"):
    """Method Decorator to check available fields in a Request

    Args:
        fields (list): List of data needed for the request
        req_type (str, optional): Type of data needed Available Values are "data", "query", "json". Defaults to "json".
    """
    def outer(endpoint, *args, **kwargs):
        @functools.wraps(endpoint)
        async def inner(self, request, **kwargs):
            if req_type == "data":
                body = await request.form()
            elif req_type == "json":
                body = await request.json()
            elif req_type == "query":
                body = request.query_params
            else:
                return JSONResponse(content={
                        "message": f"Server Error",
                        "status": False
                    }, status_code=505)

            for i in fields:
                if i not in body:
                    return JSONResponse(content={
                        "message": f"Field {i} is missing",
                        "status": False
                    }, status_code=400)

            return await endpoint(self, request, **kwargs)

        
        return inner
    return outer