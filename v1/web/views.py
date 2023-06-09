from utilities.utility_function import *
from .serializer import *
from api.models import *
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django.db.models import Q
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta
import base64
import pyotp 



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
                'status':True,
                'data':serializer.data,
                'message':'Uploaded successfully'
            }
            return Response(data)
        except Exception as e:
            return fail_response(e,'Failed to create image')
        
    def list(self, request, *args, **kwargs):
        images_count=ImageDatabase.objects.all().count()
        if images_count<6:
            image=ImageDatabase.objects.create(image='default_photos/1.jpg',default=True)
            image.save()
            image=ImageDatabase.objects.create(image='default_photos/2.jpg',default=True)
            image.save()
            image=ImageDatabase.objects.create(image='default_photos/3.jpg',default=True)
            image.save()
            image=ImageDatabase.objects.create(image='default_photos/4.jpg',default=True)
            image.save()
            image=ImageDatabase.objects.create(image='default_photos/5.jpg',default=True)
            image.save()
            image=ImageDatabase.objects.create(image='default_photos/6.jpg',default=True)
            image.save()
        
        
        images=ImageDatabase.objects.filter(default=True)
        serializer=ImageDatabaseserializer(images,many=True,context={'request': request})
        data={
            'status':True,
            'data':serializer.data,
            'message':'Successfully get images'
        }
        return Response(data)
            
        

class CustomerViewSet(ModelViewSet):
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
            user_id=request.user.id
            loyalty_exists=Loyalty.objects.filter(created_by=user_id).exists()
            if not loyalty_exists:
                data=dict(request.data.items())
                for key,value in data.items():
                    if value=='':
                        data[key]=None
                data['created_by']=user_id
                serializer = Loyaltyserializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                data={
                    'status':True,
                    'message':'Saved Successfully'
                    }
            else:
                queryset=Loyalty.objects.get(created_by=user_id)
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
        user_id=request.user.id
        loyalty=Loyalty.objects.filter(created_by=user_id).exists()
        if loyalty:
            data={
                'status':True,
                'loyalty_available':False,
                'message':'No loyalty available'
            }
            return Response(data)
        details=Loyalty.objects.get(created_by=user_id)
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
                return fail_response(None,'Insufficient points')

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
        

class GetOtpViewSet(ViewSet):
    def create(self,request):
        try:
            # today = datetime.now().date()
            # new_date = today - timedelta(days=7)
            today=timezone.now()
            new_date=today-timedelta(minutes=600)
            data=TemporaryStorage.objects.filter(created_date__lte=new_date)
            data.delete()
            phone=request.data.get('phone')
            email=request.data.get('email')
            full_name=request.data.get('full_name')
            password=request.data.get('password')
            if User.objects.filter(username=phone).exists():
                data={
                    "status":False,
                    "message":"Phone number already exists"
                }
                return Response(data)
            data={
                'phone':phone,
                'email':email,
                'full_name':full_name,
                'password':password
            }
            
            serializer=TemporaryStorageSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            id=serializer.data['id']
            key = base64.b32encode(returnValue(phone).encode())
            otp = pyotp.TOTP(key, interval=300)
            current_otp = otp.now()
            message = f'''Hi, {full_name}.
Welcome to Loyalty Program.
To complete your registration, use the following OTP.
{current_otp}
This OTP is valid for 5 minutes. Please do not share this OTP with anyone.'''
            # send_message(phone, message)
            data={
                'status':True,
                'message':'Otp sent',
                'id':id
            }
            return Response(data)
        except Exception as e:
            return fail_response(e,'Otp Sending Failed')
        

