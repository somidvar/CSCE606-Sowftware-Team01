from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from sellers.models import Items, Biddings
from buyers.models import  Items_B, Biddings_B
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from app1 import views
from decimal import *
import datetime
from django.contrib.auth.models import User
from users.models import Profile

@csrf_exempt
def saveSell(request):
	id=request.POST.get('id','')
	currentSell=Items.objects.get(id=id)
	sellers=Items.objects.all()

	Week_Number_Str=request.POST.get('Week_Number','')
	Min_Price_Str=request.POST.get('Min_Price','')
	Max_Price_Str=request.POST.get('Max_Price','')
	Total_Availibility_Str=request.POST.get('Total_Availibility','')
	End_Date_Str=request.POST.get('End_Date','')
	Start_Date_Str=request.POST.get('Start_Date','')

	#Week Number validation
	try:
		Week_Number=int(Week_Number_Str)
	except Exception as e:
		messages.error(request, "The week number should be an integer")
		return JsonResponse({"error":"validation"})

	#Min Price validation
	try:
		Min_Price=float(Min_Price_Str)
	except Exception as e:
		messages.error(request, "The min price should be a float")
		return JsonResponse({"error":"validation"})

	#Max Price validation
	try:
		Max_Price=Decimal(Max_Price_Str)
	except Exception as e:
		messages.error(request, "The max price should be a float")
		return JsonResponse({"error":"validation"})

	#Total availibility validation
	try:
		Total_Availibility=int(Total_Availibility_Str)
	except Exception as e:
		messages.error(request, "The total availibility should be an integer")
		return JsonResponse({"error":"validation"})
	
	#start date validation
	try:
		Start_Date=datetime.datetime.strptime(Start_Date_Str, "%Y-%m-%d %H:%M")
	except Exception as e:
		messages.error(request, "The start date should be in Year-Month-Day Hour:Minute")
		return JsonResponse({"error":"validation"})

	#end date validation
	try:
		End_Date=datetime.datetime.strptime(End_Date_Str, "%Y-%m-%d %H:%M")
	except Exception as e:
		messages.error(request, "The end date should be in Year-Month-Day Hour:Minute")
		return JsonResponse({"error":"validation"})

	if (Week_Number<=0):
		messages.error(request, "The week number should be positive")
		return JsonResponse({"error":"validation"})

	#Week_Number validation
	for seller in sellers:
		if(Week_Number==seller.Week_Number and seller.id!=currentSell.id):
			messages.error(request, "Week number should be unique")
			return JsonResponse({"error":"validation"})

	#min and max price validation
	if(Min_Price<0 or Max_Price<0):
		messages.error(request, "Prices cannot be negative")
		return JsonResponse({"error":"validation"})
	if(Max_Price<Min_Price):
		messages.error(request, "Min price should be smaller than max")
		return JsonResponse({"error":"validation"})

	#Checking to make sure that the update does not go under what it is already bidded
	bids=Biddings.objects.filter(Item_Id=currentSell.id)
	totalBidHour=0
	for bid in bids:
		totalBidHour=totalBidHour+bid.Hours
	if(Total_Availibility<totalBidHour):
		messages.error(request, ("The total availibility should be greater than currently bidded of "+str(totalBidHour)+" hours"))
		return JsonResponse({"error":"validation"})		

	#total availibility validation
	if(Total_Availibility<0):
		messages.error(request, "The total availibility should be between 0 and 168 hours")
		return JsonResponse({"error":"validation"})	


	Week_Start_Date=setWeekStartDay(Week_Number)
	#start/end date comparison validation
	if(Start_Date>=End_Date):
		messages.error(request, "The end date should be later than start date")
		return JsonResponse({"error":"validation"})	
	
	#bidding execution and week_Number comparison validation
	if(Week_Start_Date<End_Date):
		messages.error(request, "The bidding should be executed before the start date of the work")
		return JsonResponse({"error":"validation"})	

	currentSell.Week_Number=Week_Number
	currentSell.Start_Date=Start_Date
	currentSell.End_Date=End_Date
	currentSell.Min_Price=Min_Price
	currentSell.Max_Price=Max_Price
	currentSell.Total_Availibility=Total_Availibility
	currentSell.Remaining_Availibility = Total_Availibility
	bids=Biddings.objects.filter(Item_Id=currentSell.id)
	for bid in bids:
		currentSell.Remaining_Availibility=currentSell.Total_Availibility-bid.Hours
	currentSell.save()
	messages.success(request, "The week details is updated successfully")
	return JsonResponse({"success":"Updated"})

@csrf_exempt
def saveBid(request):
	id=request.POST.get('id','')
	new_id = views.newBid(request)
	bid=Biddings_B.objects.get(id=new_id)
	bid.Bidding_Date=request.POST.get('Bidding_Date','')#datetime.strptime
	bid.Week_Number=int(request.POST.get('Week_Number',''))
	bid.Buyer_Id = request.user.id
	bid.Price = Decimal(request.POST.get('Price', ''))
	bid.Item_Id = request.POST.get('id','')

	try:
		hoursTemp=Decimal(request.POST.get('Bid_Hours',''))
	except Exception as e:
		bid.delete()
		messages.error(request, "The bid hours is not in correct format")
		return JsonResponse({"error":"The bid hours is not in correct format"})

	if(hoursTemp<=0):
		bid.delete()
		messages.error(request, "The bid hours should be bigger than 0")
		return JsonResponse({"error":"The bid hours should be bigger than 0"})		
	if(int(hoursTemp)!=hoursTemp):
		bid.delete()
		messages.error(request, "The bid hours should be integer")
		return JsonResponse({"error":"The bid hours should be integer"})


	bid.Hours=int(hoursTemp)
	sell = Items_B.objects.get(id=id)
	if(bid.Hours>sell.Remaining_Availibility):
		bid.delete()
		messages.error(request, "The bid hours is higher than availability")
		return JsonResponse({"error":"The bid hours is higher than availability"})

	bid.save()

	UserTemp=User.objects.get(id=request.user.id)
	User_Profile= Profile.objects.get(user=UserTemp)
	Current_User_Budget=round(User_Profile.budget,2)

	if(Current_User_Budget<bid.Price*Decimal(bid.Hours)):
		bid.delete()
		messages.error(request, "Not enough budget")
		return JsonResponse({"error":"Not enough budget"})	
	else:
		sell=Items_B.objects.get(id=id)
		sell.Remaining_Availibility=sell.Remaining_Availibility-bid.Hours

		sell.save()

		User_Profile.spent=User_Profile.budget+bid.Price*bid.Hours
		User_Profile.budget=Current_User_Budget-bid.Price*bid.Hours
		User_Profile.save()
		UserTemp.save()
		messages.success(request, "The bid is placed successfully")
		return JsonResponse({"success":"Updated"})	

@csrf_exempt
def setWeekStartDay(Week_Number):
	start_date = "12/29/19"	
	date_1 = datetime.datetime.strptime(start_date, "%m/%d/%y")
	offset = ((Week_Number-1) * 7)
	date2 = date_1 + datetime.timedelta(days = int(offset))
	return date2