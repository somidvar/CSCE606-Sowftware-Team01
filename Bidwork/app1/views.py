from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from MyTimeFunctions import *

from sellers.models import Items, Biddings,Buyers
from buyers.models import Items_B, Biddings_B
from users.models import Profile

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



def home(request):
	return render(request,'app1/home.html')

def aboutus(request):
	return render(request,'app1/aboutus.html')

def seller(request):
	Buyer_Profile_Instantiating()

	sellersObjects = Items.objects.all()
	BidsObjects = Biddings.objects.all()
	if(sellersObjects.count()>0):
		for seller in sellersObjects:
			Bid_ElapsedTime=MyCurrentTime()- seller.Start_Date
			Bid_Horizon=seller.End_Date- seller.Start_Date
			Bid_Horizon=int(Bid_Horizon.total_seconds()/3600)
			Bid_ElapsedTime=int(Bid_ElapsedTime.total_seconds()/3600)

			if(Bid_ElapsedTime<=0):
				seller.Current_price=seller.Max_Price
			else:
				Current_Price_Slope =(float(seller.Max_Price)- float(seller.Min_Price))*float(Bid_ElapsedTime/Bid_Horizon)
				seller.Current_price=round(float(seller.Max_Price)-Current_Price_Slope,2)

			seller.Week_Start_Date = setWeekStartDay(seller.Week_Number).strftime("%Y-%m-%d")
			seller.Start_Date = seller.Start_Date.strftime("%Y-%m-%d %H:%M")
			seller.End_Date = seller.End_Date.strftime("%Y-%m-%d %H:%M")

			Bids = Biddings.objects.filter(Item_Id=seller.id)
			if Bids.count() == 0:
				seller.Remaining_Hours = seller.Total_Availibility
			remaining_time = seller.Total_Availibility
			for Bid in Bids:
				remaining_time = remaining_time - Bid.Hours
				Bid.Bidding_Date = Bid.Bidding_Date.strftime("%Y-%m-%d %H:%M")
			seller.Remaining_Availibility = remaining_time

	return render(request,'app1/seller.html',{'bids':BidsObjects, 'sellers' : sellersObjects})

def deleteSeller(request,sellerID):
	seller=Items.objects.get(id=sellerID)
	Bids = Biddings.objects.filter(Item_Id=seller.id)
	for Bid in Bids:
		UserTemp=User.objects.get(id=Bid.Buyer_Id)
		User_Profile= Profile.objects.get(user=UserTemp)
		User_Profile.budget=User_Profile.budget+Bid.Price*Bid.Hours

	Bids.delete()
	seller.delete()
	messages.error(request, "Deleted Successfully")
	return HttpResponseRedirect("/seller")

def newSeller(request):
	newSeller=Items()
	sellers = Items.objects.all()
	Max_Week=1
	if(sellers.count()>0):
		for seller in sellers:
			if(seller.Week_Number>=Max_Week):
				Max_Week=seller.Week_Number+1
	if (Max_Week+1>53):
		Max_Week=0
	
	newSeller.Week_Number=Max_Week
	newSeller.Total_Availibility=40
	newSeller.Remaining_Availibility=newSeller.Total_Availibility
	newSeller.Start_Date=setWeekStartDay(newSeller.Week_Number-2)
	newSeller.End_Date=setWeekStartDay(newSeller.Week_Number-1)
	newSeller.save()
	messages.success(request, "Added Successfully")
	return HttpResponseRedirect("/seller")

def buyer(request):
	Buyer_Profile_Instantiating()
	sells = Items_B.objects.all()
	
	if(sells.count()>0):
		for sell in sells:
			Bid_ElapsedTime=MyCurrentTime()- sell.Start_Date
			Bid_Horizon=sell.End_Date- sell.Start_Date
			Bid_Horizon=int(Bid_Horizon.total_seconds()/3600)
			Bid_ElapsedTime=int(Bid_ElapsedTime.total_seconds()/3600)

			if(Bid_ElapsedTime<=0):
				sell.Current_price=sell.Max_Price
			else:
				Current_Price_Slope =(float(sell.Max_Price)- float(sell.Min_Price))*float(Bid_ElapsedTime/Bid_Horizon)
				sell.Current_price=round(float(sell.Max_Price)-Current_Price_Slope,2)

			bids = Biddings_B.objects.filter(Item_Id=sell.id)
			sell.Remaining_Hours = sell.Total_Availibility
			for bid in bids:
				bid.Bidding_Date = bid.Bidding_Date.strftime("%Y-%m-%d %H:%M")
				sell.Remaining_Hours = sell.Total_Availibility-bid.Hours

			sell.Week_Start_Date = setWeekStartDay(sell.Week_Number).strftime("%Y-%m-%d")
			sell.Start_Date = sell.Start_Date.strftime("%Y-%m-%d %H:%M")
			sell.End_Date = sell.End_Date.strftime("%Y-%m-%d %H:%M")

	UserTemp=User.objects.get(id=request.user.id)
	User_Profile= Profile.objects.get(user=UserTemp)
	Current_User_Budget=round(User_Profile.budget,2)
	bids = Biddings_B.objects.filter(Buyer_Id=request.user.id)

	for bid in bids:
		bid.Bidding_Date=bid.Bidding_Date.strftime("%Y-%m-%d %H:%M")
		bid.Week_Start_Date = setWeekStartDay(bid.Week_Number).strftime("%Y-%m-%d")

	return render(request,'app1/buyer.html',{'bidsObjects': bids,'sellsObjects':sells,'budget':Current_User_Budget})

def deleteBuyer(request,buyerID):
	buyer=Biddings_B.objects.get(id=buyerID)
	#buyer.delete()
	messages.error(request, "Deleted Successfully")
	return HttpResponseRedirect("/buyer")

def newBuyer(request):
	newbuyer=Biddings_B()
	newbuyer.save()
	messages.success(request, "Added Successfully")
	HttpResponseRedirect("/buyer")	
	return newbuyer.id

def Buyer_Profile_Instantiating():
	Users=User.objects.all()
	#Initializing the user profile
	for user in Users:
		User_Profile,Created_Flag = Profile.objects.get_or_create(user=user)