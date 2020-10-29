from django.contrib import admin
from .models import Buyer

class BuyerAdmin(admin.ModelAdmin):
    list_display = ('buyerName','weekNumber', 'dateRange','bidPrice', 'bidHour','bidAmount', 'remainedBalance', 'initialBudget')
admin.site.register(Buyer, BuyerAdmin)