from rest_framework.response import Response
def fail_response(error,message):
    return Response({
        'status':False,
        'message':message,
        'error':str(error),
        'line':str(error.__traceback__.tb_lineno)
    })