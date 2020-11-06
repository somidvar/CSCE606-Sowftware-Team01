Feature: Registration

  Scenario: Validate Registration Page

    Given an unregistered user
    When I fill out the signup form and click Sign Up
    Then I should be directed to the Home Page and recieve a notification that an account is created

    Given a registered user
    When I fill out the signup form and click Sign Up
    Then I should redirected to the Sign Up page and recieve an error message