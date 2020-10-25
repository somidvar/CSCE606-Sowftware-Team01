from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Seller(models.Model):
	sellerName=models.CharField(max_length=100)
	minPrice=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'))
	maxPrice=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'))
	currentPrice=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'))
	availabilityHour=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'))
	remainedHour=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'))
	horizon=models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'))
	weekNumber=models.DecimalField(max_digits=5, decimal_places=0,default=Decimal('0'))

	def __str__(self):
		return self.sellerName
