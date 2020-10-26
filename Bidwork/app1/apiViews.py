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
	seller.minPrice=request.POST.get('minPrice','')
	seller.maxPrice = request.POST.get('maxPrice','')
	seller.save()
	
	return JsonResponse({"success":"Updated"})