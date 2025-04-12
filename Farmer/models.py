from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from Guest.models import *
from Admin.models import *



# Create your models here.
class tbl_farmerproduct(models.Model): 
    farmerproduct_stock=models.CharField(max_length=50)
    farmerproduct_date=models.DateField(auto_now_add=True)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)
    farmer=models.ForeignKey(tbl_farmer,on_delete=models.CASCADE)
    farmerproduct_price=models.IntegerField(default=0)


class tbl_frequent_swaps(models.Model):
    antecedent = models.ForeignKey(tbl_product, on_delete=models.CASCADE, related_name="antecedent_product")
    consequent = models.ForeignKey(tbl_product, on_delete=models.CASCADE, related_name="consequent_product")
    support = models.FloatField()
    confidence = models.FloatField()
    lift = models.FloatField()
    keyword = models.CharField(max_length=20, default="Frequent")  # Mark as Frequent
    
class tbl_request(models.Model):
    request_date=models.DateField(auto_now_add=True)
    request_status=models.IntegerField(default=0)
    send_farmer=models.ForeignKey(tbl_farmer, on_delete=models.CASCADE,related_name="send_farmer")
    send_product = models.ForeignKey(tbl_product, on_delete=models.CASCADE,related_name="send_product")
    send_qty = models.CharField(max_length=50)
    receive_farmer=models.ForeignKey(tbl_farmer, on_delete=models.CASCADE,related_name="receive_farmer")
    receive_product = models.ForeignKey(tbl_product, on_delete=models.CASCADE,related_name="receive_product",null=True)
    receive_qty = models.CharField(max_length=50)
    farmer_payment = models.ForeignKey(tbl_farmer, on_delete=models.CASCADE,related_name="farmer_payment",null=True) 

#class tbl_complaint(models.Model):
#     complaint_content=models.CharField(max_length=50)
#     complaint_date=models.DateField(auto_now_add=True)
#     complaint_reply=models.CharField(max_length=50)
#     complaint_status=models.CharField(max_length=50)
#     customer=models.ForeignKey(tbl_customer,on_delete=models.CASCADE,null=True)

class tbl_crop(models.Model):
    crop_file=models.FileField(upload_to='Assets/Crop/Photo/')
    crop_content=models.CharField(max_length=50)
    crop_output=models.CharField(max_length=50)
    farmer=models.ForeignKey(tbl_farmer,on_delete=models.CASCADE)
    

