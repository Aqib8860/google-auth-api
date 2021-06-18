from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.schemas import SchemaGenerator

from .social_login import GoogleSocialAuthDataClass
from utils.db import Connect
from utils.api_support import convert_to_json, check_request_data
from utils.security import jwt_authentication, refresh_to_access

from bson import ObjectId

from asyncstdlib.builtins import map as amap
from asyncstdlib.builtins import tuple as atuple



schemas = SchemaGenerator(
    {
        "openapi": "3.0.0", 
        "info": {
            "title": "Authentication APIs", 
            "version": "1.0"
        }
    }
)

# Authentication endpoints
class GoogleAuthEndpoint(HTTPEndpoint):
    async def get(self, request):
        return JSONResponse(content={
            "message": "Not a Get Endpoint",
            "status": False
        })

    @check_request_data(fields=["auth_token", ], )
    async def post(self, request):
        """
        responses:
            200:
                description: Successful Login Response
                examples:
                    {
                        "message": "Successfully Logged In",
                        "status": true,
                        "data": {
                            "profile": {
                                "email": "john.doe@example.com",
                                "channel_name": "johndoe",
                                "name": "John Doe",
                                "provider": "google",
                                "location": "",
                                "follower_count": 1,
                                "following_count": 0,
                                "profile_picture": "https://myworld2021.s3.amazonaws.com/user_files/60a7ced5c45cdf274b95c415/profile/picture1621610200253.jpg",
                                "id": "60a7ced5c45cdf274b95c415"
                            },
                            "token": {
                                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJyZWZyZXNoIiwiZXhwIjoxNjIxOTIzNDA0LCJpYXQiOjE2MjE2NjQyMDQsImlkIjoiNjBhN2NlZDVjNDVjZGYyNzRiOTVjNDE1IiwianRpIjoibFh4a2tJaEJWSGgwT1N5WGd4dEZhS2cvNWJKbVVnQWVQL1ZGV1UxTm0xST0ifQ.Qv8hC5TCqJDfF5oAr6aGrRV2Z-wJrkmX8xB5nCECAsY",
                                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJhY2Nlc3MiLCJleHAiOjE2MjE3NTA2MDQsImlkIjoiNjBhN2NlZDVjNDVjZGYyNzRiOTVjNDE1IiwianRpIjoibFh4a2tJaEJWSGgwT1N5WGd4dEZhS2cvNWJKbVVnQWVQL1ZGV1UxTm0xST0ifQ.7wuincHFtFCNaAOuHSTxCkxZuHs1z07PdYDesIlkbvU"
                            }
                        }
                    }
            201:
                description: Successful Registration Response
                examples:
                    {
                        "message": "Successfully Registered",
                        "status": true,
                        "data": {
                            "profile": {
                                "email": "john.doe@example.com",
                                "channel_name": "johndoe",
                                "name": "John Doe",
                                "provider": "google",
                                "location": "",
                                "follower_count": 1,
                                "following_count": 0,
                                "profile_picture": "https://myworld2021.s3.amazonaws.com/user_files/60a7ced5c45cdf274b95c415/profile/picture1621610200253.jpg",
                                "id": "60a7ced5c45cdf274b95c415"
                            },
                            "token": {
                                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJyZWZyZXNoIiwiZXhwIjoxNjIxOTIzNDA0LCJpYXQiOjE2MjE2NjQyMDQsImlkIjoiNjBhN2NlZDVjNDVjZGYyNzRiOTVjNDE1IiwianRpIjoibFh4a2tJaEJWSGgwT1N5WGd4dEZhS2cvNWJKbVVnQWVQL1ZGV1UxTm0xST0ifQ.Qv8hC5TCqJDfF5oAr6aGrRV2Z-wJrkmX8xB5nCECAsY",
                                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJhY2Nlc3MiLCJleHAiOjE2MjE3NTA2MDQsImlkIjoiNjBhN2NlZDVjNDVjZGYyNzRiOTVjNDE1IiwianRpIjoibFh4a2tJaEJWSGgwT1N5WGd4dEZhS2cvNWJKbVVnQWVQL1ZGV1UxTm0xST0ifQ.7wuincHFtFCNaAOuHSTxCkxZuHs1z07PdYDesIlkbvU"
                            }
                        }
                    }
            400:
                description: Login or Registration Failed
                examples:
                    {
                        "message": "The id_token is invalid or expired. Please login again.",
                        "status": false
                    }
        """
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

class RefreshToken(HTTPEndpoint):

    @check_request_data(fields=["refresh", ])
    async def post(self, request: Request):
        """
        responses:
            200:
                description: Refreshed Token
                examples:
                    {
                        "message": "Token Refreshed",
                        "status": true,
                        "data": {
                            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJhY2Nlc3MiLCJleHAiOjE2MjE3NTEyNjAsImlkIjoiNjBhN2NlZDVjNDVjZGYyNzRiOTVjNDE1IiwianRpIjoiY0ZGWGxPdVdHcWdCd080ckZaeitHSlduS3g3MGlIQ3B4ZkhHNjlKdHhBMD0ifQ.SFJg5FvbmFgL3d0LnCKNubu_YIY9wjyD24_ZiYd0BXM"
                        }
                    }
            400:
                description: Login or Registration Failed
                examples:
                    {
                        "message": "Error Message",
                        "status": false
                    }
        """
        refresh = (await request.json()).get("refresh")

        try:
            access = await refresh_to_access(refresh)
        except Exception:
            return JSONResponse(content={
                "message": "Invalid Token",
                "status": False
            }, status_code=400)
        
        return JSONResponse(content={
            "message": "Token Refreshed",
            "status": True,
            "data": {
                "access": access
            }
        })





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

    async def post(self, request):
        data = await request.json()
        channel_name = data.get("channel_name")

        if not channel_name:
            return JSONResponse(content={
                "message": "Key Channel Name Required",
                "status": False
            }, status_code=400)

        with Connect() as client:
            existing_user = client.auth.profile.find_one({"channel_name": channel_name}, {"channel_name": True})
            if existing_user:
                return JSONResponse(content={
                    "message": "Channel Name Exists",
                    "status": False
                }, status_code=302)

        return JSONResponse(content={
                "message": "Channel Name Accepted",
                "status": True
            }, status_code=202)

    async def put(self, request):
        user_id = request.user_id
        data = request.json()

class PublicProfile(HTTPEndpoint):

    @jwt_authentication
    @check_request_data(fields=['id', ], req_type="query")
    async def get(self, request: Request):
        # import pdb; pdb.set_trace()
        with Connect() as client:
            user_object = client.auth.profile.find_one({"_id": ObjectId(request.query_params.get("id"))}, {"password": False})

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

def schema_gen(request):
    return schemas.OpenAPIResponse(request=request)