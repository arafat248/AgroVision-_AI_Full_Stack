import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
logger = logging.getLogger('apps')
class ExceptionHandlingMiddleware(MiddlewareMixin):
    """
    Middleware to handle unhandled server-side exceptions.
    Logs tracebacks and formats clean error messages to avoid leaking sensitive stack traces.
    """
    def process_exception(self, request, exception):
        logger.exception(
            f"Unhandled exception during {request.method} {request.get_full_path()}: {str(exception)}"
        )
        
        # We can pass traceback details in local/debug mode, but hide them in production
        from django.conf import settings
        show_details = settings.DEBUG
        
        response_data = {
            'error': exception.__class__.__name__,
            'message': 'An unexpected error occurred on the server.',
            'details': str(exception) if show_details else {}
        }
        
        return JsonResponse(response_data, status=500)
    