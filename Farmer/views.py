from Farmer.models import*
from Guest.models import*
from Admin.models import*
from datetime import date
from django.db.models import Count
from collections import defaultdict
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage

# ml imports
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from skimage.io import imread
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

MODEL_PATH = os.path.join("Assets", "Model", "updated.h5")
model = load_model(MODEL_PATH)                                                                                                                                                                                                                                                                                  


# Create your views here.
def Homepage(request):
    if 'fid' not in request.session:
        return redirect('Guest:login')  
    return render(request,'Farmer/Homepage.html')

def myprofile(request): 
    if 'fid' not in request.session:
        return redirect('Guest:login')   
    data=tbl_farmer.objects.get(id=request.session['fid'])
    return render(request,'Farmer/MyProfile.html',{'data':data})

def editprofile(request):
    if 'fid' not in request.session:
        return redirect('Guest:login')  
    data = tbl_farmer.objects.get(id=request.session['fid'])
    if request.method == 'POST':
        if request.FILES.get("profile_picture"):
            # Update the profile picture
            data.farmer_photo = request.FILES.get("profile_picture")
            data.save()
            return JsonResponse({
                'success': True,
                'new_photo_url': data.farmer_photo.url,
                'message': 'Profile Picture Updated'
            })
        
        # Update the other profile details
        data.farmer_name = request.POST.get("name")        
        data.farmer_email = request.POST.get("mail")        
        data.farmer_contact = request.POST.get("contact")        
        data.farmer_address = request.POST.get("address")
        data.save()

        # Send a response with success message for profile update
        return JsonResponse({
            'success': True,
            'message': 'Profile Updated Successfully'
        })
    else:
        return render(request, 'Farmer/Editprofile.html', {'data': data})
    

def changepassword(request):
    if 'fid' not in request.session:
        return redirect('Guest:login')  
    data=tbl_farmer.objects.get(id=request.session['fid'])
    if request.method == "POST":
        cupass=request.POST.get("currentpass")
        npass= request.POST.get("npass")
        cpass=request.POST.get("cpass")
        print(cupass,npass,cpass,data.id)
        if data.farmer_password == cupass:
            if npass == cpass:
                data.farmer_password = cpass
                data.save()
                return render(request,'Farmer/Changepassword.html',{'msg':"Profile Updated"})
            else:
                return render(request,'Farmer/Changepassword.html',{'msg1':"Error in Confirm Password"})
        else:
            return render(request,'Farmer/Changepassword.html',{'msg1':"Error in Old Password"})
    else:
        return render(request,'Farmer/Changepassword.html')
    
def viewproduct(request):
    if 'fid' not in request.session:
        return redirect('Guest:login')  
    product=tbl_product.objects.all()
    return render(request,'Farmer/Viewproduct.html',{'product':product})

def stock(request, pid):
    if 'fid' not in request.session:
        return redirect('Guest:login')  
    farmerid=tbl_farmer.objects.get(id=request.session['fid'])
    currentstock=tbl_farmerproduct.objects.filter(farmer=farmerid,product_id=pid)
    productid = tbl_product.objects.get(id=pid)

    if request.method == "POST":
        stock = int(request.POST.get("stock"))
        data = tbl_farmerproduct.objects.filter(product=productid,farmer=farmerid).count()
        if data:
            st = tbl_farmerproduct.objects.get(product=productid,farmer=farmerid)
            total = int(st.farmerproduct_stock) + stock
            st.farmerproduct_stock = total
            st.farmerproduct_date = date.today()
            st.save()
            return redirect('Farmer:viewproduct') 
        else:
            tbl_farmerproduct.objects.create(farmerproduct_stock=stock,product=productid,farmer=farmerid)
            return redirect('Farmer:viewproduct') 
    return render(request, 'Farmer/Stock.html',{'data':currentstock})

def editstock(request,id):
    if 'fid' not in request.session:
        return redirect('Guest:login')  
    stk=tbl_farmerproduct.objects.get(id=id)

    if request.method=="POST":
        stk.farmerproduct_stock=request.POST.get("stock")
        stk.save()
        return redirect('Farmer:viewproduct')
    else:
        return render(request,"Farmer/Stock.html",{"st":stk})
    
# def myproducts(request):
#     farmerdata=tbl_farmer.objects.get(id=request.session['fid'])
#     produc=tbl_farmerproduct.objects.filter(farmer=request.session['fid'])
#     productprice=tbl_price.objects.filter()
#     productid = []
    
