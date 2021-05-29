from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.schemas import SchemaGenerator

from .social_login import GoogleSocialAuthDataClass
from utils.db import Connect
from utils.api_support import convert_to_json, check_request_data
from utils.security import jwt_authentication, refresh_to_access, loose_jwt_auth

from bson import ObjectId

from asyncstdlib.builtins import map as amap
from asyncstdlib.builtins import tuple as atuple
from starlette.requests import Request
from starlette.datastructures import UploadFile, FormData
from tempfile import NamedTemporaryFile

from utils.s3 import S3
import datetime


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
        except Exception as e:
            return JSONResponse(content={
                "message": "Invalid Token - " + str(e),
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
    fields = dict.fromkeys(['id', 'email', 'name', 'bio', 'channel_name', 'profile_picture',
                  'location', 'provider', 'following', 'follower'], True)

    @jwt_authentication
    async def get(self, request):
        # import pdb; pdb.set_trace()
        with Connect() as client:
            user_object = client.auth.profile.find_one({"_id": ObjectId(request.user_id)}, self.fields)

        followers = user_object.pop('follower')
        following = user_object.pop('following')

        obj = await convert_to_json(user_object)

        obj.update({
            "follower_count": len(followers),
            "following_count": len(following)
        })
        
        return JSONResponse(content={"data": obj, "status": True, "message": "Data Extracted"}, status_code=200)


    @jwt_authentication
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

    @jwt_authentication
    async def put(self, request):
        request_data = await request.form()

        update_dict = {}

        if request_data.get("bio"):
            update_dict.update({"bio": request_data.get("bio")})
        if request_data.get("channel_name"):
            update_dict.update({"channel_name": request_data.get("channel_name")})
        
        pp = request_data.get("profile_picture")
        ts = int(datetime.datetime.utcnow().timestamp())
        if pp:
            image_file = NamedTemporaryFile(delete=True)
            await pp.seek(0)
            image_file.write(await pp.read())
            image_file.seek(0)
            s3 = S3()
            profile_picture_url = s3.upload_fileobj(f"user_files/{str(request.user_id)}/profile/picture{ts}.jpg", image_file)
            update_dict.update({"profile_picture": profile_picture_url})

        if update_dict:
            with Connect() as client:
                client.auth.profile.update_one({"_id": ObjectId(request.user_id)}, {"$set": update_dict})
        else:
            return JSONResponse(content={"status": False, "message": "Not updated"}, status_code=400)


        return JSONResponse(content={"data": update_dict, "status": True, "message": "Data Updated"}, status_code=200)

    @jwt_authentication
    async def delete(self, request):
        with Connect() as client:
            client.auth.profile.delete_one({"_id": ObjectId(request.user_id)})

        return JSONResponse(content={"message": "Deleted User", "status": True}, status_code=200)       

        

class PublicProfile(HTTPEndpoint):
    fields = dict.fromkeys(['id', 'email', 'name', 'bio', 'channel_name', 'profile_picture',
                  'location', 'provider', 'follower', 'following'], True)
    
    @loose_jwt_auth
    @check_request_data(fields=['id', ], req_type="query")
    async def get(self, request: Request):
        # import pdb; pdb.set_trace()
        with Connect() as client:
            user_object = client.auth.profile.find_one({"_id": ObjectId(request.query_params.get("id"))}, self.fields)
        

        followers = user_object.pop('follower')
        following = user_object.pop('following')

        obj = await convert_to_json(user_object)

        obj.update({
            "follower_count": len(followers),
            "following_count": len(following)
        })

        if request.is_authenticated():
            obj.update({
                "is_following": True if ObjectId(request.user_id) in followers else False
            })
                
        return JSONResponse(content={"data": obj, "message": "Data Extracted", "status": True}, status_code=200)



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
            users_following = client.auth.profile.find({"_id": {"$in": following.get('following')}}, self.DATA_STORED)

        if not following:
            return JSONResponse(content={
                "message": "User Doesnot Exists",
                "status": False,
            }, status_code=404)

        return JSONResponse(content={
            "message": "Following List",
            "status": True,
            "data":  await atuple(amap(convert_to_json, users_following))
        }, status_code=200)

    @jwt_authentication
    @check_request_data(fields=["id",])
    async def post(self, request):
        request_body = await request.json()
        to_id = request_body.get("id")

        with Connect() as client:

            if not client.auth.profile.find_one({"_id": ObjectId(request.user_id),"following": ObjectId(to_id)}):
                client.auth.profile.update({"_id": ObjectId(request.user_id)}, {
                    "$push": {
                        "following": ObjectId(to_id)
                    },

                }, upsert=False, multi=True)

            if not client.auth.profile.find_one({"_id": ObjectId(to_id),"follower": ObjectId(request.user_id)}):
                client.auth.profile.update({"_id": ObjectId(to_id)}, {
                    "$push": {
                        "follower": ObjectId(request.user_id)
                    },

                }, upsert=False, multi=True)

            return JSONResponse(content={
                "message": "User Followed",
                "status": True,
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
            client.auth.profile.find_one_and_update({"_id": ObjectId(to_id)}, {
                "$pull": {
                    "follower": ObjectId(from_id)
                }
            })

            client.auth.profile.find_one_and_update({"_id": ObjectId(from_id)}, {
                "$pull": {
                    "following": ObjectId(to_id)
                }
            })

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
            users_following = client.auth.profile.find({"_id": {"$in": following.get('following')}}, Following.DATA_STORED)

        if not following:
            return JSONResponse(content={
                "message": "User Doesnot Exists",
                "status": False,
            }, status_code=404)

        return JSONResponse(content={
            "message": "Following List",
            "status": True,
            "data": await atuple(amap(convert_to_json, users_following))
        }, status_code=200)

def schema_gen(request):
    return schemas.OpenAPIResponse(request=request)