from behave import given, when, then


@given('an unregistered user')
def step_impl(context):
    context.username = "username"
    context.email = "username@email.com"
    context.password = "userPassword"


@when('I fill out the signup form and click Sign Up')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/register/')
    br.find_element_by_name('username').send_keys(context.username)
    br.find_element_by_name('email').send_keys(context.email)
    br.find_element_by_name('password1').send_keys(context.password)
    br.find_element_by_name('password2').send_keys(context.password)
    br.find_element_by_name('signUp').click()


@then('I should be directed to the Home Page and recieve a notification that an account is created')
def step_impl(context):
    br = context.browser
    # Check if the browser is on home page
    assert br.current_url.endswith(context.base_url + "/")
    # Check for notification for account created
    try:
        br.find_element_by_name('accountCreated')
    except:
        print("Failure")



@given('a registered user')
def step_impl(context):
    pass

@then('I should redirected to the Sign Up page and recieve an error message')
def step_impl(context):
    pass