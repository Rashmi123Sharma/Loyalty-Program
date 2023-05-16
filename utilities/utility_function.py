from twilio.rest import Client
import requests
from rest_framework.response import Response
from datetime import datetime 
import plivo


def fail_response(error,message):
    if error is None:
        return Response({
            'status':False,
            'message':message,
        })
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
    account_sid = 'ACb6f647e699efd57e7d8df24306dd27bd'
    auth_token = '05c7962924b226fc98a791f99235723e'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                from_='+12707705402',
                                body = message,
                                to = reciever
                            )



# plivo
# client = plivo.RestClient('ACb6f647e699efd57e7d8df24306dd27bd','8eb120abb14f6735ce6e79928655f54a')
# client.messages.create(src='+919876910631',dst=reciever,text=message)
    
    
# fast2sms
# 9878447129
# !Q2w3e4r5t
# api_key='daS6YTosfR1BXvrzQp8n2yZFi0Pmxut9UCkqKV4l3IhbNWJLc5VQihoW4jDm6pbXtY8xlcKJTrqy5Gk3'
# res=requests.get(f'https://www.fast2sms.com/dev/bulkV2?authorization={api_key}&variables_values={otp}&route=otp&numbers={reciever}')
# print(res.json())
# send_message('9878447129',1234)


    
    
    

