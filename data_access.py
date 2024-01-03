import os
from components import Account

class DataAccess:
    def __init__(self) -> None:
        if not os.path.exists('accounts.txt'):
            with open('accounts.txt','x'):
                pass

    # Account CRUD
    def create_account(self, account_pin: str) -> None:
        with open('accounts.txt', 'a') as file:
            file.write(f'{account_pin}:0:\n')

    def read_account(self, account_pin: str) -> Account|None:
        with open('accounts.txt', 'r') as file:
            for line in file:
                account = line.split(':')
                if account_pin == account[0]:
                    pin = int(account[0])
                    balance = float(account[1])
                    return Account(pin, balance)
            return None
    
    def update_account(self, account: Account) -> None:
        with open('accounts.txt', 'r') as file:
            all_accounts = file.readlines()
        index = 0
        while index < len(all_accounts):
            if all_accounts[index].split(':')[0] == account._pin:
                all_accounts[index] = f'{account._pin}:{account._balance}:\n'
                break
            index += 1
        with open('accounts.txt', 'w') as file:
            for row in all_accounts:
                file.write(row)

    
    # Transaction CRUD
    def create_transaction(self, account_pin: str, date: str, value: str, descriptor: str) -> None:
        with open(f'{account_pin}.txt', 'a') as file:
            file.write(f'{date},{account_pin},{value},{descriptor},\n')
    
    def read_all_transactions(self, account_pin: str) -> list[str]:
        with open(f'{account_pin}.txt', 'r') as file:
            return file.readlines()