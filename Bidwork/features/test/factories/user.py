import factory
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User
		# django_get_or_create = ('username', 'email')
		django_get_or_create = ('username', 'email', 'is_superuser', 'is_staff')

	# Defaults (can be overrided)
	username = 'zhenyu.wu'
	email = 'zhenyu.wu@tamu.edu'
	is_superuser = False
	is_staff = False
	# is_active = True