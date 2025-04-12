
from django.urls import path
from Admin import views
from .views import swap_trends_view
app_name="Admin"

urlpatterns = [
    path('District/',views.district,name="district"), 
    path('Dashboard/',views.dashboard,name='dashboard'),


    path('Admin/',views.admino,name="admino"),
    path('deladmin/<int:id>',views.deladmin,name='deladmin'),
    path('editadmin/<int:id>',views.editadmin,name='editadmin'),  #Admin frm html pge nme,admino frm views(def admino)

    
    path('Product/',views.product,name="product"),
    path('delprod/<int:did>',views.delprod,name="delprod"),
    path('Addprice/<int:id>/',views.addprice,name="addprice"),

    path('deleteprice/<int:id>/',views.deleteprice,name="deleteprice"),
    
    


    path('Category/',views.category,name="category"),
    path('Subcategory/',views.subcategory,name="subcategory"),
    path('delsubcategory/<int:id>',views.delsubcategory,name='delsubcategory'),

 
    path('Newfarmer/',views.newfarmer,name='Newfarmer'),
    path('verify/<int:id>',views.verify,name='verify'),
    path('reject/<int:id>',views.reject,name='reject'),
    path('rejectverify/<int:id>',views.rejectverify,name='rejectverify'),
    path('acceptreject/<int:id>',views.acceptreject,name='acceptreject'),
    path('Rejectedfarmer/',views.rejectedfarmer,name='rejectedfarmer'),
    path('Acceptedfarmer/',views.acceptedfarmer,name='acceptedfarmer'),

    path('Newcustomer/',views.newcustomer,name='newcustomer'),
    path('custverify/<int:id>',views.custverify,name='custverify'),
    path('custreject/<int:id>',views.custreject,name='custreject'),
    path('custrejectverify/<int:id>',views.custrejectverify,name='custrejectverify'),
    path('custacceptreject/<int:id>',views.custacceptreject,name='custacceptreject'),
    path('Rejectedcustomer/',views.rejectedcustomer,name='rejectedcustomer'),
    path('Acceptedcustomer/',views.acceptedcustomer,name='acceptedcustomer'),

    path('swap-trends/',swap_trends_view, name='swap_trends_view'),

    path('District/',views.district,name="district"),
    path('Place/',views.place,name="place"),
    path('delpalce/<int:id>',views.delplace,name='delplace'),
    path('viewcomplaint/',views.viewcomplaint,name="viewcomplaint"),
    path('reply/<int:id>',views.reply,name="reply"),
    path('logout/',views.logout,name="logout"),


]
