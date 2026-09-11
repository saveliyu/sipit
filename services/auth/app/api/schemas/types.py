from enum import StrEnum

from pydantic_extra_types.phone_numbers import PhoneNumber


class UserRole(StrEnum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    CUSTOMER = "customer"


class RuPhoneNumber(PhoneNumber):
    default_region_code = "RU"
    supported_regions = ["RU"]
    phone_format = "INTERNATIONAL"


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
