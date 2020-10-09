from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='app1-home'),
    path('aboutus', views.aboutus,name='app1-aboutus'),
]
