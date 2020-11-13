from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import DateRangeField
from MyTimeFunctions import *

class Items_B(models.Model):
    Week_Number = models.IntegerField()
    Min_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Max_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Total_Availibility = models.IntegerField()
    Remaining_Availibility = models.IntegerField()
    Start_Date = models.DateTimeField()
    End_Date = models.DateTimeField()    
    Post_Date = models.DateTimeField()
        
    class Meta:
      db_table = 'Items'
      managed = False
    
    def __str__(self):
      return f'{self.Week_Number}, {self.Min_Price}, {self.Max_Price}, {self.Total_Availibility}, {self.Remaining_Availibility}, {self.Start_Date}, {self.End_Date},{self.Post_Date}'

class Biddings_B(models.Model):
    Bidding_Date = models.DateTimeField()
    Week_Number = models.IntegerField()
    Buyer_Id = models.IntegerField()
    Price = models.DecimalField(max_digits=10,decimal_places=2)
    Hours = models.IntegerField()
    Item_Id = models.IntegerField()

    class Meta:
      db_table = 'Biddings'
      managed = False
        
    def __str__(self):
      return f'{self.Bidding_Date}, {self.Week_Number}, {self.Buyer_Id}, {self.Price}, {self.Hours}, {self.Item_Id}'