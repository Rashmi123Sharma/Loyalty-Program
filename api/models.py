from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    username=models.CharField(max_length=100,unique=True)
    firstname=models.CharField(max_length=100,unique=False)
    lastname=models.CharField(max_length=100,unique=False)
    dob=models.DateField()
    phone_no=models.CharField(default=20,max_length=10)
    country=models.CharField(max_length=100,unique=False)



class ImageDatabase(models.Model):
    image=models.ImageField(upload_to="database_Images")



class Loyalty(models.Model):
    enabled=models.BooleanField(default=True)
    logo_url=models.ForeignKey(ImageDatabase,on_delete=models.DO_NOTHING,related_name="logos")
    header=models.CharField(max_length=100)
    subtitle=models.CharField(max_length=100)
    themecolor=models.CharField(max_length=10)
    textcolor=models.CharField(max_length=10)
    banner_image=models.ForeignKey(ImageDatabase,on_delete=models.DO_NOTHING,related_name="banners")
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



class CustomerTransactions(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    amount=models.IntegerField(default=0)
    add_cashback=models.BooleanField(default=False)
    points_redeemed=models.IntegerField(default=0)
    points_earned=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    
class CustomerPointsBank(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.DO_NOTHING,unique=True)
    points=models.IntegerField(default=0)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

class DashboardUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,unique=True)
    brand_name=models.CharField(max_length=200,default="",null=True,blank=True)


