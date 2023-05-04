from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet,ViewSet
from django.contrib.auth.models import User
from rest_framework.response import Response
from v1.app.serializer import UserSerializer,UserProfileSerializer

class SignUp(ViewSet):
    def create(self,request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            
            data = {
                'username': username,
                 'email':email,
                 'password':password,
                 
            }
            print(username,email,password)
            user = User.objects.create_user(**data)
            
            user.save()
            
            data={
                'status': True,
                'message':'User created!!'
            }
            return Response(data)
        except Exception as e:
            data={
                'status':False,
                'message':'Failed !!'
            }
            return Response(data)
        
             
        
    def list(self,request):
        user=User.objects.all()
        serializers= UserSerializer(user,many=True)
        data=serializers.data
        data={
            'data':data,
            'status':True,
        }
        return Response(data)
    
  
class UserProfileView(ViewSet):
    def create(self, request):
        try:
            username = request.data.get('username')
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            dob = request.data.get('dob')
            phone_no = request.data.get('phone_no')
            country = request.data.get('country')

 
            user = User.objects.create_user(username=username)

       
            user_profile = UserProfileSerializer(
                user=user,
                firstname=firstname,
                lastname=lastname,
                dob=dob,
                phone_no=phone_no,
                country=country
            )
            user_profile.save()

            data = {
                'status': True,
                'message': 'User created!'
            }
            return Response(data)
        except Exception as e:
            data = {
                'status': False,
                'message': 'Failed to create user.'
            }
            return Response(data)
