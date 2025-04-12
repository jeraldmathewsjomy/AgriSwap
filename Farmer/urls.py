
from django.urls import path
from Farmer import views
from .views import find_frequent_swaps
from .views import suggections
from .views import swap_trends_view

app_name="Farmer"



urlpatterns = [

    path('Homepage/',views.Homepage,name='dashboard'),
    path('Myprofile/',views.myprofile,name='myprofile'),
    path('Editprofile/',views.editprofile,name='editprofile'),
    path('Changepassword/',views.changepassword,name='changepassword'),
    path('Viewproduct/',views.viewproduct,name="viewproduct"),
    path('stock/<int:pid>', views.stock, name="stock"),
    path('editstock/<int:id>', views.editstock, name="editstock"),   
    path('myproducts/', views.myproducts, name="myproducts"),
    path('addprice/<int:id>', views.addprice, name="addprice"),

    #exchange section---------------------------------------------------------
    path('exchange/', views.exchange, name="exchange"),  
    path('ajaxcal/', views.ajaxcal, name='ajaxcal'),
    path('Confirmation/', views.confirmation, name='confirmation'),
    path('ajaxsendrequest/', views.ajaxsendrequest, name='ajaxsendrequest'),
    path('Myrequest/', views.myrequest, name='myrequest'),
    path('ViewRequest/', views.viewrequest, name='viewrequest'),
    path('Otherproducts/<int:id>', views.otherproducts, name='otherproducts'),
    path('returnrequest/', views.returnrequest, name='returnrequest'),
    path('rejectrequest/<int:id>', views.rejectrequest, name='rejectrequest'),


    #disease detection--------------------------------------------------------
    path('diseaseai/',views.predict_image,name='diseaseai'),

    #payment------------------------------------------------------------------
    path('requestPayment/<int:id>', views.requestPayment, name='requestPayment'),
    path('loader/',views.loader, name='loader'),
    path('paymentsuc/',views.paymentsuc, name='paymentsuc'),

    #datamining---------------------------------------------------------------
    path('Apriori/',views.find_frequent_swaps,name="Apriori"),
    path('suggections/', suggections, name='suggections'),
    path('swap-trends/', swap_trends_view, name='swap_trends_view'),
    path('logout/', views.logout, name="logout"),
]
