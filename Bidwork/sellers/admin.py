from django.contrib import admin
from .models import Seller

class SellerAdmin(admin.ModelAdmin):
    list_display = ('sellerName','weekNumber', 'dateRange','minPrice', 'maxPrice','currentPrice', 'availabilityHour', 'remainedHour', 'horizon')
admin.site.register(Seller, SellerAdmin)