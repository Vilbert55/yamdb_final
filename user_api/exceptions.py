from rest_framework import exceptions


class RefreshConfirmationCode(exceptions.APIException):
    status_code = 201
    default_detail = 'refresh confirmation code'
    default_code = 'refresh_code'
