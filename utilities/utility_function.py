def fail_response(error,message):
    return {
        'status':False,
        'message':message,
        'error':str(error),
        'line':str(error.__traceback__.tb_lineno)
    }