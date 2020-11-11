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
	TimeZone_Offset = -5
	Current_DateTime=datetime.datetime.now()+datetime.timedelta(hours = TimeZone_Offset)

	sellersObjects = Items.objects.all()
	Bids = Biddings_B.objects.all()
	if(sellersObjects.count()>0):
		for seller in sellersObjects:

			Bid_ElapsedTime=Current_DateTime- seller.Start_Date
			Bid_Horizon=seller.End_Date- seller.Start_Date
			Bid_Horizon=int(Bid_Horizon.total_seconds()/3600)
			Bid_ElapsedTime=int(Bid_ElapsedTime.total_seconds()/3600)

			if(Bid_ElapsedTime<=0):
				seller.Current_price=seller.Max_Price
			else:
				Current_Price_Slope =(float(seller.Max_Price)- float(seller.Min_Price))*float(Bid_ElapsedTime/Bid_Horizon)
				seller.Current_price=round(float(seller.Max_Price)-Current_Price_Slope,2)


			Biddings = Biddings_B.objects.filter(Item_Id=seller.id)
			if Biddings.count() == 0:
				seller.Remaining_Hours = seller.Total_Availibility
			remaining_time = seller.Total_Availibility
			for bids in Biddings:
				remaining_time = remaining_time - bids.Hours
			seller.Remaining_Hours = remaining_time

			seller.Week_Start_Date = setWeekStartDay(seller.Week_Number).strftime("%Y-%m-%d")
			seller.Start_Date = seller.Start_Date.strftime("%Y-%m-%d %H:%M")
			seller.End_Date = seller.End_Date.strftime("%Y-%m-%d %H:%M")

			for Bid in Bids:
				Bid.Bidding_Date = Bid.Bidding_Date.strftime("%Y-%m-%d %H:%M")


	return render(request,'app1/seller.html',{'buyers':Bids, 'sellers' : sellersObjects})

def deleteSeller(request,sellerID):
	seller=Items.objects.get(id=sellerID)
	seller.delete()
	messages.error(request, "Deleted Successfully")
	return HttpResponseRedirect("/seller")

def newSeller(request):
	newSeller=Items()
	sellers = Items.objects.all()
	Max_Week=0
	if(sellers.count()>0):
		for seller in sellers:
			if(seller.Week_Number>Max_Week):
				Max_Week=seller.Week_Number
	if (Max_Week+1>53):
		Max_Week=0
	
	newSeller.Week_Number=Max_Week+1
	newSeller.Start_Date=setWeekStartDay(newSeller.Week_Number-2)
	newSeller.End_Date=setWeekStartDay(newSeller.Week_Number-1)
	newSeller.save()
	messages.success(request, "Added Successfully")
	return HttpResponseRedirect("/seller")

def setWeekStartDay(Week_Number):
	start_date = "2019-12-29"	
	date_1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
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