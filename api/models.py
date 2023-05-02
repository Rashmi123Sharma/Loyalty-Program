from django.db import models


# Create your models here.
class UserDetails(models.Model):
    username=models.CharField(max_length=100,unique=True)
    firstname=models.CharField(max_length=100,unique=True)
    lastname=models.CharField(max_length=100,unique=True)
    dob=models.DateField()
    phone =models.IntegerField(default=20)
    country=models.CharField(max_length=100,unique=True)