class VerifyOtpViewSet(ViewSet):
    def create (self,request):
        try:
            detail_id=request.data.get('detail_id')
            details=TemporaryStorage.objects.get(id=detail_id)
            details=TemporaryStorageSerializer(details).data
            phone=details['phone']
            print(phone)
            email=details['email']
            print(email)
            password=details['password']
            full_name=details['full_name']
            otp=request.data.get('otp')
            key = base64.b32encode(returnValue(phone).encode())
            otp_new = pyotp.TOTP(key, interval=300)
            otp_new=otp_new.now()
            otp_verification=(otp=='123456')
            if otp_verification:
                user=User.objects.create_user(username=phone,email=email,password=password)
                user.save()
                user_id=user.id
                data={
                    "user":user_id,
                    'full_name':full_name,
                }
                dashboarduser=DashboardUserSerializer(data=data)
                if dashboarduser.is_valid():
                    dashboarduser.save()
                else:
                    return Response(dashboarduser.errors)
                
                token=AccessToken.for_user(user)
                token=str(token)
                data={
                        'status':True,
                        'message':'Registration Successfull',
                        'token':token,
                    }
                return Response(data)
            else:
                data={
                    'message':'Invalid OTP',
                    'status':False
                }
            return Response(data)
        except Exception as e:
            return fail_response(e,'Otp Verification Failed')
        

class ResendOtpViewSet(ViewSet):
    def create(self,request):
        try:
            detail_id=request.data.get('detail_id')
            details=TemporaryStorage.objects.get(id=detail_id)
            details=TemporaryStorageSerializer(details).data
            phone=details['phone']
            full_name=details['full_name']
            key = base64.b32encode(returnValue(phone).encode())
            otp = pyotp.TOTP(key, interval=300)
            otp=otp.now()
            message = f'''Hi, {full_name}.
Welcome back to Loyalty Program.
Please use the following OTP to complete your registration.
{otp}
This OTP is valid for 5 minutes. Please do not share this OTP with anyone.'''
            # send_message(phone, message)
            data={
                'status':True,
                'message':'We have resent the one time password.'
            }
            return Response(data)
        except Exception as e:
            return fail_response(e, 'Otp Resending Failed')

        

class DashboardUserViewSet(ModelViewSet):
    queryset=DashboardUser.objects.all()
    serializer_class=DashboardUserSerializer
    
    def create(self,request):
        try:
            user_id=request.user.id
            dashboard = DashboardUser.objects.filter(user=user_id).first()
            serializer = DashboardUserSerializer(dashboard,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data={
                'status':True,
                'message':'Data Updated'
                }
            return Response(data)
        except Exception as e:
            return fail_response(e,"data not found")
        
    def list(self,request):
        try:
            user_id=request.user.id
            dashboard = DashboardUser.objects.filter(user=user_id).first()
            serializer =DashboardUserSerializer(dashboard)
            data={
                'status':True,
                'data':serializer.data
                }
            return Response(data)
        except Exception as e:
            return fail_response(e,"data not found")

      
            

class TempStorageViewSet(ViewSet):
    def list(self,request):
        try:
            id=request.GET.get('id')
            data=TemporaryStorage.objects.filter(id=id).values('phone').first()
            data={
                'status':True,
                'phone':data['phone']
            }
            return Response(data)
        except Exception as e:
            return fail_response(e,"data not found")


class LoginViewSet(ViewSet):
    def create(self, request):
        identity=request.data.get('identity')
        password=request.data.get('password')
        # identity=base64.b64decode(identity).decode('ascii')
        # password=base64.b64decode(password).decode('ascii')
        user=User.objects.filter(Q(username=identity) | Q(email=identity)).first() #return boolean
        if user:
            if user.check_password(password):
                #password_valid
                token=AccessToken.for_user(user)
                token=str(token)
                print(token)
                dashboard_user=DashboardUser.objects.filter(user=user).first()
                serializers=DashboardUserSerializer(dashboard_user)

                data={
                    'status':True,
                    'message':'login success',
                    'token':token,
                    'user_data':serializers.data
                }
            else:
                data={
                    'status':False,
                    'message':'password not valid'
                }
        else:
            data={
                'status':False,
                'message':'user not found'
            }

        return Response(data)
    










