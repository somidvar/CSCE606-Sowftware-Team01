from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from sellers.models import Seller
from buyers.models import Buyer
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse


@csrf_exempt
def saveSeller(request):
	id=request.POST.get('id','')
	seller=Seller.objects.get(id=id)
	
	seller.sellerName=request.POST.get('sellerName','')
	seller.weekNumber=request.POST.get('weekNumber','')
	seller.minPrice=request.POST.get('minPrice','')
	seller.maxPrice=request.POST.get('maxPrice','')
	seller.currentPrice=request.POST.get('currentPrice','')
	seller.availabilityHour=request.POST.get('availabilityHour','')
	seller.remainedHour=request.POST.get('remainedHour','')
	seller.horizon=request.POST.get('horizon','')

	seller.save()
	
	return JsonResponse({"success":"Updated"})

@csrf_exempt
def newSeller(request):
	id=request.POST.get('id','')
	newSeller=Seller()
	newSeller.save()
	return JsonResponse({"success":"Updated"})


@csrf_exempt
def saveBuyer(request):
	id=request.POST.get('id','')
	buyer=Buyer.objects.get(id=id)
	
	buyer.buyerName=request.POST.get('sellerName','')
	buyer.weekNumber=request.POST.get('weekNumber','')
	buyer.bidPrice=request.POST.get('bidPrice','')
	buyer.bidHour=request.POST.get('bidHour','')
	buyer.bidAmount=request.POST.get('bidAmount','')
	buyer.remainedBalace=request.POST.get('remainedBalace','')
	buyer.initialBudget=request.POST.get('initialBudget','')

	buyer.save()
	
	return JsonResponse({"success":"Updated"})	