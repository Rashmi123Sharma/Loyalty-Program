from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    username=models.CharField(max_length=100,unique=True)
    firstname=models.CharField(max_length=100,unique=False)
    lastname=models.CharField(max_length=100,unique=False)
    dob=models.DateField()
    phone_no =models.CharField(default=20)
    country=models.CharField(max_length=100,unique=False)



class ImageDatabase(models.Model):
    image=models.ImageField(upload_to="database_Images")

class Loyalty(models.Model):
    
    enabled=models.BooleanField(default=True)
    logo_url=models.ForeignKey(ImageDatabase,on_delete=models.DO_NOTHING)
    header=models.CharField(max_length=100)
    subtitle=models.CharField(max_length=100)
    themecolor=models.CharField(max_length=10)
    textcolor=models.CharField(max_length=10)
    banner_image=models.ForeignKey(ImageDatabase,on_delete=models.DO_NOTHING)
    cashback=models.IntegerField(default=20)
    min_purchase_required=models.BooleanField(default=False)
    min_purchase_amount=models.IntegerField(default=20)
    terms=models.TextField(default=True)
    html=models.TextField(default=True)
    
    cashback_reminder_enabled=models.BooleanField(default=False)
    reminder_value=models.IntegerField(default=20)
    reminder_choice=models.CharField(max_length=10,default='days') #days or weeks
    remind_only_eligible_customers=models.BooleanField(default=False)
    cashback_expiry_enabled=models.BooleanField(default=False)
    expiry_months=models.IntegerField(default=20)







