from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import DateRangeField

"""fix date range or change to start and end date"""
class Seller(models.Model):
   sellerName=models.CharField(max_length=100)
   weekNumber=models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
   dateRange= DateRangeField(default=0)
   minPrice=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   maxPrice=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   currentPrice=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   availabilityHour=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0)])
   remainedHour=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0)])
   horizon=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   

   def __str__(self):
      return f'{self.sellerName},{self.weekNumber}, {self.dateRange}, {self.minPrice}, {self.maxPrice}, {self.currentPrice}, {self.availabilityHour},{self.remainedHour}, {self.horizon}'