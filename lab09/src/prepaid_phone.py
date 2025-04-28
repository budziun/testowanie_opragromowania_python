from datetime import datetime


class CallRecord:
    def __init__(self, number, duration, cost, timestamp=None):
        self.number = number
        self.duration = duration
        self.cost = float(cost)
        self.timestamp = timestamp or datetime.now()


class PrepaidPhone:
    # Define call rates for different types
    CALL_RATES = {
        'local': 0.20,  # $0.20 per minute
        'mobile': 0.30,  # $0.30 per minute
        'international': 1.00  # $1.00 per minute
    }

    SMS_COST = 0.20  # $0.20 per SMS
    MAX_BALANCE = 100.00  # Maximum allowed balance

    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.balance = 0.0
        self.call_history = []
        self.sms_count = 0

    def add_credit(self, amount):
        """
        Add credit to the phone balance
        Returns True if successful, False if operation would exceed maximum balance
        """
        amount = float(amount)

        if self.balance + amount > self.MAX_BALANCE:
            return False

        self.balance += amount
        # Round to 2 decimal places to avoid floating point precision issues
        self.balance = round(self.balance, 2)
        return True

    def make_call(self, destination_number, duration, call_type='local'):
        """
        Attempt to make a call
        Returns True if successful, False if insufficient balance
        """
        # Calculate call cost based on duration and type
        duration_minutes = float(duration)
        rate = self.CALL_RATES.get(call_type, self.CALL_RATES['local'])
        cost = duration_minutes * rate
        # Round cost to 2 decimal places
        cost = round(cost, 2)

        if self.balance >= cost:
            # Deduct the cost and record the call
            self.balance -= cost
            self.balance = round(self.balance, 2)
            call_record = CallRecord(destination_number, duration, cost)
            self.call_history.append(call_record)
            return True

        return False

    def send_sms(self):
        """
        Attempt to send an SMS
        Returns True if successful, False if insufficient balance
        """
        if self.balance >= self.SMS_COST:
            self.balance -= self.SMS_COST
            self.balance = round(self.balance, 2)
            self.sms_count += 1
            return True

        return False

    def get_balance(self):
        """Return current balance"""
        return self.balance

    def get_call_history(self):
        """Return list of all calls made"""
        return self.call_history

    def get_total_call_cost(self):
        """Calculate total cost of all calls"""
        total = sum(call.cost for call in self.call_history)
        return round(total, 2)

    def attempt_call_with_cost(self, cost):
        """
        Attempt to make a call with a specific cost (for testing purposes)
        Returns True if successful, False if insufficient balance
        """
        cost = float(cost)

        if self.balance >= cost:
            self.balance -= cost
            self.balance = round(self.balance, 2)
            call_record = CallRecord("unknown", 0, cost)
            self.call_history.append(call_record)
            return True

        return False

    def add_call_to_history(self, number, duration, cost):
        """
        Add a call record to history (for testing purposes)
        """
        call_record = CallRecord(number, duration, cost)
        self.call_history.append(call_record)
        # Deduct from balance to simulate actual call
        self.balance -= float(cost)
        self.balance = round(self.balance, 2)

    def perform_operations(self, operations):
        """
        Perform a sequence of operations and return final balance
        """
        for operation in operations:
            op_type = operation['operation']
            amount = float(operation['amount'])

            if op_type == 'call':
                # For simplicity, we use the amount as cost directly
                self.attempt_call_with_cost(amount)
            elif op_type == 'sms':
                self.send_sms()
            elif op_type == 'topup':
                self.add_credit(amount)

        return self.balance