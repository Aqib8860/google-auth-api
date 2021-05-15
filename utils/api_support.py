from bson.json_util import dumps, loads

from json import loads

async def convert_to_json(obj) -> dict:
    data = loads(dumps(obj))
    if data.get("_id"):
        data['id'] = data["_id"]["$oid"]
        del data['_id']

    return dict(data)