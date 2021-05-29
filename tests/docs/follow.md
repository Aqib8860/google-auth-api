# Follow APIs


### Endpoint `/api/following`

<br>

#### Requst Body:

<br>

##### Request to get all the users authenticated user is following

<br>

```yaml
    GET http://54.89.49.194/api/following HTTP/1.1
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJhY2Nlc3MiLCJleHAiOjE2MjE5NjI4MDYsImlkIjoiNjBhN2NlZDVjNDVjZGYyNzRiOTVjNDE1IiwianRpIjoiY0ZGWGxPdVdHcWdCd080ckZaeitHSlduS3g3MGlIQ3B4ZkhHNjlKdHhBMD0ifQ.WYMPt2S8EEDGJup_-1hLTRqVW7ec-_i5raRiYdf09H4
```

#### Response Body: 

```json

{
  "message": "Following List",
  "status": true,
  "data": [
    {
      "email": "voice.myworld@gmail.com",
      "channel_name": "sksarifulislam",
      "name": "Sk Sariful Islam",
      "profile_picture": "https://myworld2021.s3.amazonaws.com/user_files/60a7ced5c45cdf274b95c415/profile/picture1621610200253.jpg",
      "id": "60a7ced5c45cdf274b95c415"
    }
  ]
}

```


<hr/>
<br>

#### Request Body:

<br>

##### Request to Follow an user from the authenticated account

<br>

```yaml
POST http://54.89.49.194/api/following HTTP/1.1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJhY2Nlc3MiLCJleHAiOjE2MjE5NjI4MDYsImlkIjoiNjBhN2NlZDVjNDVjZGYyNzRiOTVjNDE1IiwianRpIjoiY0ZGWGxPdVdHcWdCd080ckZaeitHSlduS3g3MGlIQ3B4ZkhHNjlKdHhBMD0ifQ.WYMPt2S8EEDGJup_-1hLTRqVW7ec-_i5raRiYdf09H4

{
    "id": "60a7ced5c45cdf274b95c415"
}

```

<br>

#### Response Body:

```json
{
  "message": "User Followed",
  "status": true,
  "data": {
    "email": "voice.myworld@gmail.com",
    "channel_name": "sksarifulislam",
    "name": "Sk Sariful Islam",
    "profile_picture": "https://myworld2021.s3.amazonaws.com/user_files/60a7ced5c45cdf274b95c415/profile/picture1621610200253.jpg",
    "id": "60a7ced5c45cdf274b95c415"
  }
}
```

<hr/>
<br>

#### Request Body:

<br>

##### Request to unfollow an user from the authenticated account
<br>

```yaml
DELETE http://54.89.49.194/api/following HTTP/1.1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJhY2Nlc3MiLCJleHAiOjE2MjE5NjI4MDYsImlkIjoiNjBhN2NlZDVjNDVjZGYyNzRiOTVjNDE1IiwianRpIjoiY0ZGWGxPdVdHcWdCd080ckZaeitHSlduS3g3MGlIQ3B4ZkhHNjlKdHhBMD0ifQ.WYMPt2S8EEDGJup_-1hLTRqVW7ec-_i5raRiYdf09H4

{
    "id": "60a7ced5c45cdf274b95c415"
}

```

<br>

#### Response Body:

```json
{
  "message": "Unfollowed",
  "status": true,
  "data": "60a7ced5c45cdf274b95c415"
}
```


### Endpoint `/api/follower`

<br>

#### Request Body:

<br>

##### Request to get all the users who follows the authenticated user
<br>

```yaml
    GET http://54.89.49.194/api/follower HTTP/1.1
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXAiOiJhY2Nlc3MiLCJleHAiOjE2MjE5NjI4MDYsImlkIjoiNjBhN2NlZDVjNDVjZGYyNzRiOTVjNDE1IiwianRpIjoiY0ZGWGxPdVdHcWdCd080ckZaeitHSlduS3g3MGlIQ3B4ZkhHNjlKdHhBMD0ifQ.WYMPt2S8EEDGJup_-1hLTRqVW7ec-_i5raRiYdf09H4
```

#### Response Body: 

```json

{
  "message": "Following List",
  "status": true,
  "data": [
    {
      "email": "voice.myworld@gmail.com",
      "channel_name": "sksarifulislam",
      "name": "Sk Sariful Islam",
      "profile_picture": "https://myworld2021.s3.amazonaws.com/user_files/60a7ced5c45cdf274b95c415/profile/picture1621610200253.jpg",
      "id": "60a7ced5c45cdf274b95c415"
    }
  ]
}

```