#     for i in produc:
#         productid.append(i.product.id)
#     pid = set(productid)
#     # print(pid)
#     pro = tbl_product.objects.filter(id__in=pid)
#     for p in pro:
#         st = 0
#         stock = tbl_farmerproduct.objects.filter(product=p.id,farmer=request.session['fid'])
#         for s in stock:
#             st = st + int(s.farmerproduct_stock)
#         p.stock = st   
#     return render(request,'Farmer/Myproducts.html',{'product':pro})



def myproducts(request):
    if 'fid' not in request.session:
        return redirect('Guest:login')  
    farmer = tbl_farmer.objects.get(id=request.session["fid"])
    district = farmer.farmer_place.district.id
    
    produc=tbl_farmerproduct.objects.filter(farmer=request.session['fid'])
    productid = []
    
    for i in produc:
        productid.append(i.product.id)
    pid = set(productid)
    # print(pid)
    pro = tbl_product.objects.filter(id__in=pid)#used early for price updation
    for p in pro:
        pricecount = tbl_price.objects.filter(district=district, product=p.id).count()
        # print(pricecount)
        if pricecount == 0:
            p.status=1
        else:
            p.status=0
        st = 0
        stock = tbl_farmerproduct.objects.filter(product=p.id,farmer=request.session['fid'])
        for s in stock:
            st = st + int(s.farmerproduct_stock)
        p.stock = st   
    return render(request,'Farmer/Myproducts.html',{'product':produc})


def addprice(request,id):
    if 'fid' not in request.session:
        return redirect('Guest:login')  
    data=tbl_farmerproduct.objects.get(id=id)
    if request.method=='POST':
        data.farmerproduct_price=request.POST.get('price')
        data.save()
        return redirect('Farmer:myproducts')
    else:
        return render(request,'Farmer/FarmerPrice.html')


def ajaxcal(request):
    farmer = tbl_farmer.objects.get(id=request.session["fid"])
    district = farmer.farmer_place.district.id
    # print(district)
    price = tbl_price.objects.filter(district=district,product=request.GET.get('pid')).last()
    # print(price.price_amount)
    total = int(price.price_amount) * int(request.GET.get('qty'))
    # print(total)
    return JsonResponse({"msg":total})


def confirmation(request):
    return render(request,'Farmer/Confirmation.html')




#exchange



def exchange(request):
    # Ensure user is logged in
    if 'fid' not in request.session:
        return redirect('Guest:login')  

    loginfarmerid = request.session['fid']
    farmerid = tbl_farmer.objects.get(id=loginfarmerid)

    # --- 🔹 Fetch Products from Different Districts ---
    productdata = tbl_farmerproduct.objects.exclude(
        farmer__farmer_place__district=farmerid.farmer_place.district
    )

    for i in productdata:
        # Get the price in the product's district
        price = tbl_price.objects.filter(
            product=i.product.id, district=i.farmer.farmer_place.district.id
        ).last()
        i.price = int(price.price_amount) if price else "Price Not Available"

        # Get the price in the logged-in farmer's district
        myprice = tbl_price.objects.filter(
            product=i.product.id, district=farmerid.farmer_place.district.id
        ).last()
        i.myprice = int(myprice.price_amount) if myprice else "Price Not Added"

    # --- 🔹 Fetch Suggested Items for the Logged-in Farmer ---
    frequent_requests = (
        tbl_request.objects
        .filter(send_farmer=loginfarmerid)  # Only fetch requests for the logged-in farmer
        .values('send_farmer', 'send_product')
        .annotate(request_count=Count('id'))
        .filter(request_count__gt=1)  # Only if requested more than once
    )

    suggested_items = defaultdict(list)
    enriched_data = []

    for req in frequent_requests:
        farmer_id = req['send_farmer']
        product_id = req['send_product']

        # Fetch related names
        farmer_name = tbl_farmer.objects.get(id=farmer_id).farmer_name
        product_name = tbl_product.objects.get(id=product_id).product_name

        # Store enriched data
        enriched_data.append({
            'farmer_id': farmer_id,
            'farmer_name': farmer_name,
            'product_id': product_id,
            'product_name': product_name,
        })

        suggested_items[farmer_id].append(product_name)

    sugdata=pd.DataFrame(enriched_data)
    print(sugdata)


    # Count requests per product
    return render(request, 'Farmer/Exchange.html', {
        'product': productdata,  # Exchange products
        'suggested_items': dict(suggested_items),  # Suggested frequently requested items
        'data': enriched_data  # Additional data
    })



