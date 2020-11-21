import time
from behave import given, when, then
from test.factories.user import UserFactory
from django.contrib.auth.models import User

@given('a logged in buyer on the Buyer Page')
def step_impl(context):
    # Creates a dummy user for our tests (user is not authenticated at this point)
    user = User.objects.create_user(username='username', email='username@email.com', password='userPassword', is_superuser=False, is_staff=False)
    u = UserFactory(user=user)
    u.save()

    context.buyerUsername = "username"
    context.buyerPassword = "userPassword"
    context.buyerBudget = 100
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
    # br.find_element_by_name("buyer").click()
    # print(br.page_source)
    # br.find_element_by_name("logout").click()

    admin = User.objects.create_user(username='admin', email='admin@email.com', password='adminPassword', is_superuser=True, is_staff=True)
    a = UserFactory(user=admin)
    a.save()
    # admin = UserFactory(user=admin)
    # admin.set_password('adminPassword')
    # admin.save()
    context.sellerUsername = "admin"
    context.sellerPassword = "adminPassword"

    # Direct user to Login page
    br = context.browser
    br.get(context.base_url + '/')
    br.find_element_by_name("login").click()
    # print(br.page_source)

    br.find_element_by_name('username').send_keys(context.sellerUsername)
    br.find_element_by_name('password').send_keys(context.sellerPassword)
    br.find_element_by_class_name("btn-outline-info").click()
    # print(br.page_source)
    #
    br.find_element_by_name("admin").click()
    br.find_element_by_xpath("//div[@id='content-main']/div[4]/table/tbody/tr/td[1]/a").click()
    br.find_element_by_xpath("//nav[@id='nav-sidebar']/div[4]/table/tbody/tr/th/a").click()
    br.find_element_by_partial_link_text(context.buyerUsername).click()
    budget = br.find_element_by_id("id_budget")
    budget.send_keys(int(context.buyerBudget/10))
    # bud = budget.get_attribute("value")
    br.find_element_by_name("_save").click()
    br.find_element_by_partial_link_text(context.buyerUsername).click()
    br.find_element_by_link_text("LOG OUT").click()
    # br.find_element_by_partial_link_text(context.buyerUsername).click()
    # bud = br.find_element_by_id("id_budget").get_attribute("value")
    # print(bud)



    # br.find_element_by_name("seller").click()
    # br.find_element_by_name("addBid").click()
    # element = br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[2]/td[6]")
    # updateButton = br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[2]/td[12]/input")
    # actions = ActionChains(br)
    # actions.double_click(element)
    # actions.send_keys_to_element('15')
    # actions.click(updateButton)
    # import time
    # time.sleep(5)
    # br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[2]/td[6]").send_keys(15)
    # # import time
    # # time.sleep(1)
    # br.implicitly_wait(1)
    # br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[2]/td[12]/input").click()
    # br.find_element_by_name("logout").click()

    # Creates a dummy user for our tests (user is not authenticated at this point)
    # u = UserFactory(username='username', email='username@email.com')
    # u.set_password('userPassword')
    # u.save()

    # context.buyerUsername = "username"
    # context.buyerPassword = "userPassword"

    # Direct user to Login page
    # br = context.browser
    br.get(context.base_url + '/')
    br.find_element_by_name("login").click()
    # print(br.page_source)

    br.find_element_by_name('username').send_keys(context.buyerUsername)
    br.find_element_by_name('password').send_keys(context.buyerPassword)
    br.find_element_by_class_name("btn-outline-info").click()
    # print(br.page_source)
    #
    br.find_element_by_name("buyer").click()
    # print(br.page_source)

@when('I enter the number of Bid Hours and select "Bid" button')
def step_impl(context):
    br = context.browser
    assert float(br.find_element_by_xpath("//html/body/div[1]/div/div/div/h5/i[2]").text) == context.buyerBudget

@then('I should see the bid under "My Bids" on the Buyer page')
def step_impl(context):
	pass

@then('as a seller I should see the bid under "Placed Bids" on the Seller page')
def step_impl(context):
	pass