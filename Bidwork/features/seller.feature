Feature: Seller

  Scenario: Test Seller Page
    Given a logged in seller on the Seller Page
    When I enter the above bids
    Then I should see the bids on the Buyer and Seller page

#    Given an seller user with administrative rights
#    When I enter the budget for a buyer
#    Then the budget should be assigned to the buyer

