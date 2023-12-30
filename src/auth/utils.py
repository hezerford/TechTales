from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy
from decouple import config

cookie_transport = CookieTransport(cookie_max_age=3600)

SECRET = config('JWT_KEY')

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)