
from django.urls import path
from Basic import views


urlpatterns = [
    
    path('Sum/',views.sum,name="name"),
    path('largest/',views.large,name="this")
]
