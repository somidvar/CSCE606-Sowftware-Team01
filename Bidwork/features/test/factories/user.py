import factory
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from users.models import Profile
# class UserFactory(factory.django.DjangoModelFactory):
# 	class Meta:
# 		model = User
# 		# django_get_or_create = ('username', 'email')
# 		django_get_or_create = ('username', 'email', 'is_superuser', 'is_staff')
#
# 	# Defaults (can be overrided)
# 	username = 'zhenyu.wu'
# 	email = 'zhenyu.wu@tamu.edu'
# 	is_superuser = False
# 	is_staff = False
# 	# is_active = True
class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		# model = User
		model = Profile
		# django_get_or_create = ('username', 'email')
		# django_get_or_create = ('username', 'email', 'is_superuser', 'is_staff')

	# Defaults (can be overrided)
	# user = User.objects.create_user('username', 'username@email.com', 'userPassword')
	# user.is_superuser = False
	# user.is_staff = False
	image='default.jpg'
	budget = 0.000
	spent=0.000
	isBuyer=1
	# is_active = True