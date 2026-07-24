from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from app.core.database import engine
from app.core.config import settings
from app.models.user import User
from app.models.profile import Profile
from app.models.measurement import Measurement
from app.models.refresh_token import RefreshToken


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session.update({"authenticated": True})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("authenticated", False)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.phone, User.is_active, User.created_at]


class ProfileAdmin(ModelView, model=Profile):
    column_list = [Profile.id, Profile.user_id, Profile.gender, Profile.age]


class MeasurementAdmin(ModelView, model=Measurement):
    column_list = [
        Measurement.id,
        Measurement.user_id,
        Measurement.name,
        Measurement.is_public,
        Measurement.created_at,
    ]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [
        RefreshToken.id,
        RefreshToken.user_id,
        RefreshToken.revoked,
        RefreshToken.expires_at,
    ]


def setup_admin(app):
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key=settings.ADMIN_SECRET_KEY),
    )
    admin.add_view(UserAdmin)
    admin.add_view(ProfileAdmin)
    admin.add_view(MeasurementAdmin)
    admin.add_view(RefreshTokenAdmin)
