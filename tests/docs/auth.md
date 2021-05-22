# BASE URL -> https://54.89.49.194

### End Points:

## - /api/auth/google 

#### Content-Type: application/json

#### Body :

```json
    {
        "auth_token": "<GOOGLE AUTH id_token>"
    }
```


#### Response Examples:

##### Success: (200, 201)
```json
    {
        "message": "Successfully Logged In",
        "status": true,
        "data": {
            "profile": {
            "email": "voice.myworld@gmail.com",
            "channel_name": "sksarifulislam",
            "name": "Sk Sariful Islam",
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
```


##### Failure: (400, 401, 500, 501)
```json
    {
        "message": "The id_token is invalid or expired. Please login again.",
        "status": false
    }
```

<hr/>

## - /api/referesh

#### Content-Type: application/json
#### Body:

```json
    {
        "refresh": "<REFRESH TOKEN>"
    }
```

#### Responses:
##### Success: (200, )

```json

    {
        "message": "Token Refreshed",
        "status": true,
        "data": {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJhY2Nlc3MiLCJleHAiOjE2MjE3NTEyNjAsImlkIjoiNjBhN2NlZDVjNDVjZGYyNzRiOTVjNDE1IiwianRpIjoiY0ZGWGxPdVdHcWdCd080ckZaeitHSlduS3g3MGlIQ3B4ZkhHNjlKdHhBMD0ifQ.SFJg5FvbmFgL3d0LnCKNubu_YIY9wjyD24_ZiYd0BXM"
        }
    }

```
