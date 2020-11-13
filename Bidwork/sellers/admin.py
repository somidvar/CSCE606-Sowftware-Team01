from django.contrib import admin
from .models import Items, Biddings

class SellerAdmin(admin.ModelAdmin):
    list_display = ('Week_Number','Min_Price', 'Max_Price', 'Start_Date', 'End_Date','Total_Availibility','Remaining_Availibility','Post_Date')
myModels = [Items, Biddings]  # iterable list
admin.site.register(myModels)