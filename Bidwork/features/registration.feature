Feature: Registration

  Scenario: Validate Registration Page

    Given an unregistered user on Registration page
    When I fill out the signup form and click Sign Up
    Then I should be directed to the Home Page and recieve a notification that an account is created

    Given a registered user on Registration page
    When I fill out the signup form and click Sign Up
    Then I should be redirected to the Registration page and receive error message