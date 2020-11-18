import time
from behave import given, when, then
from test.factories.user import UserFactory

@given('a logged in buyer on the Buyer Page')
def step_impl(context):
    admin = UserFactory(username='admin', email='admin@email.com', is_superuser=True, is_staff=True)
    admin.set_password('adminPassword')
    admin.save()
    context.sellerUsername = "admin"
    context.sellerPassword = "adminPassword"

    # Direct user to Login page
    br = context.browser
    br.get(context.base_url + '/')
    br.find_element_by_name("login").click()
    print(br.page_source)

    br.find_element_by_name('username').send_keys(context.sellerUsername)
    br.find_element_by_name('password').send_keys(context.sellerPassword)
    br.find_element_by_class_name("btn-outline-info").click()
    print(br.page_source)

    # br.find_element_by_name("admin").click()
    # br.find_element_by_xpath("//div[@id='content-main']/div[4]/table/tbody/tr/td/a").click()
    # br.find_element_by_xpath("//nav[@id='nav-sidebar']/div[4]/table/tbody/tr/th/a").click()
    br.find_element_by_name("seller").click()
    # br.find_element_by_name("addBid").click()
    print(br.page_source)

    # Creates a dummy user for our tests (user is not authenticated at this point)
    # u = UserFactory(username='username', email='username@email.com')
    # u.set_password('userPassword')
    # u.save()
    #
    # context.buyerUsername = "username"
    # context.buyerPassword = "userPassword"
    #
    # # Direct user to Login page
    # br = context.browser
    # br.get(context.base_url + '/')
    # br.find_element_by_name("login").click()
    # # print(br.page_source)
    #
    # br.find_element_by_name('username').send_keys(context.buyerUsername)
    # br.find_element_by_name('password').send_keys(context.buyerPassword)
    # br.find_element_by_class_name("btn-outline-info").click()
    # print(br.page_source)
    #
    # # br.find_element_by_name("aboutUs").click()
    # # time.sleep(1)
    # # br.find_element_by_name("home").click()
    # # time.sleep(1)
    # br.find_element_by_name("buyer").click()
    # # br.get(br.find_element_by_name("buyer").get_attribute("href"))
    # time.sleep(1)
    # print(br.page_source)
    # br.get(context.base_url + '/buyer')

    # print(br.page_source)

@when('I enter the number of Bid Hours and select "Bid" button')
def step_impl(context):
    # br = context.browser
    # br.find_element_by_id("form1")
    pass

@then('I should see the bid under "My Bids" on the Buyer page')
def step_impl(context):
	pass

@then('as a seller I should see the bid under "Placed Bids" on the Seller page')
def step_impl(context):
	pass