import logging

from django.http import JsonResponse

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return JsonResponse({"error": "Internal Server Error", "message": "Something went wrong."}, status=500)