def ajaxsendrequest(request):
    tbl_request.objects.create(send_farmer=tbl_farmer.objects.get(id=request.session["fid"]),
        send_product=tbl_product.objects.get(id=request.GET.get("pid")),
        send_qty=request.GET.get("qty"),
        receive_farmer=tbl_farmer.objects.get(id=request.GET.get("fid")))
    return JsonResponse({"msg":"Request Sent"})




def myrequest(request):
    if 'fid' in request.session:
        farmer = tbl_farmer.objects.get(id=request.session["fid"])
        requests = tbl_request.objects.filter(send_farmer=farmer)
        return render(request, 'Farmer/Myrequest.html', {'requests': requests,"farmerid": farmer.id})
    else:
        return redirect('Guest:ogin')  


def viewrequest(request):
    if 'fid' in request.session:
        farmer = tbl_farmer.objects.get(id=request.session["fid"])
        requests = tbl_request.objects.filter(receive_farmer=farmer)
        return render(request, 'Farmer/Viewrequest.html',{'requests':requests,"farmerid": farmer.id})
    else:
        return redirect('Guest:login')  

def otherproducts(request, id):
    if 'fid' in request.session:
        farmerid = tbl_farmer.objects.get(id=request.session['fid'])
        requests = tbl_request.objects.get(id=id)
        farmer = requests.send_farmer.id
        stock = tbl_farmerproduct.objects.filter(farmer=farmer)

        for i in stock:
            # Fetch price in sender's district
            price = tbl_price.objects.filter(
                product=i.product.id, 
                district=i.farmer.farmer_place.district.id
            ).last()
            i.price = int(price.price_amount) if price else "Price Not Available"  # ✅ Fix

            # Fetch price in logged-in farmer's district
            myprice = tbl_price.objects.filter(
                product=i.product.id, 
                district=farmerid.farmer_place.district.id
            ).last()
            i.myprice = int(myprice.price_amount) if myprice else "Price Not Added"  # ✅ Fix

        return render(request, 'Farmer/Otherproducts.html', {"product": stock, "req": id})
    else:
        return redirect('Guest:login')  
  


def returnrequest(request):
    req = tbl_request.objects.get(id=request.GET.get("reqid"))
    req.receive_product = tbl_product.objects.get(id=request.GET.get("pid"))
    req.receive_qty = request.GET.get("qty")
    req.request_status = 1
    req.save()
    return JsonResponse({"msg":"Request Returned"})

def rejectrequest(request, id):
    req = tbl_request.objects.get(id=id)
    req.request_status = 2
    req.save()
    return render(request, 'Farmer/Viewrequest.html',{'msg':"Request Rejected"})

def requestPayment(request, id):
    req = tbl_request.objects.get(id=id)
    sendfarmer = tbl_farmer.objects.get(id=req.send_farmer.id)
    sendproduct = req.send_product.id
    sendqty = req.send_qty
    receivefarmer = tbl_farmer.objects.get(id=req.receive_farmer.id)
    receiveproduct = req.receive_product.id
    receiveqty = req.receive_qty
    if sendfarmer.id == request.session["fid"]:
        price = tbl_price.objects.filter(product=sendproduct,district=receivefarmer.farmer_place.district.id).last()
        total_price = int(price.price_amount) * int(sendqty)
        # print(price.price_amount)
        # print(total_price)
    elif receivefarmer.id == request.session["fid"]:
        price = tbl_price.objects.filter(product=receiveproduct,district=sendfarmer.farmer_place.district.id).last()
        total_price = int(price.price_amount) * int(receiveqty)
        # print(price.price_amount)
        # print(total_price)
    if request.method == 'POST':
        if req.request_status == 3:
            req.request_status = 4
            req.farmer_payment = tbl_farmer.objects.get(id=request.session["fid"])
            req.save()
            return redirect("Farmer:loader")
        else:
            req.request_status = 3
            req.farmer_payment = tbl_farmer.objects.get(id=request.session["fid"])
            req.save()
            return redirect("Farmer:loader")
    else:
        return render(request,"Farmer/Payment.html",{"amount":total_price})

def loader(request):
    return render(request,"Farmer/Loader.html")

def paymentsuc(request):
    return render(request,"Farmer/Paymentsuc.html")

    
