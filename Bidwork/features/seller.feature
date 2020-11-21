Feature: Seller
  @slow
  Scenario: Test Seller Page
    Given an seller user with administrative rights
    When I enter the budget for a buyer
    Then the budget should be assigned to the buyer

    Given a logged in seller on the Seller Page
    When I select Add a Bid
    Then I should see the bid on the Buyer and Seller page



