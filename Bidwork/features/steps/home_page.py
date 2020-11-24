from behave import given, when, then

@given('a user on homepage')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/home')

@when('I select About')
def step_impl(context):
    br = context.browser
    # Direct user to About page
    br.find_element_by_name("about").click()

@then('I should be directed to the About page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith(context.base_url + "/aboutus")
    # Redirect to home page
    br.find_element_by_name("home").click()


@when('I select Register')
def step_impl(context):
    br = context.browser
    # Direct user to Register page
    br.find_element_by_name("register").click()


@then('I should be directed to the Register page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith(context.base_url + "/register/")
    # Redirect to home page
    br.find_element_by_name("home").click()

@when('I select Login')
def step_impl(context):
    br = context.browser
    # Direct user to Login page
    br.find_element_by_name("login").click()


@then('I should be directed to the Login page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith(context.base_url + "/login/")
    # Redirect to home page
    br.find_element_by_name("home").click()

@when('I select Developers')
def step_impl(context):
    br = context.browser
    # Direct user to Developers page
    br.find_element_by_name("developers").click()


@then('I should be directed to the Developers page')
def step_impl(context):
    br = context.browser
    assert br.current_url.endswith(context.base_url + "/developers")
    # Redirect to home page
    br.find_element_by_name("home").click()