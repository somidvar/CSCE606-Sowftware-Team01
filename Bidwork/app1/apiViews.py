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

@csrf_exempt
def saveSeller(request):
	id=request.POST.get('id','')
	currentSeller=Items.objects.get(id=id)
	sellers=Items.objects.all()

	Week_Number=Decimal(request.POST.get('Week_Number',''))
	Min_Price=Decimal(request.POST.get('Min_Price',''))
	Max_Price=Decimal(request.POST.get('Max_Price',''))
	Total_Availibility=Decimal(request.POST.get('Total_Availibility',''))
	End_Date_Str=request.POST.get('End_Date','')
	Start_Date_Str=request.POST.get('Start_Date','')

	#Week_Number validation
	for seller in sellers:
		if(Week_Number==seller.Week_Number and seller.id!=currentSeller.id):
			messages.error(request, "Week number is repeated")
			return JsonResponse({"error":"validation"})
	#min and max price validation
	if(Min_Price<0 or Max_Price<0):
		messages.error(request, "Prices cannot be negative")
		return JsonResponse({"error":"validation"})
	if(Max_Price<Min_Price):
		messages.error(request, "Min price should be bigger than max")
		return JsonResponse({"error":"validation"})
	#total availibility validation
	if(Total_Availibility<0 or Total_Availibility>24*7):
		messages.error(request, "The total availibility should be between 0 and 168 hours")
		return JsonResponse({"error":"validation"})	

	#start date validation
	try:
		Start_Date=datetime.datetime.strptime(Start_Date_Str, "%Y-%m-%d %H:%M")
	except Exception as e:
		print(str(e))
		messages.error(request, "The start date should be in Year-Month-Day Hour:Minute")
		return JsonResponse({"error":"validation"})

	#end date validation
	try:
		End_Date=datetime.datetime.strptime(End_Date_Str, "%Y-%m-%d %H:%M")
	except Exception as e:
		print(str(e))

		messages.error(request, "The end date should be in Year-Month-Day Hour:Minute")
		return JsonResponse({"error":"validation"})

	#week start date validation
	Week_Start_Date=setWeekStartDay(Week_Number)

	#start/end date comparison validation
	if(Start_Date>=End_Date):
		messages.error(request, "The end date should be later than start date")
		return JsonResponse({"error":"validation"})	
	#bidding execution and week_Number comparison validation
	if(Week_Start_Date<End_Date):
		messages.error(request, "The bidding should be executed before the start date of the work")
		return JsonResponse({"error":"validation"})	

	currentSeller.Week_Number=Week_Number
	currentSeller.Start_Date=Start_Date
	currentSeller.End_Date=End_Date
	currentSeller.Min_Price=Min_Price
	currentSeller.Max_Price=Max_Price
	currentSeller.Total_Availibility=Total_Availibility
	currentSeller.Remaining_Availibility = Total_Availibility
	bids=Biddings.objects.filter(Item_Id=currentSeller.id)
	for bid in bids:
		currentSeller.Remaining_Availibility=currentSeller.Total_Availibility-bid.Hours
	currentSeller.save()
	messages.success(request, "Updated")
	return JsonResponse({"success":"Updated"})

@csrf_exempt
def saveBuyer(request):
	id=request.POST.get('id','')
	new_id = views.newBuyer(request)
	bid=Biddings_B.objects.get(id=new_id)
	bid.Bidding_Date=request.POST.get('Bidding_Date','')#datetime.strptime
	bid.Week_Number=int(request.POST.get('Week_Number',''))
	bid.Buyer_Id = request.user.id
	bid.Price = Decimal(request.POST.get('Price', ''))
	bid.Hours=int(request.POST.get('Bid_Hours',''))

	bid.Item_Id = request.POST.get('id','')
	bid.save()
	
	sells=Items_B.objects.filter(id=id)
	for sell in sells:
		sell.Remaining_Availibility=sell.Remaining_Availibility-bid.Hours
	sell.save()
	return JsonResponse({"success":"Updated"})	

@csrf_exempt
def setWeekStartDay(Week_Number):
	start_date = "12/29/19"	
	date_1 = datetime.datetime.strptime(start_date, "%m/%d/%y")
	offset = ((Week_Number-1) * 7)
	date2 = date_1 + datetime.timedelta(days = int(offset))
	return date2