import os
from datetime import date

if not os.path.exists('accounts.txt'):
    with open('accounts.txt','x'):
        pass

error = {'menu':'Felaktigt menyval. Tryck [RETUR] för att gå tillbaka.',
         'accountNum':'Kontonummer får bara innehålla siffror.',
         'accountTaken':'Kontonummer existerar redan.',
         'accountNone':'Kontot existerar inte.',
         'insufficient':'Otillräckligt med pengar på kontot.',
         'invalidAmount':'Ogiltigt pengavärde. Måste vara hela kronor.'}

def newScreen ():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def printMenu(menuName,*options):
    req_menu_width = 7
    for item in options:
        if len(item) > req_menu_width:
            req_menu_width = len(item)
        
    print(f'{" " * (2 + (req_menu_width - 7) // 2)}BANKOMATEN')
    print(f'=={menuName}{"=" * (5 + req_menu_width - len(menuName))}')
    option_num = 0
    padding = 0
    for item in options:
        option_num += 1
        if len(item) < req_menu_width:
            padding = req_menu_width - len(item)
        print(f'| {option_num}. {item}{" " * padding} |')
        padding = 0
    border_draw = 1
    while border_draw < req_menu_width + 8:
        print('=',end='')
        border_draw += 1
    print()

def main():
    newScreen()
    printMenu('Huvudmeny','[Skapa] konto','[Administrera] konto','[Avsluta]')
    while True:
        opt = input('Menyval: ').lower()
        if opt in ['1','skapa']:
            checkAccount('create')
        elif opt in ['2','administrera']:
            checkAccount('login')
        elif opt in ['3','avsluta']:
            quit()
        else:
            input(error['menu'])
            
def checkAccount(task):
    while True:
        opt = input('Mata in kontonummer eller [avbryt] för att gå tillbaka till menyn: ').lower()
        exists = False
        if opt.isnumeric():
            with open('accounts.txt','r') as f:
                for line in f:
                    line = line.split(':')
                    if opt == line[0] and task == 'create':
                        print(error['accountTaken'])
                        exists = True
                        break
                    elif opt == line[0] and task == 'login':
                        exists = True
                        break
            if task == 'login' and not exists:
                print(error['accountNone'])
            elif task == 'login' and exists:
                admin(opt)
            elif task == 'create' and not exists:
                createAccount(opt)
        elif opt == 'avbryt':
            main()
        else:
            print(error['accountNum'])

def createAccount(account):
    with open('accounts.txt','a') as f:
        f.write(f'{account}:0\n')
    with open(f'{account}.txt','w') as f:
        f.write(f'{date.today()},{account},0,Kontot skapades\n')
    input(f'Konto #{account} skapat. Tryck [RETUR] för att gå till huvudmenyn.')
    main()

def admin(account):
    newScreen()
    printMenu(f'Kontomeny #{account}','Ta [ut] pengar','Sätt [in] pengar','Visa [saldo]','Lista [transaktioner]','[Avsluta] till huvudmeny')
    while True:
        opt = input('Menyval: ').lower()
        if opt in ['1','ut']:
            makeTransaction(account,'withdraw')
        elif opt in ['2','in']:
            makeTransaction(account,'deposit')
        elif opt in ['3','saldo']:
            balance = getBalance(account)
            if balance < 1000:
                print(f'Saldo: {balance} kr')
            else:
                print(f'Saldo: {tidyMoney(str(balance))} kr')
        elif opt in ['4','transaktioner']:
            listTransactions(account)
        elif opt in ['5','avsluta']:
            main()

def makeTransaction(account,task):
    while True:
        opt = input('Mata in önskat värde eller [avbryt] för att avbryta transaktion: ').lower()
        if opt == 'avbryt' or opt == '0':
            admin(account)
        elif opt.isnumeric():
            amount = int(opt)
            if task == 'withdraw':
                balance = getBalance(account)        
                if amount > balance:
                    print(error['insufficient'])
                    continue
                else:
                    updateBalance(account,-amount)
                    with open(f'{account}.txt','a',encoding='utf-8') as f:
                        f.write(f'{date.today()},{account},{amount},Uttag\n')
                    input('Uttagning lyckades. Tryck [RETUR] för att gå tillbaka.')
            elif task == 'deposit':
                updateBalance(account,amount)
                with open(f'{account}.txt','a',encoding='utf-8') as f:
                        f.write(f'{date.today()},{account},{amount},Insättning\n')
                input('Insättning lyckades. Tryck [RETUR] för att gå tillbaka.')
            admin(account)
        else:
            print(error['invalidAmount'])

def getBalance(account):
    with open('accounts.txt','r',encoding='utf-8') as f:
        for line in f:
            line = line.split(':')
            if line[0] == account:
                return int(line[1])

def updateBalance(account,change):
    all_accounts = []
    with open('accounts.txt','r+',encoding='utf') as f:
        for line in f:
            line = line.split(':')
            if line[0] == account:
                line[1] = str(getBalance(account) + change) +'\n'
            all_accounts.append(':'.join(line))
        f.seek(0)
        f.writelines(all_accounts)

def listTransactions(account):
    newScreen()
    transactions = []
    with open(f'{account}.txt','r',encoding='utf-8') as f:
        for line in f:
            transactions.append(line.strip('\n'))  
    index = 0
    req_menu_width = [0,0,0,0]
    for transaction in transactions:
        transactions[index] = transaction.split(',')
        if len(transactions[index][2]) > 3:
            transactions[index][2] = tidyMoney(transactions[index][2])        
        subindex = 0
        for item in transactions[index]:
            if len(item) > req_menu_width[subindex]:
                req_menu_width[subindex] = len(item)
            subindex += 1
        index += 1

    title = f'Transaktioner #{account}'
    print(f'=={title}{"=" * (sum(req_menu_width) - 4 -len(account))}')
    for transaction in transactions:
        index = 0
        for item in transaction:
            print(f'| {item}',end=f'{" " * (req_menu_width[index] - len(item) + 1)}')
            index += 1
        print('|')
    print(f'{"=" * (sum(req_menu_width) + 13)}')
    input('Tryck [RETUR] för att gå tillbaka till kontomeny.')
    admin(account)

def tidyMoney(amount):
    amount = [amount]
    while len(amount[0]) > 3:
        amount.append(amount[0][-3:])
        amount[0] = amount[0][:-3]
    amount.append(amount[0])
    amount.pop(0)
    amount.reverse()
    amount = "'".join(amount)
    return amount

if __name__ == '__main__':
    main()