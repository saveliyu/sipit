class ApiException(Exception):
    status_code: int = 400
    detail: str = "API Error"


# ----- Auth -----
class PasswordsDoesntMatchException(ApiException):
    status_code: int = 403
    detail: str = "Password Does Not Match"


class PhoneNumberAlreadyExistsException(ApiException):
    status_code: int = 403
    detail: str = "Phone Number Already Exists"


class UserNotFoundOrPasswordIncorrectException(ApiException):
    status_code: int = 403
    detail: str = "User Not Found or Password Incorrect"


class CredentialsException(ApiException):
    status_code: int = 403
    detail: str = "Could not validate credentials"


# ----- JWT Tokens ----
class ExpiredTokenException(ApiException):
    status_code: int = 403
    detail: str = "Expired Token"


class InvalidTokenException(ApiException):
    status_code: int = 403
    detail: str = "Invalid Token"


class InvalidTokenPayloadException(ApiException):
    status_code: int = 403
    detail: str = "Invalid Token Payload"


class InvalidTokenTypeException(ApiException):
    status_code: int = 403
    detail: str = "Invalid Token Type"
