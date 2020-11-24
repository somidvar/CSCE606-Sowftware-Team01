Feature:

  Scenario: Test Profile and Help Page
    Given a logged in user on the homepage
    When I select Help
    Then I should be directed to the Help page
      And I should see "Faculties Help" and "Data-analyst Help" section
    When I select Profile
    Then I should be directed to the Profile page
      And I should see my Username and Email Address
