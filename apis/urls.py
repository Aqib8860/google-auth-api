from starlette.routing import Route
from .views import GoogleAuthEndpoint, Profile

routes = [
    Route("/auth/google", GoogleAuthEndpoint),
    Route("/profile", Profile)
]