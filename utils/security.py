import jwt
from utils.db import Connect
import datetime
from server.settings import SECURITY

from Crypto.Random import get_random_bytes
import base64

from starlette.responses import JSONResponse


import hashlib
import os

import functools

async def hash_password(password: str):
    return base64.b64encode(hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        password.encode('iso-8859-1'), # Convert the password to bytes
        SECURITY.SECRET_KEY.encode("iso-8859-1"), # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )).decode("iso-8859-1")

async def authenticate(email: str, password: str, required_fields: dict = {'_id': True}) -> bool:
    user = None
    with Connect() as client:
        user = client.auth.profile.find_one({"email": email, "password": await hash_password(password)}, required_fields)
    
    return (True, user) if user else (False, None)

async def generate_payloads(id):
    present_time = datetime.datetime.utcnow()
    jti = base64.b64encode(get_random_bytes(32)).decode("iso-8859-1")

    return {
        "access": {
            "typ": "access",
            "exp": present_time + SECURITY.JWT_ACCESS_TOKEN_EXPIRY,
            "id": id,
            "jti": jti
        },
        "refresh": {
            "typ": "refresh",
            "exp": present_time + SECURITY.JWT_REFRESH_TOKEN_EXPIRY,
            "iat": present_time,
            "id": id,
            "jti": jti
        }
    }

async def generate_tokens(id):
    payloads = await generate_payloads(id)
    tokens = {
            "refresh_token": await generate_refresh_token(payloads.get('refresh')),
            "access_token": await generate_access_token(payloads.get('access'))
        }

    return tokens


async def generate_refresh_token(payload: dict):
    with Connect() as client:
        jwt_obj = client.auth.jwt.find_one({'user_id': payload.get('id')}, )

        if jwt_obj:
            client.auth.jwt.delete_one({'user_id': payload.get('id')})

        data = {
                "user_id": payload.get('id'),
                "jti": payload.get('jti'),
                "iat": payload.get('iat')
            }
        client.auth.jwt.ensure_index("iat", expireAfterSeconds=SECURITY.JWT_REFRESH_TOKEN_EXPIRY.total_seconds())
        client.auth.jwt.insert(data)

    return jwt.encode(payload=payload, algorithm="HS256", key=SECURITY.JWT_SECRET_KEY)

async def generate_access_token(payload: dict):
    return jwt.encode(payload=payload, algorithm="HS256", key=SECURITY.JWT_SECRET_KEY)


async def verify_access_token(token):
    present_time = datetime.datetime.utcnow()
    try:
        payload = jwt.decode(token, algorithms=["HS256"], key=SECURITY.JWT_SECRET_KEY)

        if payload.get("typ") != "access":
            raise jwt.exceptions.InvalidKeyError("Refresh token sent")

        if present_time.timestamp() > payload.get("exp"):
            raise jwt.exceptions.ExpiredSignatureError("Token Invalid or Expired")

        return True, payload.get('id')

    except Exception as e:
        raise e


def jwt_authentication(endpoint, *args, **kwargs):

    @functools.wraps(endpoint)
    async def inner(self, request, **kwargs):

        try:
            print(request.headers)
            token = request.headers['authorization'].split(" ")[1]

            res, user_id = await verify_access_token(token)
            if res:
                request.user_id = user_id
                return await endpoint(self, request, **kwargs)

        except Exception as e:
            return JSONResponse(content={
                "message": str(e),
                "status": False
            }, status_code=401)

    return inner

