from starlette.routing import Route
from .views import GoogleAuthEndpoint, Profile, Following, Followers

routes = [
    Route("/auth/google", GoogleAuthEndpoint),
    Route("/profile", Profile),
    Route("/follower", Followers),
    Route("/following", Following),
]