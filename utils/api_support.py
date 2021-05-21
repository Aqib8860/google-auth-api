from bson.json_util import dumps, loads

from json import loads

import functools

async def convert_to_json(obj) -> dict:
    data = loads(dumps(obj))
    if data.get("_id"):
        data['id'] = data["_id"]["$oid"]
        del data['_id']

    return dict(data)

def check_request_data(endpoint, *args, **kwargs):
    @functools.wraps(endpoint)
    async def inner(self, request, **kwargs):
        return endpoint(self, request)

    
    return inner