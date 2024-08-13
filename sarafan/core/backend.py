from datetime import datetime, timedelta, timezone

from jwt import decode as jwt_decode, encode as jwt_encode
from jwt.exceptions import DecodeError, ExpiredSignatureError
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from django.conf import settings as django_settings

from sarafan.constants import JWTAuthSettings


class JWTifier:

    def __init__(self, user=None):
        self.user = user

    @classmethod
    def _encode(cls, user, duration, tok_type):
        dt = datetime.now(tz=timezone.utc) + timedelta(seconds=duration) # noqa E501

        token = jwt_encode(
            {
                'user': str(user.id),
                'exp': dt,
                'tok': tok_type,
                'iat': datetime.now(tz=timezone.utc),

            }, django_settings.SECRET_KEY,
            algorithm=JWTAuthSettings.JWT_ALGORITHM.value,
        )
        return token

    def create_access(
        self, duration=JWTAuthSettings.JWT_ACCESS_DURATION.value
    ):
        return self._encode(self.user, duration, "access")

    def create_refresh(
        self, duration=JWTAuthSettings.JWT_REFRESH_DURATION.value
    ):
        return self.create_access(), self._encode(
            self.user, duration, "refresh"
        )

    @classmethod
    def _decode(cls, jwt):
        try:
            token = jwt_decode(
                jwt,
                django_settings.SECRET_KEY,
                algorithms=JWTAuthSettings.JWT_ALGORITHM.value,
            )
            user = get_user_model().objects.get(
                pk=token["user"], is_active=True
            )
            token["user"] = user
            return token
        except (
            DecodeError,
            ExpiredSignatureError,
            get_user_model().DoesNotExist,
        ):
            return None

    def validate_token(self, jwt, tok_type):
        token = self._decode(jwt) or {"user": None, "tok": None}
        return token["user"] == self.user and token["tok"] == tok_type

    @classmethod
    def user_from_token(cls, jwt):
        token = cls._decode(jwt) or {"user": None}
        return token["user"]

    @classmethod
    def token_from_str(cls, jwt):
        return cls._decode(jwt)


class JWTAuthenticateBackend(BaseBackend):

    def authenticate(
            self,
            request: HttpRequest,
            token: str | None = None,
            **kwargs
    ) -> AbstractBaseUser | None:

        try:
            auth_type, auth_str = token.split(" ")
            assert auth_type.lower() == "bearer"
            return JWTifier.user_from_token(auth_str)
        except (
            AssertionError,
            get_user_model().DoesNotExist,
            ExpiredSignatureError,
            DecodeError,
            ValueError,
            AttributeError,
        ):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id, is_active=True)
        except get_user_model().DoesNotExist:
            return None
