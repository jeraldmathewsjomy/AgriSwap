from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from Farmer.models import *
from Guest.models import *
from Admin.models import *

class tbl_booking(models.Model):
    booking_date = models.DateField(auto_now_add=True)
    booking_amount = models.CharField(max_length=30)
    booking_status = models.IntegerField(default=0)
    customer = models.ForeignKey(tbl_customer, on_delete=models.CASCADE)
    
class tbl_cart(models.Model):
    cart_qty = models.IntegerField(default=1)
    cart_status = models.IntegerField(default=0)
    farmerproduct = models.ForeignKey(tbl_farmerproduct, on_delete=models.CASCADE)
    booking = models.ForeignKey(tbl_booking, on_delete=models.CASCADE)