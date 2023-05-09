from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import UserDetails
from api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class userdetailsserializer(serializers.ModelSerializer):
    class Meta:
        model=UserDetails
        fields='__all__'
        
class UserDetailsSerializersNameOnly(serializers.ModelSerializer):
    class Meta:
        model=UserDetails
        fields=('firstname','lastname')


class Loyaltyserializer(serializers.ModelSerializer):
    class Meta:
        model=Loyalty
        fields='__all__'
        
        
class ImageDatabaseserializer(serializers.ModelSerializer):
    class Meta:
        model=ImageDatabase
        fields='__all__'