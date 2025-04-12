from django.shortcuts import render,redirect
from Customer.models import *
from Farmer.models import*
from Guest.models import *
from django.db.models import Sum
from django.http import JsonResponse

# Create your views here.


def dashboard(request):
    if 'cid' in request.session:
        return render(request,'Customer/Homepage.html')
    else:
        return redirect('Guest:login')

def myprofile(request):
    if 'cid' in request.session:
        data=tbl_customer.objects.get(id=request.session['cid'])
        return render(request,'Customer/MyProfile.html',{'data':data})
    else:
        return redirect('Guest:login')

 

def editprofile(request):
    if 'cid' in request.session:
        data = tbl_customer.objects.get(id=request.session['cid'])
        
        if request.method == 'POST':
            data.customer_name = request.POST.get("name")        
            data.customer_email = request.POST.get("mail")        
            data.customer_cont = request.POST.get("contact")        
            data.save()
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': "Profile Updated Successfully"})
            
            return render(request, 'Customer/Editprofile.html', {'msg': "Profile Updated"})
        
        return render(request, 'Customer/Editprofile.html', {'data': data})
    else:
        return redirect('Guest:login')
    

def changepassword(request):
    if 'cid' in request.session:
        data=tbl_customer.objects.get(id=request.session['cid'])
        if request.method == "POST":
            cupass=request.POST.get("currentpass")
            npass= request.POST.get("npass")
            cpass=request.POST.get("cpass")
            print(cupass,npass,cpass,data.id)
            if data.customer_pass == cupass:
                if npass == cpass:
                    data.customer_pass = cpass
                    data.save()
                    return render(request,'Customer/Changepassword.html',{'msg':"Profile Updated"})
                else:
                    return render(request,'Customer/Changepassword.html',{'msg1':"Error in Confirm Password"})
            else:
                return render(request,'Customer/Changepassword.html',{'msg1':"Error in Old Password"})
        else:
            return render(request,'Customer/Changepassword.html')
    else:
        return redirect('Guest:login')

def viewproduct(request):
    if 'cid' in request.session:
        product=tbl_farmerproduct.objects.exclude(farmerproduct_price=0)
        return render(request,'Customer/Viewproduct.html',{"product":product})
    else:
        return redirect('Guest:login')


def mybooking(request):
    if 'cid' in request.session:
        return render(request,'Customer/Mybooking.html')
    else:
        return redirect('Guest:login')


def Addcart(request,pid):
    if 'cid' in request.session:
        productdata=tbl_farmerproduct.objects.get(id=pid)
        customerdata=tbl_customer.objects.get(id=request.session["cid"])
        bookingcount=tbl_booking.objects.filter(customer=customerdata,booking_status=0).count()
        if bookingcount>0:
            bookingdata=tbl_booking.objects.get(customer=customerdata,booking_status=0)
            cartcount=tbl_cart.objects.filter(booking=bookingdata,farmerproduct=productdata).count()
            if cartcount>0:
                msg="Already added"
                return render(request,"Customer/Viewproduct.html",{'msg':msg})
            else:
                tbl_cart.objects.create(booking=bookingdata,farmerproduct=productdata)
                msg="Added To cart"
                return render(request,"Customer/Viewproduct.html",{'msg':msg})
        else:
            bookingdata = tbl_booking.objects.create(customer=customerdata)
            tbl_cart.objects.create(booking=tbl_booking.objects.get(id=bookingdata.id),farmerproduct=productdata)
            msg="Added To cart"
            return render(request,"Customer/Viewproduct.html",{'msg':msg})
    else:
        return redirect('Guest:login')

