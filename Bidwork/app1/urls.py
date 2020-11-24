from django.urls import path
from . import views,apiViews

urlpatterns = [
    path('', views.userSchedule,name='app1-userSchedule'),
    path('home', views.home,name='app1-home'),
    path('aboutus', views.aboutus,name='app1-aboutus'),

    path('seller', views.seller,name='app1-seller'),
    path('saveSell', apiViews.saveSell, name='saveSell'),
    path('deleteSell/<str:sellID>', views.deleteSell, name="deleteSell"),
    path('newSell', views.newSell, name='newSell'),

    path('buyer', views.buyer,name='app1-buyer'),
    path('saveBid', apiViews.saveBid, name='saveBid'),
    path('deleteBid/<str:bidID>', views.deleteBid, name="deleteBid"),
    path('newBid', views.newBid, name='newBid'),
]
