from behave import given, when, then
from django.contrib.auth.models import User
from test.factories.user import UserFactory

@given('an user with administrative rights')
def step_impl(context):
    # Create user with admin rights for testing
    admin = User.objects.create_user(username='admin', email='admin@email.com', password='adminPassword',
                                     is_superuser=True, is_staff=True)
    a = UserFactory(user=admin)
    a.save()
    context.username = "admin"
    context.password = "adminPassword"

@when('I submit an admin login request')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/admin/')
    br.find_element_by_name('username').send_keys(context.username)
    br.find_element_by_name('password').send_keys(context.password)
    # Select Log in button after login credentials are entered
    br.find_element_by_xpath("//form[1]/div[3]/input").click()

@then('I should be directed to the Admin page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith(context.base_url + "/admin/")
    # Logout after test is complete
    br.find_element_by_xpath("//div[@id='user-tools']/a[3]").click()
    print(br.current_url)


@given('an user without administrative rights')
def step_impl(context):
    # Create user without admin rights for testing
    user = User.objects.create_user(username='username', email='username@email.com', password='userPassword',
                                    is_superuser=False, is_staff=False)
    u = UserFactory(user=user)
    u.save()
    context.username = "username"
    context.password = "userPassword"

@then('I should receive an error message')
def step_impl(context):
    br = context.browser
    errorMessage = "Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive."
    assert br.find_element_by_class_name("errornote").text == errorMessage
    assert br.current_url.endswith(context.base_url + "/admin/login/?next=/admin/")