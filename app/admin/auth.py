from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed

from app.core import config


class AdminAuthProvider(AuthProvider):
    """
    This is only for demo purpose, it's not a better
    way to save and validate user credentials

    Docs:
    https://jowilf.github.io/starlette-admin/user-guide/authentication/
    """

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if username == config.admin.login and password == config.admin.password:
            """Save `username` in session"""
            request.session.update({"username": username})
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) == config.admin.login:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            request.state.user = config.admin.login
            return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        return AdminConfig(app_title=config.admin.title)

    def get_admin_user(self, request: Request) -> AdminUser:
        return AdminUser(username=config.admin.login)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
