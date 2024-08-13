from enum import IntEnum, Enum


class JWTAuthSettings(Enum):
    """Костанты для конфигураций jwt аутентификации."""

    JWT_ACCESS_DURATION = 3600  # seconds
    JWT_ACCESS_HEADER = "Authorization"
    JWT_ALGORITHM = "HS256"
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = "Strict"
    JWT_COOKIE_SECURE = True
    JWT_LOGOUT_ACCESS = True
    JWT_REFRESH_DURATION = 36000  # seconds
    JWT_REFRESH_PATH = "/users/refresh/"


class NumericalValues(IntEnum):
    """Константы для числовых значений."""

    PAGINATION_CATEGORY_VALUE = 3
    PAGINATION_PRODUCT_VALUE = 2
    PRODUCT_CATEGORY_NAME_MAX_LEN = 50
    PRODUCT_CATEGORY_SLUG_MAX_LEN = 25
    PRODUCT_SUBCATEGORY_NAME_MAX_LEN = 50
    PRODUCT_SUBCATEGORY_SLUG_MAX_LEN = 25
    PRODUCT_NAME_MAX_LEN = 100
    PRODUCT_SLUG_MAX_LEN = 25


class ImageSizeValues(Enum):
    """Константы для изображений."""

    BIG_SIZE = (640, 480)
    MID_SIZE = (320, 240)
    SMALL_SIZE = (240, 180)
    COLOR_IMAGE = (256, 0, 0)
    FORMAT_IMAGE = "RGBA"
    EXT_IMAGE = "png"
