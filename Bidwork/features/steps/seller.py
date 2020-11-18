from behave import given, when, then
from test.factories.user import UserFactory

@given('a logged in seller on the Seller Page')
def step_impl(context):
    admin = UserFactory(username='admin', email='admin@email.com', is_superuser=True, is_staff=True)
    admin.set_password('adminPassword')
    admin.save()
    context.username = "admin"
    context.password = "adminPassword"

    # Direct user to Login page
    br = context.browser
    br.get(context.base_url + '/')
    br.find_element_by_name("login").click()
    print(br.page_source)

    br.find_element_by_name('username').send_keys(context.username)
    br.find_element_by_name('password').send_keys(context.password)
    br.find_element_by_class_name("btn-outline-info").click()
    print(br.page_source)

    br.find_element_by_name("admin").click()
    br.find_element_by_xpath("//div[@id='content-main']/div[4]/table/tbody/tr/td/a").click()
    br.find_element_by_xpath("//nav[@id='nav-sidebar']/div[4]/table/tbody/tr/th/a").click()
    # br.find_element_by_name("seller").click()
    # br.get(context.base_url + '/buyer')
    # br.get('localhost:8000/register/')
    print(br.page_source)

@when('I enter the above bids')
def step_impl(context):
    pass

@then('I should see the bids on the Buyer and Seller page')
def step_impl(context):
	pass