from django.db import models
from Admin.models import *

class tbl_customer(models.Model):
    customer_name=models.CharField(max_length=50)
    customer_email=models.CharField(max_length=50)
    customer_cont=models.CharField(max_length=10)
    customer_address=models.CharField(max_length=50)
    customer_photo=models.FileField(upload_to='Assets/Customer/Photo')
    customer_place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    customer_pass=models.CharField(max_length=10)
    customer_status=models.IntegerField(default=0)


class tbl_farmer(models.Model):
    farmer_name=models.CharField(max_length=50)
    farmer_email=models.CharField(max_length=50)
    farmer_contact=models.CharField(max_length=50)
    farmer_address=models.CharField(max_length=50)
    farmer_place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    farmer_photo=models.FileField(upload_to='Assets/Farmer/Photo/')
    farmer_proof=models.FileField(upload_to='Assets/Farmer/Proof/')
    farmer_password=models.CharField(max_length=50)
    farmer_status=models.IntegerField(default=0)


class tbl_complaint(models.Model):
     complaint_title=models.CharField(max_length=50)
     complaint_content=models.CharField(max_length=100)
     complaint_date=models.DateField(auto_now_add=True)
     complaint_reply=models.CharField(max_length=50,default="Not Yet Replayed")
     complaint_status=models.IntegerField(default=0)
     customer=models.ForeignKey(tbl_customer,on_delete=models.CASCADE,null=True)


