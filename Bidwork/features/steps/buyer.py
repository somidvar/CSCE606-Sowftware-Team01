from MyTimeFunctions import *
from behave import given, when, then
from test.factories.user import ProfileFactory
from django.contrib.auth.models import User
from django.core.management import call_command

@given('a logged in buyer on the Buyer Page with the below bids')
def step_impl(context):
    # Creating a buyer user
    user = User.objects.create_user(username='username', email='username@email.com', password='userPassword',
                                    is_superuser=False, is_staff=False)
    userBudget = 3000.000
    u = ProfileFactory(user=user, budget=userBudget)
    u.save()
    context.buyerUsername = "username"
    context.buyerPassword = "userPassword"

    # Creating a seller user
    admin = User.objects.create_user(username='admin', email='admin@email.com', password='adminPassword',
                                     is_superuser=True, is_staff=True)
    a = ProfileFactory(user=admin)
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

    # Save the input bid table for later use
    context.bidInputTable = context.table
    context.bidHeader = ["Week Number", "Bid Start Date", "Bid End Date", "Min Price", "Max Price",
                         "Total Availability"]
    # 2=WeekNumber, 4=Bid Start Date, 5=Bid End Date, 6=Min Price, 7=Max Price, 9=Total Hours
    context.tdSellerIndexOfBid = [2, 4, 5, 6, 7, 9]
    for row in context.bidInputTable:
        # Select Add Bid button
        br.find_element_by_name("addBid").click()
        for idx in range(len(context.bidHeader)):
            # Click the table column (td class="editable")
            # then input/{select/option} tag appears
            # select it, clear previous value and enter new value
            # Click update button twice to update record
            bidColumn = br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[" + str(context.tdSellerIndexOfBid[idx]) + "]")
            bidColumn.click()
            if idx == 0:
                br.find_element_by_xpath(
                    "//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[" + str(context.tdSellerIndexOfBid[idx]) + "]/select/option[" + row[
                        context.bidHeader[
                            idx]] + "]").click()
            else:
                br.find_element_by_xpath(
                    "//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[" + str(context.tdSellerIndexOfBid[idx]) + "]/input").clear()
                bidColumn.click()
                br.find_element_by_xpath(
                    "//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[" + str(context.tdSellerIndexOfBid[idx]) + "]/input").send_keys(
                    row[context.bidHeader[idx]])
            br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[12]/input").click()
            br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[12]/input").click()

    br.find_element_by_name("logout").click()

    # Direct to Login Page
    br = context.browser
    br.get(context.base_url + '/')
    br.find_element_by_name("login").click()

    # Log In with buyer credentials
    br.find_element_by_name('username').send_keys(context.buyerUsername)
    br.find_element_by_name('password').send_keys(context.buyerPassword)
    br.find_element_by_class_name("btn-outline-info").click()

    # Direct to Buyer Page
    br.find_element_by_name("buyer").click()

@when('I enter the number of Bid Hours and select "Bid" button')
def step_impl(context):
    br = context.browser
    context.bidHours = "10"
    context.bidWeekNumber = br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[2]").text
    # Click the Bid Hours column (td class="editable")
    bidColumn = br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[9]")
    bidColumn.click()
    # Then input tag appears; Select it, clear previous value Enter new Bid Hours
    br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[9]/input").clear()
    bidColumn.click()
    br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[9]/input").send_keys(context.bidHours)
    # Click Bid button to update record
    br.find_element_by_xpath("//form[@id='form1']/table/tbody/tr[@id='tr_data'][1]/td[10]/input").click()


@then('I should see the bid under "My Bids" on the Buyer page')
def step_impl(context):
    br = context.browser
    # Check for Week Number of the placed bid under "My Bids" on the Buyer page
    assert context.bidWeekNumber == br.find_element_by_xpath("//form[@id='form2']/table/tbody/tr[@id='tr_data'][1]/td[2]").text
    # Check for Bid Hours of the placed bid under "My Bids" on the Buyer page
    assert context.bidHours == br.find_element_by_xpath("//form[@id='form2']/table/tbody/tr[@id='tr_data'][1]/td[4]").text
    br.find_element_by_name("logout").click()

@then('as a seller I should see the bid under "Placed Bids" on the Seller page')
def step_impl(context):
    # Direct to Login Page
    br = context.browser
    br.get(context.base_url + '/')
    br.find_element_by_name("login").click()

    # Log In with Seller credentials
    br.find_element_by_name('username').send_keys(context.sellerUsername)
    br.find_element_by_name('password').send_keys(context.sellerPassword)
    br.find_element_by_class_name("btn-outline-info").click()

    # Direct to Seller Page
    br.find_element_by_name("seller").click()
    # Check for Week Number of the placed bid under "Placed Bids" on the Seller page
    assert context.bidWeekNumber == br.find_element_by_xpath("//form[@id='form2']/table/tbody/tr[@id='tr_data'][1]/td[2]").text
    # Check for Buyer username of the placed bid under "Placed Bids" on the Seller page
    assert context.buyerUsername == br.find_element_by_xpath("//form[@id='form2']/table/tbody/tr[@id='tr_data'][1]/td[3]").text
    # Check for Bid Hours of the placed bid under "Placed Bids" on the Seller page
    assert context.bidHours == br.find_element_by_xpath("//form[@id='form2']/table/tbody/tr[@id='tr_data'][1]/td[5]").text

    call_command('flush', verbosity=0, interactive=False)

