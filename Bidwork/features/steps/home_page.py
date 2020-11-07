from behave import given, when, then

@given('a user on homepage')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/')

@when('I select About Us')
def step_impl(context):
    br = context.browser
    # Direct user to About Us page
    br.find_element_by_name("aboutUs").click()

@then('I should be directed to the About Us page')
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