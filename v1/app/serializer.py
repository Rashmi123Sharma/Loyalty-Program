from api.models import User

from rest_framework import serializers

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_fields = ['username','firstname','lastname','dob','phone_no','country']
    