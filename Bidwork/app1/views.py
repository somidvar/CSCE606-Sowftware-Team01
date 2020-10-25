from django.shortcuts import render
from django.http import HttpResponse

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from sellers.models import Seller


def home(request):
	return render(request,'app1/home.html')

def aboutus(request):
	return render(request,'app1/aboutus.html')

def seller(request):
	context={
	'sellers':Seller.objects.all()
	}
	return render(request,'app1/seller.html',context)
