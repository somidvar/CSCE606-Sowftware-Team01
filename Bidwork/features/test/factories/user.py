import factory
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from users.models import Profile

class ProfileFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Profile
	image='default.jpg'
	budget = 0.000
	spent=0.000
	isBuyer=1