from django.db import models


# Create your models here

class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=50)
    admin_email=models.CharField(max_length=50)
    admin_password=models.CharField(max_length=10)

class tbl_district(models.Model):
    district_name=models.CharField(max_length=50)

class tbl_product(models.Model):
    product_name=models.CharField(max_length=50)
    product_image=models.FileField(upload_to='Assets/Product/Photo')

class tbl_price(models.Model):
    price_date=models.DateField(auto_now_add=True)
    price_amount=models.CharField(max_length=50)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
    product=models.ForeignKey(tbl_product,on_delete=models.CASCADE)

class tbl_reply(models.Model):
    reply=models.CharField(max_length=100)

class tbl_category(models.Model):
    category_name=models.CharField(max_length=50)

class tbl_subcategory(models.Model):
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)
    subcategory_name=models.CharField(max_length=50)

class tbl_place(models.Model):
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
    place_name=models.CharField(max_length=50)


