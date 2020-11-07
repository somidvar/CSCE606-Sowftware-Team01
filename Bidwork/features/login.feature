Feature: Login form

  Scenario: Access the login form

	Given a registered user on Login page
	When I submit a login request
	Then I should be directed to the Home page

	Given an unregistered user on Login page
	When I submit a login request
	Then I should be redirected to the Login page and receive error message