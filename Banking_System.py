class Banking_System:
    balance = 0

    def __init__(self):
        print("Welcome Customer")
    
    def credit(self, amount):
        self.balance += amount
        print(amount, " Credited Successfully")
    
    def debit(self, amount):
        if self.balance < amount:
            print("Insufficient Balance")
            return
        
        self.balance -= amount
        print("Amount debited successfully")
        print("Your current balance is: ", self.balance)
    
    def check_balance(self):
        print("Your Balance: ", self.balance)

account = Banking_System()
i = 0

while(i < 4):
    print("1    Credit")
    print("2    Debit")
    print("3    Check Balance")
    print("4    Exit")
    i = int(input("Enter your choice: "))

    if i == 1:
        temp = int(input("Enter the amount you want to Credit: "))
        account.credit(temp)
    
    elif i == 2:
        temp = int(input("Enter the amount you want to debit: "))
        account.debit(temp)

    elif i == 3:
        account.check_balance()
    
    elif i == 4:
        break

    else:
        print("Enter valid choice")
    
print("Thankyou for using our services")