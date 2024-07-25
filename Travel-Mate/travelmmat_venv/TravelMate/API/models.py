from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class users(AbstractUser):

    name = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=100,null=True)
    password = models.CharField(max_length=100,null=True)
    usertype = models.IntegerField(default=0)
    busprofile= models.FileField(null=True)
    hotelname = models.CharField(max_length=100,null=True)
    hoteladdress = models.CharField(max_length=100,null=True)
    status=models.IntegerField(default=0)


class Busdetails(models.Model):
    owner_id = models.ForeignKey(users,null=True,on_delete=models.CASCADE)
    seat_no = models.CharField(max_length=100,null=True)
    desc = models.CharField(max_length=100,null=True)
    busname = models.CharField(max_length=100,null=True)
    busprofile= models.FileField(null=True)
    status=models.IntegerField(default=0)


class Hoteldetails(models.Model):
    owner_id = models.ForeignKey(users,null=True,on_delete=models.CASCADE)
    room_no = models.CharField(max_length=100,null=True)
    room_desc = models.CharField(max_length=100,null=True)
    roomname = models.CharField(max_length=100,null=True)
    roomprofile= models.FileField(null=True)
    status=models.IntegerField(default=0) 

class package(models.Model):
   
    busname = models.CharField(max_length=100,null=True)
    bus_id = models.ForeignKey(Busdetails,null=True,on_delete=models.CASCADE)
    hotelname = models.CharField(max_length=100,null=True)
    hotel_id = models.ForeignKey(users,null=True,on_delete=models.CASCADE)
    fromplace = models.CharField(max_length=100,null=True)
    toplace = models.CharField(max_length=100,null=True)
    startdate = models.DateField(null=True)
    enddate = models.DateField(null=True)
    amount=models.IntegerField(default=0)
    seats=models.IntegerField(default=0)
    desc = models.CharField(max_length=100,null=True)
    image= models.FileField(null=True)
    room_id=models.ForeignKey(Hoteldetails,null=True,on_delete=models.CASCADE)
    pkg_image= models.FileField(null=True)
    status=models.IntegerField(default=0)
   

class bookings(models.Model):
    user_id = models.ForeignKey(users,null=True,on_delete=models.CASCADE)
    pkg_id = models.ForeignKey(package,null=True,on_delete=models.CASCADE)
    
    date=models.DateField(null=True)
    no_ppl=models.IntegerField(default=0)
    amount=models.IntegerField(default=0)
    status=models.IntegerField(default=0)
class review(models.Model):
    user_id = models.ForeignKey(users,null=True,on_delete=models.CASCADE)
    review = models.CharField(max_length=100,null=True)
   
   


