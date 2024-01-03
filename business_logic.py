from components import Account
from datetime import date
from data_access import DataAccess

class BusinessLogic:
    def __init__(self) -> None:
        self._dal = DataAccess()

    def create_account(self, account_pin: str) -> bool:
        if self._dal.read_account(account_pin):
            return False
        else:
            self._dal.create_account(account_pin)
            today = date.today().strftime('%d%m%Y')
            self._dal.create_transaction(account_pin, today, 0, 'Account created')
            return True
    
    def login(self, account_pin: str) -> Account|None:
        return self._dal.read_account(account_pin)
    
    def withdrawal(self, account: Account, amount: float) -> bool:
        if amount > account._balance:
            return False
        elif amount < 0:
            return False
        else:
            account._balance -= amount
            today = date.today().strftime('%d%m%Y')
            self._dal.create_transaction(account._pin, today, str(amount), 'Withdraw')
            self._dal.update_account(account)
            return True
    
    def deposit(self, account: Account, amount: float) -> bool:
        if amount < 0:
            return False
        else:
            account._balance += amount
            today = date.today().strftime('%d%m%Y')
            self._dal.create_transaction(account._pin, today, str(amount), 'Deposit')
            self._dal.update_account(account)
            return True
    
    def get_transactions(self, account: Account) -> list[dict[str, str]]:
        all_transactions = self._dal.read_all_transactions(account._pin)
        index = 0
        while index < len(all_transactions):
            old_row = all_transactions[index].split(',')
            new_row = {}
            new_row['date'] = old_row[0]
            new_row['account'] = old_row[1]
            new_row['amount'] = old_row[2]
            new_row['descriptor'] = old_row[3]
            all_transactions[index] = new_row
            index += 1
        return all_transactions