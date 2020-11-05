from behave import given, when, then
from selenium.webdriver.common.by import By
from time import sleep


@given('a user on homepage')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/')

@when('I select About Us')
def step_impl(context):
    br = context.browser
    context.about_us_url = br.find_element_by_name("aboutUs").get_attribute("href")

@then('I should be directed to the About Us page')
def step_impl(context):
    assert context.about_us_url.endswith('/aboutus')


@when('I select Register')
def step_impl(context):
    br = context.browser
    context.about_us_url = br.find_element_by_name("register").get_attribute("href")


@then('I should be directed to the Register page')
def step_impl(context):
    assert context.about_us_url.endswith('/register/')

@when('I select Login')
def step_impl(context):
    br = context.browser
    context.about_us_url = br.find_element_by_name("login").get_attribute("href")


@then('I should be directed to the Login page')
def step_impl(context):
    assert context.about_us_url.endswith('/login/')