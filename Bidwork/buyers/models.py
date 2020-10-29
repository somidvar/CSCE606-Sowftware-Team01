from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import DateRangeField

class Buyer(models.Model):
   buyerName=models.CharField(max_length=100)
   weekNumber=models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'), validators=[MinValueValidator(1)])
   dateRange = DateRangeField(default=0)
   bidPrice=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   bidHour=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0)])
   bidAmount=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   remainedBalance=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   initialBudget=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'), validators=[MinValueValidator(0.01)])
   
   def __str__(self):
      return f'{self.buyerName},{self.weekNumber},{self.dateRange}, {self.bidPrice},{self.bidHour}, {self.bidAmount},{self.remainedBalance},{self.initialBudget}'