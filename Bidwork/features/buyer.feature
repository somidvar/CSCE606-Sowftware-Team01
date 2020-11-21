Feature: Buyer

#  @slow
  Scenario: Test Buyer Page
    Given a logged in buyer on the Buyer Page
    When I enter the number of Bid Hours and select "Bid" button
    Then I should see the bid under "My Bids" on the Buyer page
      And as a seller I should see the bid under "Placed Bids" on the Seller page