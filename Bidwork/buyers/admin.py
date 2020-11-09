from django.contrib import admin
from .models import Items_B, Biddings_B, Buyers_B

class BuyerAdmin(admin.ModelAdmin):
    list_display = ('Bidding_Date', 'Week_Number', 'Buyer_Id', 'Bidding_Date', 'Week_Number', 'Buyer_Id', 'Price', 'Hours', 'User_Id', 'Total_Budget', 'Spent', 'Week_Number','Min_Price', 'Max_Price', 'Start_Date', 'End_Date','Total_Availibility','Post_Date')
myModels = [Items_B, Biddings_B, Buyers_B]  # iterable list
admin.site.register(myModels)