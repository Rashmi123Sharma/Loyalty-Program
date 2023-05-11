from rest_framework.response import Response
from datetime import datetime 
import plivo


def fail_response(error,message):
    return Response({
        'status':False,
        'message':message,
        'error':str(error),
        'line':str(error.__traceback__.tb_lineno)
    })


def returnValue(phone):
    return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"
   


def send_message(reciever,message):
    if not reciever:
        return Response({'message': 'Phone number is missing', 'status': False})
    reciever=f'+91{reciever}'
    client = plivo.RestClient('MANJVJZWRKZDHLMDZMOD','MThjNzc3Y2Q2Y2NhOGY1Y2I3ODRhMmI4YTZhY2Yw')
    client.messages.create(src='+919876910631',dst=reciever,text=message)