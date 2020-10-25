In order to work with the database, please make sure that you are setting the parameters first:
inside the terminal set the settings
for windows:
set DJANGO_SETTINGS_MODULE=Bidwork.settings
for linux:
set export DJANGO_SETTINGS_MODULE=Bidwork.settings
Then, you need to import the following lines in the python file
import django
django.setup()

from app1.models import Post
from sellers.models import Seller
from users.models import Profile
from django.contrib.auth.models import User