#-----------------------------------------------------------------------------------
#swapping
def farmer_suggestions(request):
    if 'fid' in request.session:
        # Fetch the farmer's stock based on their ID
        farmer = tbl_farmer.objects.get(id=request.session['fid'])
        farmer_products = tbl_farmerproduct.objects.filter(farmer=farmer)
        products_in_stock = [p.product.product_name for p in farmer_products]
        
        # Convert the products_in_stock to a regex pattern or join as a string
        matching_rules = tbl_productrule.objects.filter(
            antecedents__regex=r'(' + '|'.join(products_in_stock) + ')'
        )
        
        # Collect the suggested products (consequents)
        suggestions = []
        for rule in matching_rules:
            suggestions.extend(rule.consequents.split(','))  # Assuming consequents is a comma-separated string
        
        # Render the suggestions to the farmer
        return render(request, 'Farmer/SuggestedProducts.html', {'suggestions': suggestions})

    else:
        return redirect('Guest:login')  

#swap_product
def swap_products(request):
    if 'fid' in request.session:
        # Fetch the current farmer's stock
        farmer = tbl_farmer.objects.get(id=request.session['fid'])
        current_stock = tbl_farmerproduct.objects.filter(farmer=farmer)

        # Get the current farmer's products
        farmer_products = tbl_farmerproduct.objects.filter(farmer=farmer).values_list('product__product_name', flat=True)
        farmer_products_set = set(farmer_products)

        # Debugging: Check the farmer's products
        print("Farmer's Products:", farmer_products_set)

        # Fetch matching association rules based on the farmer's current products
        matching_rules = tbl_productrule.objects.filter(
            antecedents__iregex=r'(' + '|'.join(farmer_products_set) + ')'
        ).order_by('-confidence')  # Order by confidence to prioritize stronger rules

        # Debugging: Check the matching rules
        print("Matching Rules:", matching_rules)

        # Prepare the context
        context = {
            'current_stock': current_stock,
            'rules': matching_rules,
            'farmer_products': farmer_products_set,
        }

        if request.method == "POST":
            # Get the selected products to swap from the POST request
            selected_product_id = request.POST.get("selected_product")
            swap_quantity = int(request.POST.get("swap_quantity"))

            # Find the selected product in the farmer's stock
            selected_product = tbl_farmerproduct.objects.get(id=selected_product_id)

            # Check if the farmer has enough stock to swap
            if selected_product.farmerproduct_stock >= swap_quantity:
                # Update the farmer's stock by reducing the stock of the selected product
                selected_product.farmerproduct_stock -= swap_quantity
                selected_product.save()

                # Find or create the product the farmer wants to swap with
                swap_product = tbl_product.objects.get(id=selected_product.product_id)

                # Add the swapped product to the farmer's stock
                tbl_farmerproduct.objects.create(
                    farmer=farmer,
                    product=swap_product,
                    farmerproduct_stock=swap_quantity
                )

                # Redirect to a page where the farmer can see the updated stock (Optional)
                return redirect('Farmer:viewproduct')  # Change this to the appropriate URL

        # Render the template with current stock and suggested swap products
        return render(request, 'Farmer/SwapProducts.html', context)
    else:
        return redirect('Guest:login')  

#----------------------------------------------------------------------------------------------------------------
#apriori algorithm



def find_frequent_swaps(request):
    if 'fid' in request.session:
        # Fetch swap history
        swaps = list(tbl_request.objects.values_list('send_product_id', 'receive_product_id'))
        tbldata=tbl_frequent_swaps.objects.all()

        if not swaps:
            return render(request, 'Farmer/swap_results.html', {'rules': None})

        # Convert to DataFrame
        df = pd.DataFrame(swaps, columns=['send_product_id', 'receive_product_id'])

        # Fetch product names
        product_map = {p.id: p.product_name for p in tbl_product.objects.all()}  

        # Replace Product IDs with Names
        df['send_product_name'] = df['send_product_id'].map(product_map)
        df['receive_product_name'] = df['receive_product_id'].map(product_map)

        # Remove rows with missing mappings
        df.dropna(subset=['send_product_name', 'receive_product_name'], inplace=True)

        # Transform data into a transaction format
        transactions = df.groupby(['send_product_name', 'receive_product_name']).size().unstack(fill_value=0)

        # Apply Apriori Algorithm
        frequent_itemsets = apriori(transactions.astype(bool), min_support=0.2, use_colnames=True)

        # Get association rules
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

        # Convert frozensets safely
        rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x))
        rules['consequents'] = rules['consequents'].apply(lambda x: list(x))

        # Store frequent swaps in the database
        tbl_frequent_swaps.objects.all().delete()  # Clear previous data

        for _, row in rules.iterrows():
            for antecedent_name in row['antecedents']:
                for consequent_name in row['consequents']:
                    # Get product instances
                    antecedent_product = tbl_product.objects.filter(product_name=antecedent_name).first()
                    consequent_product = tbl_product.objects.filter(product_name=consequent_name).first()

                    if antecedent_product and consequent_product:
                        tbl_frequent_swaps.objects.create(
                            antecedent=antecedent_product,
                            consequent=consequent_product,
                            support=row['support'],
                            confidence=row['confidence'],
                            lift=row['lift'],
                            keyword="Frequent"
                        )

        return render(request, 'Farmer/Apriori.html', {'rules': rules.to_html(classes="table table-striped") if not rules.empty else None,'data':tbldata})
    else:
        return redirect('Guest:login')  


