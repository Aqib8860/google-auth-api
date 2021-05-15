from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from .social_login import GoogleSocialAuthDataClass
from utils.db import Connect
from utils.api_support import convert_to_json
from utils.security import jwt_authentication

from bson import ObjectId

# Authentication endpoints
class GoogleAuthEndpoint(HTTPEndpoint):
    async def get(self, request):
        return JSONResponse(content={
            "message": "Not a Get Endpoint",
            "status": False
        })

    async def post(self, request):
        request_body = await request.json()
        auth_token = request_body.get("auth_token")
        data_class = GoogleSocialAuthDataClass(auth_token=auth_token)
        res, mes = await data_class.is_valid(raise_exception=False)

        if not res:
            return JSONResponse(content=mes, status_code=401)

        type_of_res = mes.pop('type')
        status = {
            "login": 200,
            "register": 201,
            "failed": 401
        }
        return JSONResponse(content=mes, status_code=status[type_of_res])



# Profile Endpoints

class Profile(HTTPEndpoint):

    @jwt_authentication
    async def get(self, request):
        # import pdb; pdb.set_trace()
        with Connect() as client:
            user_object = client.auth.profile.find_one({"_id": ObjectId(request.user_id)}, {"password": False})

        obj = await convert_to_json(user_object)
        
        return JSONResponse(content=obj, status_code=200)
