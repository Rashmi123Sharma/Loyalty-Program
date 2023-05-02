from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    username=models.CharField(max_length=100,unique=True)
    firstname=models.CharField(max_length=100,unique=True)
    lastname=models.CharField(max_length=100,unique=True)
    age=models.IntegerField(default=20)
    phone_no =models.IntegerField(default=20)
    country=models.CharField(max_length=100,unique=True)
