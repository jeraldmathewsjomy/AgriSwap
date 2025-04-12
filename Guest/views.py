from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *

def index(request):
    return render(request,'Guest/index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('mail')
        password = request.POST.get('password')

        # Checking Admin Login
        admincount = tbl_admin.objects.filter(admin_email=email, admin_password=password).count()
        if admincount > 0:
            admin = tbl_admin.objects.get(admin_email=email, admin_password=password)
            request.session['aid'] = admin.id
            return redirect('Admin:dashboard')

        # Checking Farmer Login
        farmercount = tbl_farmer.objects.filter(farmer_email=email, farmer_password=password).count()
        if farmercount > 0:
            farmer = tbl_farmer.objects.get(farmer_email=email, farmer_password=password)
            if farmer.farmer_status == 2:
                return render(request, "Guest/Login.html", {'msg': "You have been Blocked by administrator, contact immediately"})
            request.session['fid'] = farmer.id
            return redirect('Farmer:dashboard')

        # Checking Customer Login
        customercount = tbl_customer.objects.filter(customer_email=email, customer_pass=password).count()
        if customercount > 0:
            customer = tbl_customer.objects.get(customer_email=email, customer_pass=password)
            if customer.customer_status == 2:
                return render(request, "Guest/Login.html", {'msg': "You have been Blocked by administrator, contact immediately"})
            request.session['cid'] = customer.id
            return redirect('Customer:dashboard')

        # If no valid credentials are found
        return render(request, "Guest/Login.html", {'msg': "Invalid Credentials"})

    else:
        return render(request, "Guest/Login.html")



def customer(request):
    districts = tbl_district.objects.all()
    if request.method == "POST":
        cname = request.POST.get("name")  
        cmail = request.POST.get("mail")
        ccon = request.POST.get("cont")
        place_id = request.POST.get("sel_place")
        cplace = tbl_place.objects.get(id=place_id) 
        cphoto = request.FILES.get('file_photo')
        cpass = request.POST.get("password")

        tbl_customer.objects.create(
                customer_name = cname,
                customer_email = cmail, 
                customer_cont = ccon,
                customer_place = cplace,
                customer_photo = cphoto,
                customer_pass = cpass
            )
        msg = "Data Inserted"


        return render(request, "Guest/Customer.html", {"msg": msg, 'dist': districts})
    
    return render(request, "Guest/Customer.html", {'dist': districts})




def farmer(request):
    districts = tbl_district.objects.all()
    if request.method == "POST":
        fname = request.POST.get("name")
        fmail = request.POST.get("mail")
        fcont = request.POST.get("cont")
        faddr = request.POST.get("addr")
        
        # Check if a place is selected
        place_id = request.POST.get("sel_place")
        if place_id:
            try:
                fplace = tbl_place.objects.get(id=place_id)
            except tbl_place.DoesNotExist:
                fplace = None
        else:
            fplace = None
        
        fpass = request.POST.get("password")
        fphoto = request.FILES.get('file_photo')
        fproof = request.FILES.get('file_proof')

        if fplace:  # Ensure place is selected before creating the farmer record
            tbl_farmer.objects.create(
                farmer_name = fname,
                farmer_email = fmail,
                farmer_contact = fcont,
                farmer_address = faddr,
                farmer_place = fplace,
                farmer_password = fpass,
                farmer_photo = fphoto,
                farmer_proof = fproof,
            )
            msg = "Data Inserted"
        else:
            msg = "Please select a valid place."

        return render(request, "Guest/Farmer.html", {"msg": msg, 'dist': districts})
    
    return render(request, "Guest/Farmer.html", {'dist': districts})


def ajaxplace(request):
    place=tbl_place.objects.filter(district=request.GET.get("did")) #district frm forign key
    return render(request, 'Guest/Ajaxplace.html',{'place':place})