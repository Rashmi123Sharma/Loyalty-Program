from django.contrib.auth.models import User
from .serializer import *
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from api.models import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

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
            data={
                'status':False,
                'message':'Failed to create image',
                'error':str(e),
                'line':str(e.__traceback__.tb_lineno)
            }
            return Response(data)



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
        details=self.filter_queryset(details)
        details=self.paginate_queryset(details)
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
            data={
                'status':False,
                'message':'Failed to get user details',
                'error':str(e),
                'line':str(e.__traceback__.tb_lineno)
            }
            return Response(data)

class LoyaltyViewSet(ModelViewSet):
    queryset=Loyalty.objects.all()
    serializer_class=Loyaltyserializer

    