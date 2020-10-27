from django.shortcuts import render
from django.http import HttpResponse

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from sellers.models import Seller
from buyers.models import Buyer


import json

from django.contrib import messages
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa
from io import StringIO, BytesIO
from requests import request
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



def home(request):
	return render(request,'app1/home.html')

def aboutus(request):
	return render(request,'app1/aboutus.html')

def seller(request):
	return render(request,'app1/seller.html',{'sellers':Seller.objects.all()})

def deleteSeller(request,sellerID):
	seller=Seller.objects.get(id=sellerID)
	seller.delete()
	messages.error(request, "Deleted Successfully")
	return HttpResponseRedirect("/seller")

def newSeller(request):
	newseller1=Seller()
	newseller1.save()
	messages.success(request, "Added Successfully")
	return HttpResponseRedirect("/seller")

def buyer(request):
	return render(request,'app1/buyer.html',{'buyers':Buyer.objects.all(),'sellers':Seller.objects.all()})

def deleteBuyer(request,buyerID):
	buyer=Buyer.objects.get(id=buyerID)
	buyer.delete()
	messages.error(request, "Deleted Successfully")
	return HttpResponseRedirect("/buyer")

def newBuyer(request):
	newbuyer=Buyer()
	newbuyer.save()
	messages.success(request, "Added Successfully")
	return HttpResponseRedirect("/buyer")	