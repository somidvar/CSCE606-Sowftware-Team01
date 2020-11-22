# Bidwork

## Installation

### Requirements:
- Django~=3.1.2
- Selenium (Testing)
- behave_django (Testing)
- factory_boy (Testing)

### Step-by-step installation for Linux
```
conda create --name team01 python=3.6
conda activate team01
cd team01
pip install -r requirements.txt
cd Bidwork

```

## Testing

### Instructions for running testing
Set managed=True for Items and Biddings Model in sellers/migrations/000_initial.py
```
python manage.py behave
```

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

Testing
Set managed=True for Items and Biddings Model in sellers/migrations/000_initial.py
