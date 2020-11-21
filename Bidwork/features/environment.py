from selenium import webdriver
from django.core.management import call_command
import os

def before_all(context):
	# PhantomJS is used there (headless browser - meaning we can execute tests in a command-line environment, which is what we want for use with SemaphoreCI
	# For debugging purposes, you can use the Firefox driver instead.
	# context.browser = webdriver.PhantomJS()
	context.browser = webdriver.Firefox()
	context.browser.set_window_size(1920, 1080)
	context.browser.implicitly_wait(1)
	context.server_url = 'http://localhost:8000'
	call_command('flush', verbosity=0, interactive=False)


def after_all(context):
	# Explicitly quits the browser, otherwise it won't once tests are done
	context.browser.quit()

def before_scenario(context, scenario):
	# Code to be executed each time a feature is going to be tested
	call_command('flush', verbosity=0, interactive=False)