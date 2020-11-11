from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import DateRangeField
from django.utils import timezone
import pytz
import datetime


class Items(models.Model): 
    TimeZone_Offset = -5
    Current_DateTime=datetime.datetime.now()+datetime.timedelta(hours = TimeZone_Offset)

    Week_Number = models.DecimalField(max_digits=2, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(0)])
    Min_Price = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
    Max_Price = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
    Start_Date = models.DateTimeField(default= Current_DateTime)
    End_Date = models.DateTimeField(default= Current_DateTime)    
    Post_Date = models.DateTimeField(default= Current_DateTime)
    Total_Availibility = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    

    class Meta:
        db_table = 'Items'
        managed = False
    
    def __str__(self):
      return f'{self.Week_Number}, {self.Min_Price}, {self.Max_Price}, {self.Start_Date}, {self.End_Date}, {self.Total_Availibility},{self.Post_Date}'


class Biddings(models.Model):
    Bidding_Date = models.DateTimeField(default=timezone.now)
    Week_Number = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Buyer_Id = models.TextField(max_length=100,blank = True)
    Price = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
    Hours = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0)])
    Item_Id = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('-1'), validators=[MinValueValidator(1)])
    class Meta:
        db_table = 'Biddings'
        managed = False

    def __str__(self):
      return f'{self.Bidding_Date}, {self.Week_Number}, {self.Buyer_Id}, {self.Price}, {self.Hours}, {self.Item_Id}'

class Buyers(models.Model):
    User_Id = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Total_Budget = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Spent = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])

    class Meta:
      db_table = 'Buyers'
      managed = False

    def __str__(self):
      return f'{self.User_Id}, {self.Total_Budget}, {self.Spent}'

