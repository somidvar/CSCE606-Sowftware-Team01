from behave import given, when, then
from django.contrib.auth.models import User
from test.factories.user import ProfileFactory

@given('a logged in user on the homepage')
def step_impl(context):
	# Creates a dummy user for our tests (user is not authenticated at this point)
	user = User.objects.create_user(username='username', email='username@email.com', password='userPassword',
									is_superuser=False, is_staff=False)
	u = ProfileFactory(user=user)
	u.save()
	context.username = "username"
	context.password = "userPassword"
	context.emailAddress = "username@email.com"


    # Direct user to Login page
	br = context.browser
	br.get(context.base_url + '/home')
	br.find_element_by_name("login").click()

	# Fill login form and submit it (valid version)
	br.find_element_by_name('username').send_keys(context.username)
	br.find_element_by_name('password').send_keys(context.password)
	br.find_element_by_class_name("btn-outline-info").click()

@when('I select Help')
def step_impl(context):
    br = context.browser
    # Direct user to Help page
    br.find_element_by_name("help").click()

@then('I should be directed to the Help page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith(context.base_url + "/help")

@then('I should see "Faculties Help" and "Data-analyst Help" section')
def step_impl(context):
    helpSection1 = "Faculties Help"
    helpSection2 = "Data-analyst Help"
    br = context.browser
    # Check if the help page contains faculties and data-analyst help section
    assert br.find_element_by_xpath("//h1[@id='facultiesHelp']/strong").text==helpSection1 and br.find_element_by_xpath("//h1[@id='dataAnalystHelp']/strong").text==helpSection2
    # Redirect to home page
    br.find_element_by_name("home").click()

@when('I select Profile')
def step_impl(context):
    br = context.browser
    # Direct user to Profile page
    br.find_element_by_name("profile").click()

@then('I should be directed to the Profile page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith(context.base_url + "/profile/")

@then('I should see my Username and Email Address')
def step_impl(context):
    br = context.browser
    # Check if the help page contains faculties and data-analyst help section
    assert br.find_element_by_class_name("account-heading").text==context.username and br.find_element_by_class_name("text-secondary").text==context.emailAddress
    # Logout after test is complete
    br.find_element_by_name("logout").click()