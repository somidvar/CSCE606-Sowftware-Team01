from behave import given, when, then
from django.contrib.auth.models import User
from test.factories.user import UserFactory
from django.core.management import call_command

@given('an seller user with administrative rights')
def step_impl(context):
    # Creating a buyer user
    user = User.objects.create_user(username='username', email='username@email.com', password='userPassword',
                                    is_superuser=False, is_staff=False)
    u = UserFactory(user=user)
    u.save()
    context.buyerUsername = "username"
    context.buyerPassword = "userPassword"
    context.buyerBudget = 100

    # Creating a seller user
    admin = User.objects.create_user(username='admin', email='admin@email.com', password='adminPassword',
                                     is_superuser=True, is_staff=True)
    a = UserFactory(user=admin)
    a.save()
    context.sellerUsername = "admin"
    context.sellerPassword = "adminPassword"

@when('I enter the budget for a buyer')
def step_impl(context):
    # Direct to Login Page
    br = context.browser
    br.get(context.base_url + '/')
    br.find_element_by_name("login").click()

    # Log In with seller credentials
    br.find_element_by_name('username').send_keys(context.sellerUsername)
    br.find_element_by_name('password').send_keys(context.sellerPassword)
    br.find_element_by_class_name("btn-outline-info").click()

    # Direct to Admin Page
    br.find_element_by_name("admin").click()
    # Select Profiles link under the Users section
    br.find_element_by_xpath("//div[@id='content-main']/div[last()]/table/tbody/tr/th/a").click()
    br.find_element_by_xpath("//nav[@id='nav-sidebar']/div[last()]/table/tbody/tr/th/a").click()
    # Select the buyer user and change the budget
    br.find_element_by_partial_link_text(context.buyerUsername).click()
    budget = br.find_element_by_id("id_budget")
    budget.send_keys(int(context.buyerBudget / 10))
    # Select the Save button
    br.find_element_by_name("_save").click()
    # Log out from the Admin page
    br.find_element_by_link_text("LOG OUT").click()

    # Direct user to the Login Page
    br.get(context.base_url + '/')
    br.find_element_by_name("login").click()

    # Log in with Buyer Credentials
    br.find_element_by_name('username').send_keys(context.buyerUsername)
    br.find_element_by_name('password').send_keys(context.buyerPassword)
    br.find_element_by_class_name("btn-outline-info").click()
    # Direct user to the Buyer Page
    br.find_element_by_name("buyer").click()

@then('the budget should be assigned to the buyer')
def step_impl(context):
    # Check if the modified budget is reflected on the Buyer's page
    br = context.browser
    assert float(br.find_element_by_xpath("//html/body/div[1]/div/div/div/h5/i[2]").text) == context.buyerBudget
    br.find_element_by_name("logout").click()
    # Clear records from the database
    call_command('flush', verbosity=0, interactive=False)

@given('a logged in seller on the Seller Page')
def step_impl(context):
    # Creating a buyer user
    user = User.objects.create_user(username='username', email='username@email.com', password='userPassword',
                                    is_superuser=False, is_staff=False)
    u = UserFactory(user=user)
    u.save()
    context.buyerUsername = "username"
    context.buyerPassword = "userPassword"

    # Creating a seller user
    admin = User.objects.create_user(username='admin', email='admin@email.com', password='adminPassword',
                                     is_superuser=True, is_staff=True)
    a = UserFactory(user=admin)
    a.save()
    context.sellerUsername = "admin"
    context.sellerPassword = "adminPassword"

    # Direct to Login Page
    br = context.browser
    br.get(context.base_url + '/')
    br.find_element_by_name("login").click()

    # Log In with seller credentials
    br.find_element_by_name('username').send_keys(context.sellerUsername)
    br.find_element_by_name('password').send_keys(context.sellerPassword)
    br.find_element_by_class_name("btn-outline-info").click()

    # Direct to Seller Page
    br.find_element_by_name("seller").click()

@when('I select Add a Bid')
def step_impl(context):
    br = context.browser
    br.find_element_by_name("addBid").click()
    # 2=Week Number, 3=Start Day, 4=Bid Start Date, 5=Bid Execution Date, 9=Remaining Availability
    context.tdSellerIndexOfBid = [2, 3, 4, 5, 9]
    context.newBidDetails = {}
    for idx in context.tdSellerIndexOfBid:
        context.newBidDetails[idx] = br.find_element_by_xpath("//tr[@id='tr_data'][last()]/td["+str(idx)+"]").text



@then('I should see the bid on the Buyer and Seller page')
def step_impl(context):
    br = context.browser
    for idx in context.tdSellerIndexOfBid:
        assert context.newBidDetails[idx] == br.find_element_by_xpath("//tr[@id='tr_data'][last()]/td["+str(idx)+"]").text

    br.find_element_by_name("logout").click()

    # Direct to Login Page
    br = context.browser
    br.get(context.base_url + '/')
    br.find_element_by_name("login").click()

    # Log In with seller credentials
    br.find_element_by_name('username').send_keys(context.buyerUsername)
    br.find_element_by_name('password').send_keys(context.buyerPassword)
    br.find_element_by_class_name("btn-outline-info").click()

    # Direct to Seller Page
    br.find_element_by_name("buyer").click()

    # 2=Week Number, 3=Start Day, 4=Bid Start Date, 5=Bid Execution Date, 7=Remaining Availability
    tdBuyerIndexOfBid = [2, 3, 4, 5, 7]
    for idx in range(len(tdBuyerIndexOfBid)):
        assert context.newBidDetails[context.tdSellerIndexOfBid[idx]] == br.find_element_by_xpath("//tr[@id='tr_data'][last()]/td["+str(tdBuyerIndexOfBid[idx])+"]").text

