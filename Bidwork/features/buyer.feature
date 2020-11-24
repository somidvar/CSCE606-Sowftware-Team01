Feature: Buyer

  Scenario: Test Buyer Page
    Given a logged in buyer on the Buyer Page with the below bids
      | Week Number | Bid Start Date   | Bid End Date     | Min Price | Max Price  | Total Availability |
      | 35          | 2019-12-05 00:00 | 2019-12-10 00:00 | 10.00     | 60.00      | 5                  |
      | 40          | 2020-08-10 00:00 | 2020-08-15 00:00 | 20.00     | 70.00      | 10                 |
      | 45          | 2020-09-15 00:00 | 2020-09-20 00:00 | 30.00     | 80.00      | 15                 |
      | 50          | 2020-10-20 00:00 | 2020-10-25 00:00 | 40.00     | 90.00      | 20                 |
      | 53          | 2020-12-05 00:00 | 2020-12-10 00:00 | 50.00     | 100.00     | 25                 |
    When I enter the number of Bid Hours and select "Bid" button
    Then I should see the bid under "My Bids" on the Buyer page
      And as a seller I should see the bid under "Placed Bids" on the Seller page