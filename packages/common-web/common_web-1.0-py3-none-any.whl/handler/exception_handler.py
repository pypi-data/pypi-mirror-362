from src.dto.res_dto import ResObj
from src.exception.auth_exception import AuthException
from src.exception.business_exception import BusinessException

SYSTEM_EXCEPTION_CODE = 999
BUSINESS_EXCEPTION_CODE = 500
AUTH_EXCEPTION_CODE = 400


def process_exception(exception):
    print('exception is:', exception)
    if isinstance(exception, BusinessException):
        code = BUSINESS_EXCEPTION_CODE
        message = exception.value
    elif isinstance(exception, AuthException):
        code = AUTH_EXCEPTION_CODE
        message = exception.value
    else:
        code = SYSTEM_EXCEPTION_CODE
        message = "system error"
    return ResObj(code=code, message=message)
