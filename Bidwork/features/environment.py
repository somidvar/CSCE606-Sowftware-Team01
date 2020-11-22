from selenium import webdriver
from sellers.models import Items, Biddings
from buyers.models import Items_B, Biddings_B
from django.core.management import call_command

def before_all(context):
	context.browser = webdriver.Firefox()
	context.browser.set_window_size(1920, 1080)
	context.browser.implicitly_wait(1)
	context.server_url = 'http://localhost:8000'
	call_command('flush', verbosity=0, interactive=False)


def after_all(context):
	# Explicitly quits the browser, otherwise it won't once tests are done
	context.browser.quit()

# Code to be executed each time a scenario is tested
def before_scenario(context, scenario):
	Items.objects.all().delete()
	Biddings.objects.all().delete()
	Items_B.objects.all().delete()
	Biddings_B.objects.all().delete()