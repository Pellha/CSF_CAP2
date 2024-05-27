import os
import string
import random

class Account:
    def __init__(self, num, bal, typ):
        self.num = num
        self.bal = bal
        self.typ = typ

    def deposit(self, amount):
        self.bal += amount
        return self.bal

    def withdraw(self, amount):
        if self.bal >= amount:
            self.bal -= amount
            return self.bal
        else:
            return "Insufficient funds"

    def __str__(self):
        return f"Account Number: {self.num}\nBalance: {self.bal}\nAccount Type: {self.typ}"

class PersonalAccount(Account):
    def __init__(self, num, bal):
        super().__init__(num, bal, "Personal")

class BusinessAccount(Account):
    def __init__(self, num, bal):
        super().__init__(num, bal, "Business")

class Bank:
    def __init__(self):
        self.accts = {}
        self.load_accts()

    def load_accts(self):
        if os.path.exists("accts.txt"):
            with open("accts.txt", "r") as file:
                for line in file:
                    acct_info = line.strip().split(',')
                    acct_num = acct_info[0]
                    bal = float(acct_info[1])
                    typ = acct_info[2]
                    if typ == "Personal":
                        self.accts[acct_num] = PersonalAccount(acct_num, bal)
                    elif typ == "Business":
                        self.accts[acct_num] = BusinessAccount(acct_num, bal)

    def save_accts(self):
        with open("accts.txt", "w") as file:
            for acct_num, acct in self.accts.items():
                file.write(f"{acct_num},{acct.bal},{acct.typ}\n")

    def create_acct(self, typ):
        acct_num = ''.join(random.choices(string.digits, k=8))
        if typ == "Personal":
            acct = PersonalAccount(acct_num, 0)
        elif typ == "Business":
            acct = BusinessAccount(acct_num, 0)
        self.accts[acct_num] = acct
        self.save_accts()
        return acct

    def login(self, acct_num):
        return self.accts.get(acct_num)

def main():
    bank = Bank()

    while True:
        print("1. Create an Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            typ = input("Enter account type (Personal/Business): ").capitalize()
            if typ in ["Personal", "Business"]:
                acct = bank.create_acct(typ)
                print(f"Account created!\nYour account number is: {acct.num}")
            else:
                print("Invalid! Please enter either Personal or Business.")

        elif choice == "2":
            acct_num = input("account number: ")
            acct = bank.login(acct_num)
            if acct:
                print("Login successful")
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. View Balance")
                    print("4. Logout")
                    option = input("Enter your choice: ")
                    if option == "1":
                        amount = float(input("Enter amount: "))
                        print("New Balance:", acct.deposit(amount))
                    elif option == "2":
                        amount = float(input("Enter amount: "))
                        print(acct.withdraw(amount))
                    elif option == "3":
                        print(acct)
                    elif option == "4":
                        break
                    else:
                        print("wrong choice")
            else:
                print("Invalid account number! Please try again.")

        elif choice == "3":
            print("Thank you")
            break

        else:
            print("Invalid choice! Please enter a valid option.")

if __name__ == "__main__":
    main()
