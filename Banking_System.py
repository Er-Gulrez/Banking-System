class Banking_System:
    def __init__(self):
        self.balance = 0
        print("Welcome Customer")
    
    def credit(self, amount):
        self.balance += amount
        print("Your balance is: ", self.balance)
    
    def debit(self, amount):
        # if self.balance < amount:
        #     print("Insufficient Balance")
        #     return
        
        self.balance -= amount
        return self.balance
    
    def check_balance(self):
        print("Your Balance: ", self.balance)