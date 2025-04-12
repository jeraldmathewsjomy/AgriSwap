
from django.urls import path
from Guest import views

app_name="Guest"

urlpatterns = [
    path('Customer/',views.customer,name="customer"),
    path('Farmer/',views.farmer,name="farmer"),
    path('ajaxplace/',views.ajaxplace,name='ajaxplace'),
    path('Login/',views.login,name='login'),
    path('',views.index,name='index'),
    
]
