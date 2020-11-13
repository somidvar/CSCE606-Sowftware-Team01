from django.contrib import admin
from .models import Items_B, Biddings_B,Buyers_B

class BuyerAdmin(admin.ModelAdmin):
    list_display = ('Budget', 'Spent')
myModels = [Items_B, Biddings_B,Buyers_B]  # iterable list
admin.site.register(myModels)