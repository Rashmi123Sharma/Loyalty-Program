from django.contrib.auth.models import User
from .serializer import *
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from api.models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from utilities.utility_function import *
from django.db.models import Q



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
                if len(loyalty)==0:
                    pass
                else:
                    loyalty=loyalty[0]
                    cashback=loyalty['cashback']
                    min_purchase_required=loyalty['min_purchase_required']
                    min_purchase_amount=loyalty['min_purchase_amount']
                    if min_purchase_required==True:
                        if data['amount']>=min_purchase_amount:
                            cashback_percent=cashback
                            cahback_points=(data['amount']*cashback_percent)/100
                            transaction.points_earned=cahback_points
                            transaction.save()
                    else:
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
        
        
        