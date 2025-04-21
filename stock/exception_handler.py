from rest_framework.views import exception_handler
from datetime import datetime


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # if response is not None:
    #     print(response.data)
    #     response.data['message'] = response.data['detail']
    #     del response.data['detail']
    return response
