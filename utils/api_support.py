from bson.json_util import dumps
from json import loads
import json
import functools
from starlette.responses import JSONResponse
import traceback
import datetime
import random
from server.local_settings import FCM

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
                raise e
                return JSONResponse(content={
                            "message": f"Bad request for {str(e)}",
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
        self.filename = filename
        with open(filename, "r") as fp:
            self.ids: dict = json.load(fp)

    def get(self, _k: str):
        return self.ids[_k] 

    def inc(self, _k):
        if self.ids.get(_k):
            self.ids.update({_k: self.ids.get(_k) + 1})
        else:
            raise KeyError

    def save(self):
        with open(self.filename, 'w') as fp:
            json.dump(self.ids, fp)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        traceback.extract_tb(exc_tb)
        self.save()

async def generate_user_id():
    ts = datetime.datetime.utcnow().timestamp()
    with LastIds() as lids:
        end = lids.get("profile")
        lids.inc("profile")
    user_id = "{}{:08d}{:010d}".format("ID", int((ts * 10**8) // random.randint(1000, 10**8)) % 10**8, end)
    return user_id

from pyfcm import FCMNotification

push_service = FCMNotification(api_key=FCM.API_KEY)
