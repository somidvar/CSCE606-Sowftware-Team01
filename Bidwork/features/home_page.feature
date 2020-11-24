Feature: Home Page

  Scenario: Test services of Home Page
    Given a user on homepage
    When I select About
    Then I should be directed to the About page
    When I select Register
    Then I should be directed to the Register page
    When I select Login
    Then I should be directed to the Login page
    When I select Developers
    Then I should be directed to the Developers page
