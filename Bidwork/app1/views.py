from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone

import os, sys, json
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from sellers.models import Items, Biddings
from buyers.models import Items_B, Biddings_B
from users.models import Profile

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
from MyTimeFunctions import *
from django.shortcuts import redirect


def home(request):
	return render(request,'app1/home.html')

def userSchedule(request):
	if (request.user.is_staff):
		return redirect(seller)
	else:
		return redirect(buyer)


def aboutus(request):
	return render(request,'app1/aboutus.html')

@login_required
def seller(request):
	Buyer_Profile_Instantiating()

	sells = Items.objects.order_by('-Week_Number')
	sellsDetails=[]
	if(sells.count()>0):
		for sell in sells:
			sellEditable=1
			Bid_ElapsedTime=MyCurrentTime()- sell.Start_Date
			Bid_Horizon=sell.End_Date- sell.Start_Date
			Bid_Horizon=int(Bid_Horizon.total_seconds()/3600)
			Bid_ElapsedTime=int(Bid_ElapsedTime.total_seconds()/3600)
			if(sell.End_Date<MyCurrentTime()):
				sell.Current_price=sell.Min_Price
			else:
				if(Bid_ElapsedTime<=0):
					sell.Current_price=sell.Max_Price
				else:
					Current_Price_Slope =(float(sell.Max_Price)- float(sell.Min_Price))*float(Bid_ElapsedTime/Bid_Horizon)
					sell.Current_price=round(float(sell.Max_Price)-Current_Price_Slope,2)

			bids = Biddings.objects.filter(Item_Id=sell.id)
			if bids.count() == 0:
				sell.Remaining_Hours = sell.Total_Availibility
			remaining_time = sell.Total_Availibility

			for bid in bids:
				remaining_time = remaining_time - bid.Hours
			sell.Remaining_Availibility = remaining_time

			if(bids.count()>0):
				sellEditableFlag=0
				editableSellStyle="color:#00688B;text-decoration: underline;"
				editableSellClass=""
			else:
				sellEditableFlag=1
				editableSellStyle="color:#00688B;text-decoration: underline;"
				editableSellClass="editable"

			if(sell.End_Date<MyCurrentTime()):
				editableSellStyle=editableSellStyle+"background-color: #EBEBE4"
				readonlySellStyle="background-color: #EBEBE4"
			else:
				editableSellStyle=editableSellStyle+"background-color: #FFFFFF"
				readonlySellStyle="background-color: #FFFFFF"

			sell.Week_Start_Date = setWeekStartDay(sell.Week_Number).strftime("%Y-%m-%d")
			sell.Start_Date = sell.Start_Date.strftime("%Y-%m-%d %H:%M")
			sell.End_Date = sell.End_Date.strftime("%Y-%m-%d %H:%M")
			sell.Post_Date=sell.Post_Date.strftime("%Y-%m-%d %H:%M")

			sellsDetails.append([str(sell.id),str(sell.Week_Number),str(sell.Week_Start_Date),str(sell.Start_Date)
				,str(sell.End_Date),str(sell.Min_Price),str(sell.Max_Price),str(sell.Current_price),str(sell.Total_Availibility)
				,str(sell.Remaining_Availibility),str(sell.Post_Date),str(sellEditableFlag),str(editableSellStyle),str(editableSellClass)
				,str(readonlySellStyle)])

	bids = Biddings.objects.order_by('-Week_Number')
	bidDetails =[]
	for bid in bids:
		UserTemp=User.objects.get(id=bid.Buyer_Id)
		if(MyCurrentTime()<setWeekStartDay(bid.Week_Number)):
			bidEnableStyle="background-color: #FFFFFF"#active bids
		else:
			bidEnableStyle="background-color: #EBEBE4"#past bids
		bid.Bidding_Date = bid.Bidding_Date.strftime("%Y-%m-%d %H:%M")
		bidDetails.append([str(bid.id),str(bid.Week_Number),str(UserTemp.username), str(bid.Price),str(bid.Hours),str(bid.Hours*bid.Price),str(bid.Bidding_Date),str(bidEnableStyle)])

	UserTemp=User.objects.get(id=request.user.id)
	return render(request,'app1/seller.html',{'bidsObjects':bidDetails, 'sellsObjects' : sellsDetails,'currentUser':UserTemp})

def deleteSell(request,sellID):
	sell=Items.objects.get(id=sellID)
	bids = Biddings.objects.filter(Item_Id=sell.id)
	for bid in bids:
		UserTemp=User.objects.get(id=bid.Buyer_Id)
		User_Profile= Profile.objects.get(user=UserTemp)
		User_Profile.budget=User_Profile.budget+bid.Price*bid.Hours
		User_Profile.save()
		UserTemp.save()
		bid.delete()

	sell.delete()
	messages.error(request, "Deleted Successfully")
	return HttpResponseRedirect("/seller")

