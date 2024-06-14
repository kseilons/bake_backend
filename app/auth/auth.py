import uuid
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from app.core.config import settings

from app.auth.manager import get_user_manager
from app.auth.models import User

from fastapi_users import FastAPIUsers

cookie_transport = CookieTransport(cookie_name="lomo_bake_cookie", cookie_max_age=3600 * 14 * 24)

SECRET = settings.auth.SECRET

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600 * 14 * 24)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
# Get the current active and verified user
current_active_user = fastapi_users.current_user(active=True)
# Get the current active superuser
current_superuser = fastapi_users.current_user(active=True, superuser=True)
