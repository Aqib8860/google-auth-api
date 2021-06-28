from google.auth.transport import requests
from google.oauth2 import id_token
from dataclasses import dataclass
from PIL.Image import Image
from tempfile import NamedTemporaryFile
from server import settings
import os
import random
import io
import requests as req
from urllib.request import urlopen
import time
from .exceptions import AuthenticationError

from utils.db import Connect
from utils.security import authenticate, generate_tokens, hash_password
from utils.api_support import convert_to_json, generate_user_id
from utils.s3 import S3

from bson import ObjectId

class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    async def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
            print(idinfo)
        except:
            return {"message": "The token is either invalid or has expired"}


async def generate_username(name):

    username = "".join(name.split(' ')).lower()

    user_obj = None
    with Connect() as client:
        user_obj = client.auth.profile.find_one({'channel_name': username}, {"_id"})

    if not user_obj:
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return await generate_username(random_username)

async def generate_id():
    with Connect() as client:
        client.auth.last_ids.find_one()



async def register_social_user(user_id, email, name, picture, provider):
    required_fields = {
                '_id': True, 
                'email': True, 
                'name': True, 
                'bio': True, 
                'channel_name': True,
                'profile_picture': True,
                'location': True,
                'provider': True,
                'following': True,
                'follower': True,
                'profile_picture': True
            }

    try:
        with Connect() as client:
            filtered_user_by_email = client.auth.profile.find_one({"email": email}, {"_id": True, 'provider': True})
    except Exception as e:
        print(e.__dict__)
        print(e.__class__)
        print(e.__module__)
        print(e.with_traceback())
        raise e

    if filtered_user_by_email:

        if provider == filtered_user_by_email["provider"]:

            res, registered_user = await authenticate(email=email, password=settings.SOCIAL.SOCIAL_SECRET, required_fields=required_fields)

            if not res:
                return {
                    "message": "Login Failed",
                    "type": "failed",
                    "status": False
                }

            followers = registered_user.pop('follower')
            following = registered_user.pop('following')

            obj = await convert_to_json(registered_user)

            obj.update({
                "follower_count": len(followers),
                "following_count": len(following)
            })

            return {
                "message": "Successfully Logged In",
                "status": True,
                'type': 'login',
                "data": {
                    'profile': obj,
                    'token': await generate_tokens(str(obj.get("id")))
                }
            }

        else:
            raise AuthenticationError(detail="Login using " + filtered_user_by_email["provider"])
            # raise AuthenticationFailed(
            #     detail='Please continue your login using ' + str(filtered_user_by_email[0].profile.provider))

    else:
        user = {
                '_id': await generate_user_id(),
                'email': email,
                'password': await hash_password(settings.SOCIAL.SOCIAL_SECRET),
                'channel_name': await generate_username(name), 
                'name': name,
                'provider': provider,
                'bio': '',
                'location': '',
                'follower': [],
                'following': [],
                'verified': False,
                'profile_picture': ''
            }

        with Connect() as client:
            result = client.auth.profile.insert_one(user)

        ts = int(time.time() * 1000)

        s3 = S3()
        profile_picture_url = s3.upload_fileobj(f"user_files/{str(result.inserted_id)}/profile/picture{ts}.jpg", picture)

        with Connect() as client:
            client.auth.profile.update_one({"_id": result.inserted_id}, {"$set": {"profile_picture": profile_picture_url}})

        res, registered_user = await authenticate(email=email, password=settings.SOCIAL.SOCIAL_SECRET, required_fields=required_fields)

        followers = registered_user.pop('follower')
        following = registered_user.pop('following')

        obj = await convert_to_json(registered_user)

        obj.update({
            "follower_count": len(followers),
            "following_count": len(following)
        })

        return {
            "message": "Successfully Registered",
            "status": True,
            'type': 'register',
            "data": {
                'profile': obj,
                'token': await generate_tokens(str(result.inserted_id))
            }
        }




# SERIALIZERS 
# FIXME: 

@dataclass(init=True, repr=True)
class GoogleSocialAuthDataClass():
    auth_token: str

    async def is_valid(self, raise_exception: bool = True):
        try:
            output = await self.validate_auth_token(self.auth_token)
            return (True, output)
        except Exception as e:
            if raise_exception:
                raise e
            return (False, {"message": str(e), "status": False})


    async def validate_auth_token(self, auth_token):
        # import pdb; pdb.set_trace()
        user_data = await Google.validate(auth_token)


        try:
            user_data['sub']
        except:
            raise AuthenticationError(
                detail='The id_token is invalid or expired. Please login again.'
            )

        if user_data['aud'] not in settings.SOCIAL.GOOGLE_CLIENT_ID:
            raise AuthenticationError(detail="Google Client ID dont match")


        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        profile_picture_url = user_data['picture']

#        print(profile_picture_url)

        image_temp = NamedTemporaryFile(delete=True, )
        image_temp.write(urlopen(profile_picture_url).read())
        image_temp.seek(0)

        provider = 'google'
        # import pdb; pdb.set_trace()
        return await register_social_user(user_id=user_id, email=email, name=name, provider=provider, picture=image_temp)


# class FacebookSocialAuthSerializer():
#     """Handles serialization of facebook related data"""
#     auth_token: str

#     def validate_auth_token(self, auth_token):
#         user_data = facebook.Facebook.validate(auth_token)
#         print(user_data)
#         try:
#             user_id = user_data['id']
#             email = user_data['email']
#             name = user_data['name']
#             profile_picture_file = ImageFile(io.BytesIO(requests.get(user_data['picture']['data']['url']).content))
#             provider = 'facebook'
#             return register_social_user(
#                 provider=provider,
#                 user_id=user_id,
#                 email=email,
#                 name=name,
#                 picture=profile_picture_file
#             )
#         except Exception as identifier:

#             raise serializers.ValidationError(
#                 'The token  is invalid or expired. Please login again.'
#             )