# View to render frequent swaps page
def frequent_swaps_view(request):
    if 'fid' in request.session:
        rules = find_frequent_swaps()
        return render(request, 'Farmer/Apriori.html', {'rules': rules.to_html() if rules is not None else None})
    else:
        return redirect('Guest:login')  

#suggection-------------------------------------------------------------------


def suggections(request):
    if 'fid' in request.session:
        loginfarmerid = request.session.get('fid')  # Get logged-in farmer ID
        if not loginfarmerid:
            return render(request, 'Farmer/suggested_items.html', {'data': []})  # No data if not logged in

        # Filter requests for the logged-in farmer
        frequent_requests = (
            tbl_request.objects
            .filter(send_farmer=loginfarmerid)  # Only fetch requests for the logged-in farmer
            .values('send_farmer', 'send_product')
            .annotate(request_count=Count('id'))
            .filter(request_count__gt=1)  # Only if requested more than once
        )

        suggested_items = defaultdict(list)
        enriched_data = []

        for req in frequent_requests:
            farmer_id = req['send_farmer']
            product_id = req['send_product']

            # Fetch related names
            farmer_name = tbl_farmer.objects.get(id=farmer_id).farmer_name
            product_name = tbl_product.objects.get(id=product_id).product_name

            # Store enriched data
            enriched_data.append({
                'farmer_id': farmer_id,
                'farmer_name': farmer_name,
                'product_id': product_id,
                'product_name': product_name,
            })

            suggested_items[farmer_id].append(product_name)

        return render(request, 'Farmer/suggested_items.html', {
            'suggested_items': dict(suggested_items),
            'data': enriched_data
        })
    else:
        return redirect('Guest:login')  



import io
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import tbl_request, tbl_product

def plot_swap_trends(request):
    if 'fid' in request.session:
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
    if 'fid' in request.session:
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






#-----------------------------------------------------------------------------------------------------------------
#disease



class_names = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
    'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 
    'Tomato___healthy'
]

def predict_image(request):
    predicted_class = "No prediction made"

    if request.method == "POST" and request.FILES.get("image"):
        uploaded_image = request.FILES["image"]
        try:
            # Read and preprocess the image
            from PIL import Image
            img = Image.open(uploaded_image)
            img = img.resize((224, 224))  # Resize image to match model input
            img_array = img_to_array(img)  # Convert to array
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            img_array = preprocess_input(img_array)  # Preprocess for the model
            img_array /= 255.0
            # Make prediction
            predictions = model.predict(img_array)
            pred_index = np.argmax(predictions)
            confidence = float(np.max(predictions))  # Confidence score

            confidence_threshold = 0.70  # Set confidence threshold (50%)
            
            if confidence >= confidence_threshold:
                predicted_class = class_names[pred_index]
                return render(
                request, 
                "Farmer/Predict.html", 
                {"prediction": predicted_class, "confidence": f"{confidence:.2%}"}
            )
            else:
                predicted_class = "No disease detected"
                return render(
                request, 
                "Farmer/Predict.html", 
                {"prediction": predicted_class}
            )

            # predicted_class = class_names[pred_index]
            # print(predictions)
            # Render the result
            # return render(
            #     request, 
            #     "Farmer/Predict.html", 
            #     {"prediction": predicted_class, "confidence": f"{confidence:.2%}"}
            # )
        except Exception as e:
            return render(
                request, 
                "Farmer/Predict.html", 
                {"error": f"An error occurred: {str(e)}"}
            )
    else:
        return render(request, "Farmer/Predict.html")

def logout(request):
    if 'fid' in request.session:
        del request.session["fid"]
        return redirect("Guest:login")
    else:
        return redirect("Guest:login")
    
