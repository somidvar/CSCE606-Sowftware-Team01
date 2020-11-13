from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import DateRangeField
from MyTimeFunctions import *

class Items(models.Model): 
    Week_Number = models.DecimalField(max_digits=2, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(0)])
    Min_Price = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
    Max_Price = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
    Total_Availibility = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Remaining_Availibility = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(0)])
    Start_Date = models.DateTimeField(default= MyCurrentTime())
    End_Date = models.DateTimeField(default= MyCurrentTime())    
    Post_Date = models.DateTimeField(default= MyCurrentTime())
        
    class Meta:
        db_table = 'Items'
        managed = False
    
    def __str__(self):
      return f'{self.Week_Number}, {self.Min_Price}, {self.Max_Price}, {self.Total_Availibility}, {self.Remaining_Availibility},{self.Start_Date}, {self.End_Date},{self.Post_Date}'


class Biddings(models.Model):
    Bidding_Date = models.DateTimeField(default= MyCurrentTime())
    Week_Number = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    Buyer_Id = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    Price = models.DecimalField(max_digits=10,decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.00)])
    Hours = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    Item_Id = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    class Meta:
        db_table = 'Biddings'
        managed = False

    def __str__(self):
      return f'{self.Bidding_Date}, {self.Week_Number}, {self.Buyer_Id}, {self.Price}, {self.Hours}, {self.Item_Id}'

class Buyers(models.Model):
    Spent = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Budget = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    class Meta:
      db_table = 'Buyers'
      managed = False

    def __str__(self):
      return f'{self.Spent},{self.Budget}'