from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from sellers.models import Seller


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