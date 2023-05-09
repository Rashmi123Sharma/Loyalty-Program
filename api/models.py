from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    username=models.CharField(max_length=100,unique=True)
    firstname=models.CharField(max_length=100,unique=False)
    lastname=models.CharField(max_length=100,unique=False)
    dob=models.DateField()
    phone_no =models.IntegerField(default=20)
    country=models.CharField(max_length=100,unique=False)



class Loyalty(models.Model):
    logo=models.ImageField(upload_to="")
    header=models.CharField(max_length=100)
    subtitle=models.CharField(max_length=100)
    themecolor=models.CharField(max_length=100)
    textcolor=models.CharField(max_length=100)
    banner_image=models.ImageField(upload_to="")
    expiry=models.IntegerField(default=20)
    creative=models.TextField(default=True)





