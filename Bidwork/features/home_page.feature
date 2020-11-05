# Created by rahul at 11/4/20
Feature: Home Page

  Scenario: Test services of Home Page
    Given a user on homepage
    When I select About Us
    Then I should be directed to the About Us page
    When I select Register
    Then I should be directed to the Register page
    When I select Login
    Then I should be directed to the Login page
