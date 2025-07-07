class Banking_System:
    def __init__(self, balance):
        self.balance = balance
        print("Welcome Customer")
    
    def credit(self, amount):
        self.balance += amount
        return self.balance
    
    def debit(self, amount):
        if self.balance < amount:
            raise ValueError("Insufficient Balance")
        self.balance -= amount
        return self.balance
    
    def check_balance(self):
        return self.balance
