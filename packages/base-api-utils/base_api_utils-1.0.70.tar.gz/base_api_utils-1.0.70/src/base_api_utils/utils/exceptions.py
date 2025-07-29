import logging
import traceback

from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound

from .external_errors import handle_external_service_errors


def custom_exception_handler(e, context):
    if isinstance(e, NotFound):
        return Response({'message': e.__str__()}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(e, ValidationError):
        errors = [str(error) for error in e.detail]
        return Response({'message': 'Validation Failed', 'errors': errors, 'code': 0},
                        status=status.HTTP_412_PRECONDITION_FAILED)

    # First check if DRF handles it
    response = exception_handler(e, context)

    if response is not None:
        return response

    external_error_response = handle_external_service_errors(e)
    if external_error_response:
        return external_error_response

    # Default to 500
    logging.getLogger('api').error(e)
    logging.getLogger('api').error(traceback.format_exc())
    return Response({'message': 'server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)