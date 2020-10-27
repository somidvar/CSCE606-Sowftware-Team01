from django.urls import path
from . import views,apiViews

urlpatterns = [
    path('', views.home,name='app1-home'),
    path('aboutus', views.aboutus,name='app1-aboutus'),

    path('seller', views.seller,name='app1-seller'),
    path('saveSeller', apiViews.saveSeller, name='saveSeller'),
    path('deleteSeller/<str:sellerID>', views.deleteSeller, name="deleteSeller"),
    path('newSeller', views.newSeller, name='newSeller'),

    path('buyer', views.buyer,name='app1-buyer'),
    path('saveBuyer', apiViews.saveBuyer, name='saveBuyer'),
    path('deleteBuyer/<str:buyerID>', views.deleteBuyer, name="deleteBuyer"),
    path('newBuyer', views.newBuyer, name='newBuyer'),
]
