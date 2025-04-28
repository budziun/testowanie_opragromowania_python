Feature: Prepaid phone functionality
    As a prepaid phone user
    I want to manage my phone balance and make calls
    So that I can use my phone services effectively

    Background:
        Given a prepaid phone with number "555-123-4567"

    Scenario: Make a call with sufficient balance
        Given the phone has a balance of $10.00
        When I make a call that costs $2.50
        Then the call should be successful
        And the remaining balance should be $7.50

    Scenario: Attempt to make a call with insufficient balance
        Given the phone has a balance of $1.00
        When I attempt to make a call that costs $2.50
        Then the call should be rejected
        And the remaining balance should be $1.00

    Scenario: Top up the phone balance
        Given the phone has a balance of $5.00
        When I add $15.00 to the balance
        Then the new balance should be $20.00

    Scenario: Check call history
        Given the phone has a balance of $20.00
        And I have made the following calls:
            | number       | duration | cost  |
            | 555-987-6543 | 5 min    | $2.50 |
            | 555-234-5678 | 3 min    | $1.50 |
        When I check my call history
        Then I should see 2 calls in the history
        And the total cost should be $4.00

    Scenario Outline: Different call rates
        Given the phone has a balance of $10.00
        When I make a <duration> minute call to <type> number
        Then the call cost should be $<cost>
        And the remaining balance should be $<remaining>

        Examples:
            | duration | type          | cost | remaining |
            | 2        | local         | 0.40 | 9.60      |
            | 5        | international | 5.00 | 5.00      |
            | 3        | mobile        | 0.90 | 9.10      |

    Scenario: Multiple top-ups with different amounts
        Given the phone has a balance of $0.00
        When I add the following amounts:
            | amount |
            | $5.00  |
            | $10.00 |
            | $2.50  |
        Then the final balance should be $17.50

    Scenario: Check balance limits
        Given the phone has a balance of $95.00
        When I add $10.00 to the balance
        Then the operation should be rejected with message "Maximum balance limit of $100.00 exceeded"
        And the balance should remain $95.00

    Scenario: Send SMS message
        Given the phone has a balance of $5.00
        When I send an SMS message
        Then the SMS should be sent successfully
        And the remaining balance should be $4.80

    Scenario: Multiple operations in sequence
        Given the phone has a balance of $20.00
        When I perform the following operations:
            | operation | detail        | amount |
            | call      | 5 min local   | $1.00  |
            | sms       | 1 message     | $0.20  |
            | topup     | add credit    | $5.00  |
            | call      | 3 min mobile  | $0.90  |
        Then the final balance should be $22.90