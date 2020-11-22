Feature: Seller
#  @slow
  Scenario: Test Seller Page
#    Given an seller user with administrative rights
#    When I enter the budget for a buyer
#    Then the budget should be assigned to the buyer

    Given a logged in seller on the Seller Page
    When I Add the below bids
      | Week Number | Bid Start Date   | Bid End Date     | Min Price | Max Price  | Total Availability |
      | 35          | 2019-12-05 00:00 | 2019-12-10 00:00 | 10.00     | 60.00      | 5                  |
      | 40          | 2020-08-10 00:00 | 2020-08-15 00:00 | 20.00     | 70.00      | 10                 |
      | 45          | 2020-09-15 00:00 | 2020-09-20 00:00 | 30.00     | 80.00      | 15                 |
      | 50          | 2020-10-20 00:00 | 2020-10-25 00:00 | 40.00     | 90.00      | 20                 |
      | 53          | 2020-12-05 00:00 | 2020-12-10 00:00 | 50.00     | 100.00     | 25                 |
    Then I should see the bid on the Buyer and Seller page



