from behave import given, when, then
from django.contrib.auth.models import User
from test.factories.user import ProfileFactory

@given('a registered user on Login page')
def step_impl(context):
	# Creates a dummy user for our tests (user is not authenticated at this point)
	user = User.objects.create_user(username='username', email='username@email.com', password='userPassword',
									is_superuser=False, is_staff=False)
	u = ProfileFactory(user=user)
	u.save()
	context.username = "username"
	context.password = "userPassword"

	# Direct user to Login page
	br = context.browser
	br.find_element_by_name("login").click()

@when('I submit a login request')
def step_impl(context):
	br = context.browser

	# Checks for Cross-Site Request Forgery protection input
	assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

	# Fill login form and submit it (valid version)
	br.find_element_by_name('username').send_keys(context.username)
	br.find_element_by_name('password').send_keys(context.password)
	br.find_element_by_class_name("btn-outline-info").click()

@then('I should be directed to the Home page')
def step_impl(context):
	br = context.browser
	# Checks URL matches Home Page URL
	assert br.current_url.endswith("/") and not br.current_url.endswith("/login/")
	# Redirect to home page
	br.find_element_by_name("logout").click()

@given('an unregistered user on Login page')
def step_impl(context):
	context.username = "username"
	context.password = "invalidPassword"

	# Direct user to Login page
	br = context.browser
	br.find_element_by_name("login").click()

@then('I should be redirected to the Login page and receive error message')
def step_impl(context):
	br = context.browser
	errorMessage = "Please enter a correct username and password. Note that both fields may be case-sensitive."
	# Checks redirection URL and error message
	assert br.current_url.endswith("/login/")
	assert br.find_element_by_class_name("alert-block").text == errorMessage