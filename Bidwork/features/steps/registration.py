from behave import given, when, then

@given('an unregistered user on Registration page')
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
    print(br.current_url)
    assert br.current_url.endswith(context.base_url + "/home")
    # Check for notification for account created
    try:
        br.find_element_by_name('accountCreated')
    except:
        print("Failure")



@given('a registered user on Registration page')
def step_impl(context):
    context.username = "username"
    context.email = "username@email.com"
    context.password = "userPassword"

@then('I should be redirected to the Registration page and receive error message')
def step_impl(context):
    br = context.browser
    errorMessage = "A user with that username already exists."
    # Checks redirection URL and error message
    assert br.current_url.endswith(context.base_url + "/register/")
    assert br.find_element_by_id("error_1_id_username").text == errorMessage