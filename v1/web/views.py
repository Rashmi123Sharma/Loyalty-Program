from django.contrib.auth.models import User
from .serializer import UserSerializer,userdetailsserializer,Loyaltyserializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from api.models import UserDetails,Loyalty
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters


class UserViewSet(ModelViewSet):
    queryset=UserDetails.objects.all()
    serializer_class=userdetailsserializer
    filter_backends = [filters.SearchFilter]
    search_fields=['user__id','firstname']

    def create(self, request):
        data=request.data
        serializer = userdetailsserializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        details = UserDetails.objects.all()
        details=self.filter_queryset(details)
        details=self.paginate_queryset(details)
        serializer = userdetailsserializer(details, many=True)
        return Response(serializer.data)
    

class LoyaltyViewSet(ModelViewSet):
    queryset=Loyalty.objects.all()
    serializer_class=Loyaltyserializer

    