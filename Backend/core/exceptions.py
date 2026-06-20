from rest_framework.views import exception_handler
from rest_framework import status
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    if response is not None:
        # Check standard keys
        detail_msg = "Validation failed or request error."
        details = response.data
        
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                detail_msg = response.data['detail']
                # remove detail to prevent redundancy
                del response.data['detail']
            elif len(response.data) == 1 and isinstance(list(response.data.values())[0], list):
                # If single field error
                key = list(response.data.keys())[0]
                detail_msg = f"{key}: {response.data[key][0]}"
        elif isinstance(response.data, list) and len(response.data) > 0:
            detail_msg = str(response.data[0])
        custom_data = {
            'error': exc.__class__.__name__,
            'message': detail_msg,
            'details': details
        }
        response.data = custom_data
        
    return response