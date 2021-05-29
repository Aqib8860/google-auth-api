from starlette.routing import Route
from .views import GoogleAuthEndpoint, Profile, PublicProfile, Following, Followers, RefreshToken, schema_gen

routes = [
    Route("/auth/google", GoogleAuthEndpoint),
    Route("/profile", Profile),
    Route("/public", PublicProfile),
    Route("/follower", Followers),
    Route("/following", Following),
    Route("/refresh", RefreshToken),
    Route("/schema", schema_gen, include_in_schema=False)
]