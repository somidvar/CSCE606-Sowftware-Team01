from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    budget=models.DecimalField(max_digits=10, decimal_places=3,default=Decimal('0'))
    spent=models.DecimalField(max_digits=10, decimal_places=3,default=Decimal('0'))
    isBuyer=models.IntegerField(default=1)
    def __str__(self):
        return f'{self.user.username} Profile'
