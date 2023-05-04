from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import UserDetails


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class userdetailsserializer(serializers.ModelSerializer):
    class Meta:
        model=UserDetails
        fields='__all__'
        