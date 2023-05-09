from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'
        


class Loyaltyserializer(serializers.ModelSerializer):
    class Meta:
        model=Loyalty
        fields='__all__'
        
        
class ImageDatabaseserializer(serializers.ModelSerializer):
    class Meta:
        model=ImageDatabase
        fields='__all__'
        

class CustomerTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerTransactions
        fields='__all__'
        
        
        
        
class CustomerPointsBankSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerPointsBank
        fields='__all__'