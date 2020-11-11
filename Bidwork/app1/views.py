from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from sellers.models import Items, Biddings
from buyers.models import Items_B, Biddings_B, Buyers_B


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
from decimal import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import datetime


def home(request):
	return render(request,'app1/home.html')

def aboutus(request):
	return render(request,'app1/aboutus.html')

def seller(request):
	sellers1 = Items.objects.all()
	for seller in sellers1:
		if (seller.End_Date - seller.Start_Date) != datetime.timedelta(0):
			seller.Current_price = float(seller.Max_Price) - ((float(seller.Max_Price)+ float(seller.Min_Price))*((timezone.now() - seller.Start_Date))/((seller.End_Date - seller.Start_Date)))
			if seller.Current_price < float(seller.Min_Price):
				seller.Current_price = float(seller.Min_Price)
			elif seller.Current_price > float(seller.Max_Price): 
				seller.Current_price = float(seller.Max_Price)
		else:
			seller.Current_price = float(seller.Max_Price)

		Biddings = Biddings_B.objects.filter(Item_Id=seller.id)
		if Biddings.count() == 0:
			seller.Remaining_Hours = seller.Total_Availibility
		remaining_time = seller.Total_Availibility
		for bids in Biddings:
				remaining_time = remaining_time - bids.Hours
		seller.Remaining_Hours = remaining_time

		seller.Week_Start_Date = setWeekStartDay(seller.Week_Number).strftime("%Y-%m-%d")
		seller.Start_Date = seller.Start_Date.strftime("%Y-%m-%d")
		seller.End_Date = seller.End_Date.strftime("%Y-%m-%d")

		biddings1 = Biddings_B.objects.all()
		for bidding in biddings1:
			bidding.Bidding_Date = bidding.Bidding_Date.strftime("%Y-%m-%d")


	return render(request,'app1/seller.html',{'buyers':biddings1, 'sellers' : sellers1})

def deleteSeller(request,sellerID):
	seller=Items.objects.get(id=sellerID)
	seller.delete()
	messages.error(request, "Deleted Successfully")
	return HttpResponseRedirect("/seller")

def newSeller(request):
	newseller1=Items()
	newseller1.save()
	messages.success(request, "Added Successfully")
	return HttpResponseRedirect("/seller")

def setWeekStartDay(Week_Number):
	start_date = "12/29/19"	
	date_1 = datetime.datetime.strptime(start_date, "%m/%d/%y")
	offset = ((Week_Number-1) * 7)
	date2 = date_1 + datetime.timedelta(days = int(offset))
	return date2

def buyer(request):
	sellers1 = Items.objects.all()
	
	for seller in sellers1:
		if (seller.End_Date - seller.Start_Date) != datetime.timedelta(0):
			seller.Price = float(seller.Max_Price) - ((float(seller.Max_Price)+ float(seller.Min_Price))*((timezone.now() - seller.Start_Date))/((seller.End_Date - seller.Start_Date)))
			if seller.Price < float(seller.Min_Price):
				seller.Price = float(seller.Min_Price)
			elif seller.Price > float(seller.Max_Price): 
				seller.Price = float(seller.Max_Price)
		else:
			seller.Price = float(seller.Max_Price)
		seller.Week_Start_Date = setWeekStartDay(seller.Week_Number).strftime("%Y-%m-%d")
		seller.Start_Date = seller.Start_Date.strftime("%Y-%m-%d")
		seller.End_Date = seller.End_Date.strftime("%Y-%m-%d")
		Biddings = Biddings_B.objects.filter(Item_Id=seller.id)
		if Biddings.count() == 0:
			seller.Remaining_Hours = seller.Total_Availibility
		remaining_time = seller.Total_Availibility
		for bids in Biddings:
				remaining_time = remaining_time - bids.Hours
		seller.Remaining_Hours = remaining_time
	myBids = Biddings_B.objects.filter(Buyer_Id = request.user.id)
	for bids in myBids:
		bids.Bidding_Date = bids.Bidding_Date.strftime("%Y-%m-%d")
		bids.Week_Start_Date = setWeekStartDay(bids.Week_Number).strftime("%Y-%m-%d")
	return render(request,'app1/buyer.html',{'buyers': myBids,'sellers':sellers1})

def deleteBuyer(request,buyerID):
	buyer=Biddings_B.objects.get(id=buyerID)
	buyer.delete()
	messages.error(request, "Deleted Successfully")
	return HttpResponseRedirect("/buyer")

def newBuyer(request):
	newbuyer=Biddings_B()
	newbuyer.save()
	messages.success(request, "Added Successfully")
	HttpResponseRedirect("/buyer")	
	return newbuyer.id