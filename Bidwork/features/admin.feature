Feature: Admin

  Scenario: Test Admin Page
    Given an user with administrative rights
    When I submit an admin login request
    Then I should be directed to the Admin page

    Given an user without administrative rights
    When I submit an admin login request
    Then I should receive an error message
