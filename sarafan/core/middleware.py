from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate

from sarafan.constants import JWTAuthSettings


class JWTAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request) -> None:

        access_token_str = request.COOKIES.get(
            JWTAuthSettings.JWT_ACCESS_HEADER.value,
        )
        if access_token_str and not request.user.is_authenticated:

            request.user = (
                authenticate(
                    request, token=access_token_str,
                ) or AnonymousUser()
            )
