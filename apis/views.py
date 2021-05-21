from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from .social_login import GoogleSocialAuthDataClass
from utils.db import Connect
from utils.api_support import convert_to_json, check_request_data
from utils.security import jwt_authentication

from bson import ObjectId

from asyncstdlib.builtins import map as amap
from asyncstdlib.builtins import tuple as atuple

# Authentication endpoints
class GoogleAuthEndpoint(HTTPEndpoint):
    async def get(self, request):
        return JSONResponse(content={
            "message": "Not a Get Endpoint",
            "status": False
        })

    @check_request_data(fields=["auth_token", ])
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


####################################✅❌
# Profile Endpoints ################
####################################
# Available Endpints are: ##########
#### - Get Public Profile ########## ❌
#### - Get Profile Media ########### ❌
####################################

class Profile(HTTPEndpoint):

    @jwt_authentication
    async def get(self, request):
        # import pdb; pdb.set_trace()
        with Connect() as client:
            user_object = client.auth.profile.find_one({"_id": ObjectId(request.user_id)}, {"password": False})

        obj = await convert_to_json(user_object)
        
        return JSONResponse(content=obj, status_code=200)



#######################################
# Follow APIs #########################
#######################################
# Available Endpints: #################
#### - Following ###################### ✅
######### - Get (Get Users Following) #
#### - Get Followers ################## ✅


# Follow APIs
class Following(HTTPEndpoint):

    DATA_STORED = {
        "_id": True,
        "channel_name": True,
        "name": True,
        "email": True,
        "profile_picture": True
    }

    @jwt_authentication
    async def get(self, request):
        with Connect() as client:
            following = client.auth.profile.find_one({"_id": ObjectId(request.user_id)}, {"following": True})

        if not following:
            return JSONResponse(content={
                "message": "User Doesnot Exists",
                "status": False,
            }, status_code=404)

        return JSONResponse(content={
            "message": "Following List",
            "status": True,
            "data":  await atuple(amap(convert_to_json, following["following"]))
        }, status_code=200)

    @jwt_authentication
    @check_request_data(fields=["id",])
    async def post(self, request):
        request_body = await request.json()
        to_id = request_body.get("id")

        with Connect() as client:
            to_user = client.auth.profile.find_one({"_id": ObjectId(to_id)}, self.DATA_STORED)

            from_user = client.auth.profile.find_one({"_id": ObjectId(request.user_id)}, self.DATA_STORED)


            if not client.auth.profile.find_one({"_id": ObjectId(request.user_id),"following": {"$elemMatch": {"_id": ObjectId(to_id)}}}):
                client.auth.profile.update({"_id": ObjectId(request.user_id)}, {
                    "$push": {
                        "following": to_user,
                    },
                    "$inc": {
                        "following_count": 1
                    }
                }, upsert=False, multi=True)

            if not client.auth.profile.find_one({"_id": ObjectId(to_id),"follower": {"$elemMatch": {"_id": ObjectId(request.user_id)}}}):
                client.auth.profile.update({"_id": ObjectId(to_id)}, {
                    "$push": {
                        "follower": from_user,
                    },
                    "$inc": {
                        "follower_count": 1
                    }
                }, upsert=False, multi=True)

            return JSONResponse(content={
                "message": "User Followed",
                "status": True,
                "data": await convert_to_json(to_user)
            }, status_code=200)

        return JSONResponse(content={
            "message": "Database Error",
            "status": False
        }, status_code=501)

    @jwt_authentication
    @check_request_data(fields=["id",])
    async def delete(self, request):
        from_id = request.user_id
        to_id = (await request.json()).get("id")

        with Connect() as client:
            client.auth.profile.update({"_id": ObjectId(to_id)}, {
                "$pull": {
                    "follower": {
                        "_id": ObjectId(from_id)
                    }
                },
                "$inc": {
                    "follower_count": -1
                }
            }, upsert=False, multi=True, )

            client.auth.profile.update({"_id": ObjectId(from_id)}, {
                "$pull": {
                    "following": {
                        "_id": ObjectId(to_id)
                    }
                },
                "$inc": {
                    "following_count": -1
                }
            }, upsert=False, multi=True)

            return JSONResponse(content={
                "message": "Unfollowed",
                "status": True,
                "data": to_id
            }, status_code=200)
        
        return JSONResponse(content={
                "message": "Database Error",
                "status": False,
            }, status_code=501)
        
        
class Followers(HTTPEndpoint):

    @jwt_authentication
    async def get(self, request):
        with Connect() as client:
            following = client.auth.profile.find_one({"_id": ObjectId(request.user_id)}, {"following": True})

        if not following:
            return JSONResponse(content={
                "message": "User Doesnot Exists",
                "status": False,
            }, status_code=404)

        return JSONResponse(content={
            "message": "Following List",
            "status": True,
            "data": await atuple(amap(convert_to_json, following["following"]))
        }, status_code=200)

