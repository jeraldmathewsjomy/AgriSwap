from django.shortcuts import render,redirect
from Admin.models import *
import io
import matplotlib.pyplot as plt
from django.http import HttpResponse
from mlxtend.frequent_patterns import apriori, association_rules
from Guest.models import tbl_customer,tbl_complaint,tbl_farmer
from Farmer.models import tbl_request
import pandas as pd
import matplotlib.pyplot as plt
from django.db.models import Count
from collections import defaultdict
from django.http import JsonResponse

import io
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import redirect
from Farmer.models import tbl_request, tbl_product
# Create your views here.
from Guest.models import *

def dashboard(request):
    new_farmers = tbl_farmer.objects.filter(farmer_status='0')  # Adjust based on your model
    new_customers = tbl_customer.objects.filter(customer_status='0')  # Adjust based on your model

    context = {
        'far': new_farmers,
        'cus': new_customers
    }
    return render(request, 'Admin/dashboard.html', context)

def district(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    if request.method=="POST":
        district=request.POST.get("txt_district")   #txt_district taken frm html page district & is assignd to new variable district
        tbl_district.objects.create(   #tbl creation
            district_name=district    #value in district from previos line gvn to nw varible
        )
        
        msg="Data Inserted"
        return render(request,"Admin/District.html",{"msg":msg})
    else:
        return render(request,"Admin/District.html")  #else stmt compulsory

#ADMIN  
def admino(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    admin=tbl_admin.objects.all()  #many other filtering methd like object.filter
    if request.method=="POST":
        adm=request.POST.get("name")
        admail=request.POST.get("mail")
        adpass=request.POST.get("password")

        tbl_admin.objects.create(
            admin_name=adm,    #admin_name frm Admin.html
            admin_email=admail,
            admin_password=adpass
         )
        msg="Data Inserted"
        return render(request,"Admin/Admin.html",{"msg":msg})
    else:
        return render(request,"Admin/Admin.html",{"Admin":admin})
        
def deladmin(request,id):   #id is self given primary key by the database itself
    tbl_admin.objects.get(id=id).delete()
    return redirect("Admin:admino")

def editadmin(request,id):
    admin=tbl_admin.objects.get(id=id)
    if request.method=="POST":
        admin.admin_name=request.POST.get("name")
        admin.admin_email=request.POST.get("mail")
        admin.admin_password=request.POST.get("password")
        admin.save()
        return redirect('Admin:admino')
    else:
         return render(request,"Admin/Admin.html",{"Edit":admin})
               
#PRODUCT
def product(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    product=tbl_product.objects.all()
    if request.method=="POST":
        pprice=request.POST.get("name")
        
        pphoto=request.FILES.get("product_image")

        tbl_product.objects.create(
           product_name =pprice,
           
           product_image=pphoto,

        )
        msg="Data Inserted"
        return render(request,"Admin/Product.html",{"msg":msg})
    else:
        return render(request,"Admin/Product.html",{"product":product})
    
def delprod(request,did):
        tbl_product.objects.get(id=did).delete()
        return redirect("Admin:product")

def editprod(request,id):
    product=tbl_product.objects.get(id=id)
    if request.method=="POST":
        product.product_name=request.POST.get("Name")
        product.product_price=request.POST.get("Price")
        product.save()
        return redirect("Admin:product")
    else:
        return render(request,"Admin/Product.html",{"edit":product})

def reply(request,id):
    data=tbl_complaint.objects.get(id=id)
    if request.method=='POST':
        data.complaint_reply = request.POST.get("reply")
        data.complaint_status=1
        data.save()
        return render(request, "Admin/Reply.html", {"msg": "Reply Sent Successfully"})
    else:
        return render(request, "Admin/Reply.html")

def category(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    if request.method == "POST":
        categ=request.POST.get("txt_category")
        tbl_category.objects.create(
           category_name =categ
        )
        msg="Data Inserted"
        return render(request,"Admin/Category.html",{"msg":msg})
    else:
        return render(request,"Admin/Category.html")
    
def subcategory(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    cates=tbl_category.objects.all()  #to show everything in category to the drop down menu
    subcates=tbl_subcategory.objects.all()
    if request.method == "POST":
        categ=tbl_category.objects.get(id=request.POST.get("sel_category"))
        s_name=request.POST.get("subcate")
        tbl_subcategory.objects.create(
            category=categ,subcategory_name=s_name
        )
        msg="Data Inserted"
        return render(request,"Admin/Subcategory.html",{"msg":msg})
    else:
        return render(request,"Admin/Subcategory.html",{"cat":cates,"subcates":subcates})

def delsubcategory(request,id):
    tbl_subcategory.objects.get(id=id).delete()
    return redirect("Admin:subcategory")
#for new farmer,accept,reject,reject accepted.accept rejected---------------------------------------------------

def newfarmer(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    farmer=tbl_farmer.objects.filter(farmer_status=0)
    return render(request,'Admin/Newfarmer.html',{'far':farmer})
         
def verify(request,id):
    farm=tbl_farmer.objects.get(id=id)
    farm.farmer_status=1
    farm.save()
    return redirect('Admin:Newfarmer')

def reject(request,id):
    far=tbl_farmer.objects.get(id=id)
    far.farmer_status=2
    far.save()
    return redirect('Admin:Newfarmer')
    
def rejectedfarmer(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    farmer=tbl_farmer.objects.filter(farmer_status=2)
    return render(request,'Admin/Rejectedfarmer.html',{'far':farmer})

def acceptedfarmer(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    farmer=tbl_farmer.objects.filter(farmer_status=1)
    return render(request,'Admin/Acceptedfarmer.html',{'far':farmer})


def rejectverify(request,id):
    farm=tbl_farmer.objects.get(id=id)
    farm.farmer_status=1
    farm.save()
    return redirect('Admin:rejectedfarmer')

def acceptreject(request,id):
    far=tbl_farmer.objects.get(id=id)
    far.farmer_status=2
    far.save()
    return redirect('Admin:acceptedfarmer')


#for new customer,accept,reject,reject accepted.accept rejected---------------------------------------------------

def newcustomer(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    customer=tbl_customer.objects.filter(customer_status=0)
    return render(request,'Admin/Newcustomer.html',{'cus':customer})
         
def custverify(request,id):
    cust=tbl_customer.objects.get(id=id)
    cust.customer_status=1
    cust.save()
    return redirect('Admin:newcustomer')

def custreject(request,id):
    cus=tbl_customer.objects.get(id=id)
    cus.customer_status=2
    cus.save()
    return redirect('Admin:newcustomer')
    
def rejectedcustomer(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    customer=tbl_customer.objects.filter(customer_status=2)
    return render(request,'Admin/Rejectedcustomer.html',{'cus':customer})

def acceptedcustomer(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    customer=tbl_customer.objects.filter(customer_status=1)
    return render(request,'Admin/Acceptedcustomer.html',{'cus':customer})


def custrejectverify(request,id):
    customer=tbl_customer.objects.get(id=id)
    customer.customer_status=1
    customer.save()
    return redirect('Admin:rejectedcustomer')

def custacceptreject(request,id):
    cus=tbl_customer.objects.get(id=id)
    cus.customer_status=2
    cus.save()
    return redirect('Admin:acceptedcustomer')



#district to place drp dwn menu---------------------------------------

def district(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    if request.method == "POST":
        dist=request.POST.get("txt_district")
        tbl_district.objects.create(
           district_name =dist
        )
        msg="Data Inserted"
        return render(request,"Admin/District.html",{"msg":msg})
    else:
        return render(request,"Admin/District.html")
    
def place(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    dist=tbl_district.objects.all()  
    plac=tbl_place.objects.all()
    if request.method == "POST":
        dist=tbl_district.objects.get(id=request.POST.get("sel_district"))
        p_name=request.POST.get("txt_place")
        tbl_place.objects.create(
            district=dist,place_name=p_name
        )
        msg="Data Inserted"
        return render(request,"Admin/Place.html",{"msg":msg})
    else:
        return render(request,"Admin/Place.html",{"dis":dist,"pla":plac})

def delplace(request,id):
    tbl_place.objects.get(id=id).delete()
    return redirect("Admin:place")

def addprice(request, id):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    prod = tbl_product.objects.get(id=id)  
    prices = tbl_price.objects.filter(product=prod)  
    districts = tbl_district.objects.all() 
    
    if request.method == "POST": 
        dist = tbl_district.objects.get(id=request.POST.get("sel_district"))
        pprice = request.POST.get("amount")
        tbl_price.objects.create(
            price_amount=pprice,
            district=dist, 
            product=prod
        ) 
        
        msg = "Data Inserted" 
        return render(request, "Admin/Addprice.html", {"msg": msg, "pro": prod, "dis": districts, "prices": prices}) 
    else: 
        return render(request, "Admin/Addprice.html", {"pro": prod, "dis": districts, "prices": prices})
    
def deleteprice(request, id):
    tbl_price.objects.get(id=id).delete()
    return redirect("Admin:addprice", id=request.GET.get('product_id'))

def viewcomplaint(request):
    if 'aid' not in request.session:
        return redirect('Guest:login')
    data=tbl_complaint.objects.all()
    return render(request,'Admin/Viewcomplaints.html',{'data':data})

def logout(request):
    if 'aid' in request.session:
        del request.session["aid"]
        return redirect("Guest:login")
    else:
        return redirect("Guest:login")


def plot_swap_trends(request):
    if 'fid' in request.session:
        # Fetch swap data: (send_product, receive_product)
        swaps = tbl_request.objects.values_list('send_product', 'receive_product')
        df = pd.DataFrame(swaps, columns=['send_product', 'receive_product'])
        
        # Create a lookup dictionary: {product_id: product_name}
        product_map = {p.id: p.product_name for p in tbl_product.objects.all()}
        # Map receive_product IDs to product names
        df['receive_product'] = df['receive_product'].map(product_map)
        
        if df.empty:
            return None  # No data available

        # Compute the top 5 swapped "receive_product" (by name)
        popular_swaps = df['receive_product'].value_counts().head(5)
        
        # Create a pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(popular_swaps.values,
                labels=popular_swaps.index,
                autopct='%1.1f%%',
                startangle=140,
                colors=plt.cm.Paired.colors)
        plt.title("Top 5 Swapped Products Distribution")
        
        # Save the plot to a BytesIO buffer in PNG format
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        plt.close()  # Free memory
        buffer.seek(0)
        
        return buffer
    else:
        return redirect('Guest:login')  

def swap_trends_view(request):
    if 'aid' in request.session:
        buffer = plot_swap_trends(request)
        
        if buffer is None:
            return HttpResponse("No swap data available", content_type="text/plain")
        
        return HttpResponse(buffer.getvalue(), content_type="image/png")
    else:
        return redirect('Guest:login')  

    


def plot_swap_trends(request):
    if 'aid' in request.session:
        # Fetch swap data: (send_product, receive_product)
        swaps = tbl_request.objects.values_list('send_product', 'receive_product')
        df = pd.DataFrame(swaps, columns=['send_product', 'receive_product'])
        
        # Create a lookup dictionary: {product_id: product_name}
        product_map = {p.id: p.product_name for p in tbl_product.objects.all()}
        # Map receive_product IDs to product names, handling missing values
        df['receive_product'] = df['receive_product'].map(product_map).fillna('Unknown')

        if df.empty or df['receive_product'].nunique() == 0:
            return None  # No data available

        # Compute the top 5 swapped "receive_product" (by name)
        popular_swaps = df['receive_product'].value_counts().head(5)

        # Create a pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(popular_swaps.values,
                labels=popular_swaps.index,
                autopct='%1.1f%%',
                startangle=140,
                colors=plt.cm.Paired.colors)
        plt.title("Top 5 Swapped Products Distribution")

        # Save the plot to a BytesIO buffer in PNG format
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        plt.close()  # Free memory
        buffer.seek(0)

        return buffer
    else:
        return redirect('Guest:login')  

def swap_trends_view(request):
    if 'aid' in request.session:
        buffer = plot_swap_trends(request)
        
        if buffer is None:
            # Return an empty PNG instead of plain text to avoid frontend issues
            empty_buffer = io.BytesIO()
            plt.figure(figsize=(6, 6))
            plt.text(0.5, 0.5, "No Data Available", fontsize=12, ha='center')
            plt.axis("off")
            plt.savefig(empty_buffer, format="png")
            plt.close()
            empty_buffer.seek(0)
            return HttpResponse(empty_buffer.getvalue(), content_type="image/png")

        return HttpResponse(buffer.getvalue(), content_type="image/png")
    else:
        return redirect('Guest:login')
        
        


