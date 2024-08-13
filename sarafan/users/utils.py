from sarafan.constants import JWTAuthSettings


def set_cookie(response, key, value, path="/"):
    response.set_cookie(
        key=key,
        value=value,
        path=path,
        samesite=JWTAuthSettings.JWT_COOKIE_SAMESITE.value,
        httponly=JWTAuthSettings.JWT_COOKIE_HTTPONLY.value,
        secure=JWTAuthSettings.JWT_COOKIE_SECURE.value,
    )
