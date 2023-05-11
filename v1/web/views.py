from django.contrib.auth.models import User
from .serializer import *
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from api.models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from utilities.utility_function import *
from django.db.models import Q
from django.shortcuts import render
from datetime import datetime 
import base64
import pyotp 
import plivo




class ImageDatabaseViewSet(ModelViewSet):
    queryset=ImageDatabase.objects.all()
    serializer_class=ImageDatabaseserializer
    
    def create(self, request, *args, **kwargs):
        try:
            data=request.data
            serializer = ImageDatabaseserializer(data=data,context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data={
                'success':True,
                'data':serializer.data
            }
            return Response(data)
        except Exception as e:
            return fail_response(e,'Failed to create image')



class UserViewSet(ModelViewSet):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields=['user__id','firstname']

    def create(self, request):
        data=request.data
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        details = self.get_queryset()
        details = self.filter_queryset(details)
        details = self.paginate_queryset(details)
        serializer = self.get_serializer(details, many=True)
        return Response(serializer.data)
    
    
    
class CashierSearchViewSet(ViewSet):
    def list(self,request):
        try:
            data=request.query_params.get('search')
            user=Customer.objects.filter(Q(phone_no__icontains=data)|Q(phone_no=data))
            serializer=CustomerSerializer(user,many=True)
            data={
                'status':True,
                'data':serializer.data,
                'message':'Successfully get user details'
            }
            return Response(data)
        except Exception as e:
            return fail_response(e,'Failed to get user details')

class LoyaltyViewSet(ModelViewSet):
    queryset=Loyalty.objects.all()
    serializer_class=Loyaltyserializer
    def create(self,request):
        try:
            if Loyalty.objects.count()==0:
                data=request.data
                serializer = Loyaltyserializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data={
                        'status':True,
                        'message':'Saved Successfully'
                        }
            else:
                queryset=Loyalty.objects.get(id=1)
                serializer = Loyaltyserializer(queryset,data=request.data,partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data={
                        'status':True,
                        'message':'Updated Successfully'
                        }
            return Response(data)
        except Exception as e:

            data={
                'status':False,
                'message':'Failed to save',
                'error':str(e),
                'line':e.__traceback__.tb_lineno
            }
            return Response(data)
        
    def list(self, request):
        #check for new loyalty
        if Loyalty.objects.count()==0:
            data={
                'status':True,
                'loyalty_available':False,
                'message':'No loyalty points available'
            }
            return Response(data)
        
        details=Loyalty.objects.get(id=1)
        serializer = Loyaltyserializer(details,context={'request': request})
        return Response(serializer.data)
            

class CustomerTransactionsViewSet(ViewSet):
    def create(self, request):
        try:
            customer_id=request.data.get('customer_id')
            redeem_points=request.data.get('redeem_points')
            points_to_redeem=request.data.get('points_to_redeem',0)
            redeem_points = redeem_points == 'true'
            customer_points=CustomerPointsBank.objects.filter(customer=customer_id).values('points')
            if len(customer_points)==0:
                data={
                    'customer':customer_id,
                    'points':0
                }
                customer_points=CustomerPointsBankSerializer(data=data)
                customer_points.is_valid(raise_exception=True)
                customer_points.save()
                customer_points=customer_points.data
                customer_points=customer_points['points']
            else:
                customer_points=customer_points[0]['points']

            if redeem_points and points_to_redeem > customer_points:
                return fail_response('','Insufficient points')

            if redeem_points:
                customer_points=customer_points-points_to_redeem
                CustomerPointsBank.objects.filter(customer=customer_id).update(points=customer_points)


            data=dict(request.data.items())
            data={
                'customer':data['customer_id'],
                'amount':data['amount'],
                'add_cashback':data['add_cashback'],
                'points_redeemed':points_to_redeem,
            }
            transaction=CustomerTransactionsSerializer(data=data)
            transaction.is_valid(raise_exception=True)
            transaction.save()
            transaction=CustomerTransactions.objects.get(id=transaction.data['id'])


            if data['add_cashback']=='true':
                loyalty=Loyalty.objects.filter(id=1).values('cashback','min_purchase_required','min_purchase_amount')
                if len(loyalty) != 0:
                    loyalty=loyalty[0]
                    min_purchase_required=loyalty['min_purchase_required']
                    min_purchase_amount=loyalty['min_purchase_amount']
                    if (
                        min_purchase_required == True
                        and data['amount'] >= min_purchase_amount
                        or min_purchase_required != True
                    ):
                        cashback=loyalty['cashback']
                        cashback_percent=cashback
                        cahback_points=(data['amount']*cashback_percent)/100
                        transaction.points_earned=cahback_points
                        transaction.save()
            data={
                'status':True,
                'data':transaction.id,
                'message':'Successfully created transaction'
            }
            return Response(data)

        except Exception as e:
            return fail_response(e,'Failed to create transaction')
        


def returnValue(phone):
    return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"
    # return str(phone) + str(datetime.datetime.now()) + "Some Random Secret Key"


def send_message(reciever,message):
    if not reciever:
        return Response({'message': 'Phone number is missing', 'status': False})
    reciever=f'+91{reciever}'
    client = plivo.RestClient('MANJVJZWRKZDHLMDZMOD','MThjNzc3Y2Q2Y2NhOGY1Y2I3ODRhMmI4YTZhY2Yw')
    client.messages.create(src='+919876910631',dst=reciever,text=message)



class OTPViewSet(ModelViewSet):
    queryset=None
    serializer_class=None

    def list(self,request):
        try:
            
            phone=request.data.get('phone')
            key = base64.b32encode(returnValue(phone).encode())
            otp = pyotp.TOTP(key, interval=300)
            current_otp = otp.now()
            message = f"Your OTP is {current_otp}"
            send_message(phone, message)
            data={
                'status':True,
                'message':'Otp sent'
                

            }
            return Response(data)
        except Exception as e:
            data={
                'status':False,
                'message':'Otp sending Failed'
            }
            return Response(data)

    def create (self,request):
        phone=request.data.get('phone')
        otp=request.data.get('otp')
        key = base64.b32encode(returnValue(phone).encode())
        otp_new = pyotp.TOTP(key, interval=300)
        if(otp==otp_new):
            data={
                'message':'OTP verified',
                'status':True
            }
            # user = User.objects.create(phone=phone)
            # user.save()
        else:
            data={
                'message':'Invalid OTP',
                'status':False

            }
        return Response(data)