def Mycart(request):
    if "cid" in request.session:
        if request.method=="POST":
            bookingdata=tbl_booking.objects.get(id=request.session["bookingid"])
            bookingdata.booking_amount=request.POST.get("carttotalamt")
            bookingdata.booking_status=1
            bookingdata.save()
            cart = tbl_cart.objects.filter(booking=bookingdata)
            for i in cart:
                i.cart_status = 1
                i.save()
            return redirect("Customer:productpayment")
        else:
            bookcount = tbl_booking.objects.filter(customer=request.session["cid"],booking_status=0).count()
            if bookcount > 0:
                book = tbl_booking.objects.get(customer=request.session["cid"],booking_status=0)
                request.session["bookingid"] = book.id
                cart = tbl_cart.objects.filter(booking=book)
                for i in cart:
                    total_stock = tbl_farmerproduct.objects.filter(product=i.farmerproduct.id).aggregate(total=Sum('farmerproduct_stock'))['total']
                    total_cart = tbl_cart.objects.filter(farmerproduct=i.farmerproduct.id, cart_status=1).aggregate(total=Sum('cart_qty'))['total']
                    # print(total_stock)
                    # print(total_cart)
                    if total_stock is None:
                        total_stock = 0
                    if total_cart is None:
                        total_cart = 0
                    total =  total_stock - total_cart
                    i.total_stock = total
                return render(request,"Customer/MyCart.html",{'cartdata':cart})
            else:
                return render(request,"Customer/MyCart.html")
    else:
        return redirect("Guest:login")
        

def DelCart(request,did):
   tbl_cart.objects.get(id=did).delete()
   return redirect("Customer:Mycart")

def CartQty(request):
   qty=request.GET.get('QTY')
   cartid=request.GET.get('ALT')
   cartdata=tbl_cart.objects.get(id=cartid)
   cartdata.cart_qty=qty
   cartdata.save()
   return redirect("Customer:Mycart")

def productpayment(request):
    if "cid" in request.session:
        bookingdata = tbl_booking.objects.get(id=request.session["bookingid"])
        amt = bookingdata.booking_amount
        if request.method == "POST":
            bookingdata.booking_status = 2
            bookingdata.save()
            return redirect("Customer:loader")
        else:
            return render(request,"Customer/Payment.html",{"total":amt})
    else:
        return redirect("Guest:login")

def loader(request):
    return render(request,"Customer/Loader.html")

def paymentsuc(request):
    return render(request,"Customer/Payment_suc.html")

def mybooking(request):
    if "cid" in request.session:
        book = tbl_booking.objects.filter(customer=request.session["cid"])
        return render(request,"Customer/Mybooking.html",{"book":book})
    else:
        return redirect("Guest:login")

def reproductpayment(request, id):
    bookingdata = tbl_booking.objects.get(id=id)
    amt = bookingdata.booking_amount
    if request.method == "POST":
        bookingdata.booking_status = 2
        bookingdata.save()
        return redirect("Customer:loader")
    else:
        return render(request,"Customer/Payment.html",{"total":amt})

def myproducts(request, id):
    if 'cid' in request.session:
        cart = tbl_cart.objects.filter(booking=id)
        return render(request, "Customer/Myproducts.html", {"cart":cart})
    else:
        return redirect('Guest:login')

def complaint(request):
    if 'cid' in request.session:
        data=tbl_customer.objects.get(id=request.session['cid'])
        if request.method == "POST":
            tit=request.POST.get("txt_title")
            contnt= request.POST.get("txt_content")
            
            tbl_complaint.objects.create(
                complaint_title=tit,
                complaint_content=contnt,
                customer=data,
                
            )
            msg = "Data Inserted"
            return render(request, "Customer/Complaint.html", {"msg": msg})
        else:
            return render(request,'Customer/Complaint.html')
    else:
        return redirect('Guest:login')

def mycomplaints(request):
    if 'cid' in request.session:
        data=tbl_complaint.objects.filter(customer=request.session['cid'])
        return render(request,'Customer/Mycomplaints.html',{'data':data})
    else:
        return redirect('Guest:login')

def delcomp(request,id):
    tbl_complaint.objects.get(id=id).delete()
    return render(request,'Customer/Complaint.html',{'msg':"Complaint Removed"})

def logout(request):
    if 'cid' in request.session:
        del request.session["cid"]
        return redirect("Guest:login")
    else:
        return redirect("Guest:login")


