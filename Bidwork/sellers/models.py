from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import DateRangeField
from django.utils import timezone

"""fix date range or change to start and end date"""
class Items(models.Model):
   # sellerName=models.CharField(max_length=100)
   # weekNumber=models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
   # dateRange= DateRangeField(default=0)
   # minPrice=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   # maxPrice=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   # currentPrice=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   # availabilityHour=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0)])
   # remainedHour=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0)])
   # horizon=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])

   

    Week_Number = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Min_Price = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
    Max_Price = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
    Start_Date = models.DateTimeField(default=timezone.now)
    End_Date = models.DateTimeField(default=timezone.now)
    Total_Availibility = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Post_Date = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'Items'
        managed = False
    
    def __str__(self):
      #return f'{self.sellerName},{self.weekNumber}, {self.dateRange}, {self.minPrice}, {self.maxPrice}, {self.currentPrice}, {self.availabilityHour},{self.remainedHour}, {self.horizon}'
      return f'{self.Week_Number}, {self.Min_Price}, {self.Max_Price}, {self.Start_Date}, {self.End_Date}, {self.Total_Availibility},{self.Post_Date}'

class Biddings(models.Model):
    Bidding_Date = models.DateTimeField(default=timezone.now)
    Week_Number = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Buyer_Id = models.TextField(max_length=100,blank = True)
    Price = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
    Hours = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0)])
    #User_Id = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    #Total_Budget = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    #Spent = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Item_Id = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('-1'), validators=[MinValueValidator(1)])
    class Meta:
        db_table = 'Biddings'
        managed = False

    def __str__(self):
      #return f'{self.sellerName},{self.weekNumber}, {self.dateRange}, {self.minPrice}, {self.maxPrice}, {self.currentPrice}, {self.availabilityHour},{self.remainedHour}, {self.horizon}'
      return f'{self.Bidding_Date}, {self.Week_Number}, {self.Buyer_Id}, {self.Price}, {self.Hours}, {self.Item_Id}'

class Buyers(models.Model):
    User_Id = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Total_Budget = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
    Spent = models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])

    class Meta:
      db_table = 'Buyers'
      managed = False

    def __str__(self):
      #return f'{self.sellerName},{self.weekNumber}, {self.dateRange}, {self.minPrice}, {self.maxPrice}, {self.currentPrice}, {self.availabilityHour},{self.remainedHour}, {self.horizon}'
      return f'{self.User_Id}, {self.Total_Budget}, {self.Spent}'
