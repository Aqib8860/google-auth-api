from starlette.routing import Route
from .views import GoogleAuthEndpoint, Profile, Following, Followers, RefreshToken

routes = [
    Route("/auth/google", GoogleAuthEndpoint),
    Route("/profile", Profile),
    Route("/follower", Followers),
    Route("/following", Following),
    Route("/refresh", RefreshToken)
]