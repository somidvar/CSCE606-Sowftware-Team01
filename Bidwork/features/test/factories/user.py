import factory
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User
		django_get_or_create = ('username', 'email')

	# Defaults (can be overrided)
	username = 'zhenyu.wu'
	email = 'zhenyu.wu@tamu.edu'