from bson.json_util import dumps
from json import loads
import json
import functools
from starlette.responses import JSONResponse


async def convert_to_json(obj) -> dict:
    obj['id'] = str(obj.pop("_id"))
    data = loads(dumps(obj))
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
            try:
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
            except Exception as e:
                return JSONResponse(content={
                            "message": f"Bad request",
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


class LastIds():
    def __init__(self, filename="./utils/last_ids.json"):
        with open(filename, "r") as fp:
            self.ids = json.load(fp)

    def get(self, _k=None):
        pass