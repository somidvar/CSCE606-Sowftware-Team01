from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from sellers.models import Items, Biddings
from buyers.models import  Items_B, Biddings_B, Buyers_B
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from app1 import views

@csrf_exempt
def saveSeller(request):
	id=request.POST.get('id','')
	seller=Items.objects.get(id=id)
	
	seller.Week_Number=request.POST.get('Week_Number','')
	seller.Start_Date=request.POST.get('Start_Date','')
	seller.End_Date=request.POST.get('End_Date','')
	seller.Min_Price=request.POST.get('Min_Price','')
	seller.Max_Price=request.POST.get('Max_Price','')
	seller.Total_Availibility=request.POST.get('Total_Availibility','')
	#seller.Buyer_Id=request.POST.get('Buyer_Id','')
	seller.save()
	
	return JsonResponse({"success":"Updated"})


@csrf_exempt
def saveBuyer(request):
	
	id=request.POST.get('id','')
	new_id = views.newBuyer(request)
	buyer=Biddings_B.objects.get(id=new_id)
	#if(buyer.Buyer_Id != request.user.id):
	#	new_id=views.newBuyer(request)
	#else:
	#	new_id=id
	#buyer=Biddings_B.objects.get(id=new_id)
	buyer.Week_Number=request.POST.get('Week_Number','')
	buyer.Week_Start_Date=request.POST.get('Week_Start_Date','')
	buyer.Price = request.POST.get('Price', '')
	buyer.Buyer_Id=request.POST.get('Week_Number','')
	buyer.Remaining_Hours=request.POST.get('Remaining_Hours','')
	#buyer.Bid_Start_Date=request.POST.get('Bid_Start_Date','')
	buyer.Bidding_Date=request.POST.get('Bidding_Date','')
	buyer.Hours=request.POST.get('Bid_Hours','')
	buyer.Buyer_Id = request.user.id
	buyer.Item_Id = request.POST.get('id','')
	buyer.save()
	
	return JsonResponse({"success":"Updated"})	