def newSell(request):
	newSell=Items()
	sells = Items.objects.all()
	Max_Week=1
	if(sells.count()>0):
		for sell in sells:
			if(sell.Week_Number>=Max_Week):
				Max_Week=sell.Week_Number+1

	if (Max_Week+1>53):
		availableWeek=[]
		for counter in range(1,54):
			availableWeek.append(counter)
		for sell in sells:
			if(availableWeek.count(sell.Week_Number)>0):
				availableWeek.remove(sell.Week_Number)
		if(len(availableWeek)>0):
			Max_Week=availableWeek.pop(0)
		else:
			Max_Week=1

	newSell.Week_Number=Max_Week
	newSell.Min_Price=10
	newSell.Max_Price=50
	newSell.Total_Availibility=40
	newSell.Remaining_Availibility=newSell.Total_Availibility
	newSell.Start_Date=setWeekStartDay(newSell.Week_Number-2)
	newSell.End_Date=setWeekStartDay(newSell.Week_Number-1)
	newSell.Post_Date=MyCurrentTime()
	newSell.save()
	messages.success(request, "Added Successfully")
	return HttpResponseRedirect("/seller")

@login_required
def buyer(request):
	Buyer_Profile_Instantiating()

	sells = Items_B.objects.order_by('-Week_Number')
	sellsDetails=[]
	if(sells.count()>0):
		for sell in sells:
			Bid_ElapsedTime=MyCurrentTime()- sell.Start_Date
			Bid_Horizon=sell.End_Date- sell.Start_Date
			Bid_Horizon=int(Bid_Horizon.total_seconds()/3600)
			Bid_ElapsedTime=int(Bid_ElapsedTime.total_seconds()/3600)
			if(sell.End_Date<MyCurrentTime()):
				sell.Current_price=sell.Min_Price
			else:
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
			
			if(MyCurrentTime()<sell.End_Date):
				sellEnableFlag=1#active sells
				sellEnableStyle="background-color: #FFFFFF"
			else:
				sellEnableFlag=0#past sells
				sellEnableStyle="background-color: #EBEBE4"

			sell.Week_Start_Date = setWeekStartDay(sell.Week_Number).strftime("%Y-%m-%d")
			sell.Start_Date = sell.Start_Date.strftime("%Y-%m-%d %H:%M")
			sell.End_Date = sell.End_Date.strftime("%Y-%m-%d %H:%M")
			sell.Post_Date=sell.Post_Date.strftime("%Y-%m-%d %H:%M")

			sellsDetails.append([str(sell.id),str(sell.Week_Number),str(sell.Week_Start_Date),str(sell.Start_Date),str(sell.End_Date)
				,str(sell.Current_price),str(sell.Remaining_Availibility),str(sell.Post_Date),str(sellEnableFlag),str(sellEnableStyle)])

	UserTemp=User.objects.get(id=request.user.id)
	User_Profile= Profile.objects.get(user=UserTemp)
	Current_User_Budget=round(User_Profile.budget,2)

	bids = Biddings_B.objects.filter(Buyer_Id=request.user.id).order_by('-Week_Number')
	for bid in bids:
		bid.Bidding_Date=bid.Bidding_Date.strftime("%Y-%m-%d %H:%M")
		bid.Week_Start_Date = setWeekStartDay(bid.Week_Number).strftime("%Y-%m-%d")


	bidDetails =[]
	for bid in bids:
		if(MyCurrentTime()<setWeekStartDay(bid.Week_Number)):
			bidEnableStyle="background-color: #FFFFFF"#active bids
		else:
			bidEnableStyle="background-color: #EBEBE4"#past bids
		bidDetails.append([str(bid.id),str(bid.Week_Number), str(bid.Price),str(bid.Hours),str(bid.Hours*bid.Price),str(bid.Bidding_Date),str(bidEnableStyle)])

	return render(request,'app1/buyer.html',{'bidsObjects': bidDetails,'sellsObjects':sellsDetails,'budget':Current_User_Budget,'currentUser':UserTemp})

def deleteBid(request,bidID):
	bid=Biddings_B.objects.get(id=bidID)
	bid.delete()
	messages.error(request, "Deleted Successfully")
	return HttpResponseRedirect("/buyer")

def newBid(request):
	newBid=Biddings_B()
	newBid.Hours=0
	newBid.save()
	return newBid.id

def Buyer_Profile_Instantiating():
	Users=User.objects.all()
	#Initializing the user profile
	for user in Users:
		User_Profile,Created_Flag = Profile.objects.get_or_create(user=user)