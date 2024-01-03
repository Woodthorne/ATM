import os
from business_logic import BusinessLogic
from components import Account

class Interface:
    def __init__(self, bank_name: str = 'Test Bank') -> None:
        self._bank_name = bank_name
        self._bll = BusinessLogic()

    def main_menu(self) -> None:
        while True:
            self._print_menu(f'{self._bank_name.upper()} - Main Menu',
                            options = ['Create Account', 'Manage Account'],
                            escape = 'Quit')
            menu_opt = input('>>> ')
            if menu_opt == '0':
                quit()
            elif menu_opt == '1':
                self._create_account()
            elif menu_opt == '2':
                self._manage_account()
            else:
                input('Invalid option. Press [ENTER] to continue...')
    
    def _create_account(self) -> None:
        while True:
            self._print_menu(f'{self._bank_name.upper()} - Create Account',
                             listing = ['Enter desired account PIN'],
                             escape = 'Cancel and return to main menu')
            menu_opt = input('>>> ')
            if menu_opt == '0':
                return
            else:
                try:
                    desired_pin = int(menu_opt)
                    if desired_pin < 1:
                        input('Account PIN may only contain numbers. Press [ENTER] to continue...')
                    elif not self._bll.create_account(str(desired_pin)):
                        input('Account already exists. Press [ENTER] to continue...')
                    else:    
                        input('Account created. Press [ENTER] to continue...')
                        return
                except ValueError:
                    input('Account PIN must be numeric. Press [ENTER] to continue...')

    def _manage_account(self) -> None:
        while True:
            self._print_menu(f'{self._bank_name.upper()} - Manage Account',
                             listing = ['Enter account PIN'],
                             escape = 'Cancel and return to main menu')
            menu_opt = input('>>> ')
            if menu_opt == '0':
                return
            else:
                try:
                    account = self._bll.login(str(menu_opt))
                    if account:
                        break
                    else:    
                        input('No account with that PIN. Press [ENTER] to continue...')
                        return
                except ValueError:
                    input('Account PIN must be numeric. Press [ENTER] to continue...')

        while True:
            self._print_menu(f'{self._bank_name.upper()} - Manage Account #{account._pin}',
                             options = ['Withdraw From Account',
                                        'Deposit To Account',
                                        'Show Account Balance',
                                        'List Account Transactions'
                                        ],
                             escape = 'Return To Main Menu'
                             )
            menu_opt = input('>>> ')
            if menu_opt == '0':
                return
            elif menu_opt == '1':
                self._withdraw_from(account)
            elif menu_opt == '2':
                self._deposit_to(account)
            elif menu_opt == '3':
                self._show_balance(account)
            elif menu_opt == '4':
                self._list_transactions(account)
            else:
                input('Invalid option. Press [ENTER] to continue...')

    def _withdraw_from(self, account: Account) -> None:
        self._print_menu(f'{self._bank_name.upper()} - Manage Account #{account._pin}',
                         listing = ['Enter amount to withdraw from account'],
                         escape = 'Return to Account Management')
        menu_opt = input('>>> ')
        if menu_opt == '0':
            return
        else:
            try:
                amount = float(menu_opt)
                if self._bll.withdrawal(account, amount):
                    input('Withdrawal successful. Press [ENTER] to return to account menu...')
                    return
                else:
                    input('Amount must be between balance and zero. Press [ENTER] to continue...')
            except ValueError:
                input('Amount must be numeric. Press [ENTER] to continue...')

    def _deposit_to(self, account: Account) -> None:
        self._print_menu(f'{self._bank_name.upper()} - Manage Account #{account._pin}',
                         listing = ['Enter amount to deposit to account'],
                         escape = 'Return to Account Management')
        menu_opt = input('>>> ')
        if menu_opt == '0':
            return
        else:
            try:
                amount = float(menu_opt)
                if self._bll.deposit(account, amount):
                    input('Deposit successful. Press [ENTER] to return to account menu...')
                    return
                else:
                    input('Amount must greater than zero. Press [ENTER] to continue...')
            except ValueError:
                input('Amount must be numeric. Press [ENTER] to continue...')

    def _show_balance(self, account: Account) -> None:
        self._print_menu(f'{self._bank_name.upper()} - Manage Account #{account._pin}',
                         listing = [f'"Balance"{f"{account._balance}".rjust(35, ".")}',
                                    'Press [ENTER] to continue...'])
        input() 

    def _list_transactions(self, account: Account) -> None:
        all_transactions = self._bll.get_transactions(account)
        amount_len = 0
        descriptor_len = 0
        for transaction in all_transactions:
            if len(transaction['amount']) > amount_len:
                amount_len = len(transaction['amount'])
            if len(transaction['descriptor']) > descriptor_len:
                descriptor_len = len(transaction['descriptor'])

        listing: list[str] = []
        for transaction in all_transactions:
            row = ''
            row += transaction['date']
            row += f'|{transaction["account"]}'
            row += f'|{transaction["amount"].rjust(amount_len)}'
            row += f'|{transaction["descriptor"].rjust(descriptor_len)}'
            print(row)
            print(listing)
            listing.append(row)
        listing.append('Press [ENTER] to continue...')

        self._print_menu(f'{self._bank_name.upper()} - Manage Account #{account._pin}',
                         description = 'Transaction history',
                         listing = listing)
        input()

    def _print_menu(self,
                    header: str,
                    menu_width: int = 6,
                    description: str = None,
                    listing: list[str] = None,
                    options: list[str] = None,
                    escape: str = None
                    ) -> None:
        
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        
        if len(header) > 2:
            menu_width += len(header) - 2
        if listing:
            for item in listing:
                if len(item) + 4 > menu_width:
                    menu_width = len(item) + 4
        if options:
            for item in options:
                if len(item) + 7 > menu_width:
                    menu_width = len(item) + 7
        if escape and len(escape) + 7 > menu_width:
            menu_width = len(escape) + 7
        content_width = menu_width - 4

        print(f'=={header}{"=" * (content_width - len(header))}==')
        option_num = 0
        if description:
            if len(description) <= content_width:
                padding = content_width - len(description)
                print(f'| {description}{" " * padding} |')
            else:
                split_description = description.split(' ')
                while split_description:
                    current_row = ''
                    while split_description and len(current_row) \
                                                + len(split_description[0]) \
                                                + 1 \
                                                    <= content_width:
                        current_row += ' ' + split_description.pop(0)
                    padding = content_width - len(current_row)
                    print(f'| {current_row}{" " * padding} |')
            print('=' * menu_width)
        
        if listing:
            for item in listing:
                padding = content_width - len(item)
                print(f'| {item}{" " * padding} |')
            print('=' * menu_width)

        if options:
            for item in options:
                option_num += 1
                padding = content_width - len(item) - 3
                print(f'| {option_num}. {item}{" " * padding} |')
        if escape:
            padding = content_width - len(escape) - 2
            print(f'| 0. {escape}{" " * padding}|')
        if options or escape:
            print('=' * menu_width)

