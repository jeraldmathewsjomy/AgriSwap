
from django.urls import path
from Customer import views
app_name="Customer"



urlpatterns = [
    path('Dashboard/',views.dashboard,name='dashboard'),
    path('Myprofile/',views.myprofile,name='myprofile'),
    path('Editprofile/',views.editprofile,name='editprofile'),
    path('Changepassword/',views.changepassword,name='changepassword'),
    path('Viewproduct/',views.viewproduct,name='Viewproduct'),
    path('Complaint/',views.complaint,name='complaint'),
    path('mycomplaints/',views.mycomplaints,name='mycomplaints'),
    path('delcomp/<int:id>',views.delcomp,name='delcomp'),

    path('mybooking/',views.mybooking,name='mybooking'),
    path('Addcart/<int:pid>',views.Addcart, name='Addcart'),   
    path('Mycart/',views.Mycart, name='Mycart'),   
    path("DelCart/<int:did>", views.DelCart,name="delcart"),
    path("CartQty/", views.CartQty,name="cartqty"),
    path("productpayment/", views.productpayment,name="productpayment"),
    path("mybooking/", views.mybooking,name="mybooking"),
    path("reproductpayment/<int:id>", views.reproductpayment,name="reproductpayment"),

    path('loader/',views.loader, name='loader'),
    path('paymentsuc/',views.paymentsuc, name='paymentsuc'),

    path("myproducts/<int:id>", views.myproducts,name="myproducts"),
    path('logout/',views.logout,name="logout"),
]
