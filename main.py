from tkinter import *
from tkinter import ttk
import json
import datetime
import math

root = Tk()
root.title("Swedbank")
root.geometry("390x844")  
root.configure(bg='white')


Konts = {}
Krājkonts = {}
Transaction_history = []
current_view = None
views = {}

def save_accounts():
    data = {
        "konts": Konts,
        "krajkonts": Krājkonts,
        "transactions": Transaction_history
    }
    with open("konti.txt", "w") as f:
        json.dump(data, f, indent=4)

def load_accounts():
    global Konts, Krājkonts, Transaction_history
    try:
        with open("konti.txt", "r") as f:
            data = json.load(f)
            Konts = data["konts"]
            Krājkonts = data["krajkonts"]
            Transaction_history = data["transactions"]
    except (FileNotFoundError, json.JSONDecodeError):
        Konts = {"LV16HABA0551052320753": 0}
        Krājkonts = {"LV59HABA0552060057732": 0}
        Transaction_history = []
        save_accounts()

load_accounts()

def add_transaction(account, amount, description=""):
    transaction_record = {
        "account": account,
        "amount": amount,
        "date": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M"),
        "description": description
    }
    Transaction_history.insert(0, transaction_record)
    save_accounts()

def calculate_total_expenses():
    total_expenses = 0
    for transaction in Transaction_history:
        if transaction["amount"] < 0:
            total_expenses += abs(transaction["amount"])
    return total_expenses

class View(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        self.pack_propagate(False)
        self.grid_propagate(False)

class OverviewView(View):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        header = Frame(self, bg='white')
        header.pack(fill=X, padx=20, pady=(20,0))
        
        Label(header, text="Overview", font=('Arial', 24, 'bold'), bg='white', fg='black').pack(anchor=W)

        accounts_frame = Frame(self, bg='white')
        accounts_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(accounts_frame, text="Accounts", font=('Arial', 16, 'bold'), bg='white').pack(anchor=W)
        
        for account, balance in Konts.items():
            account_frame = Frame(accounts_frame, bg='white', pady=10)
            account_frame.pack(fill=X)
            
            account_label = Label(account_frame, text=account, font=('Arial', 14), 
                                bg='white', cursor="hand2")
            account_label.pack(anchor=W)
            account_label.bind("<Button-1>", lambda e, acc=account: show_account(acc))
            
            Label(account_frame, text=f"{balance:.2f} EUR", 
                  font=('Arial', 14, 'bold'), bg='white').pack(anchor=W)
        
        for account, balance in Krājkonts.items():
            account_frame = Frame(accounts_frame, bg='white', pady=10)
            account_frame.pack(fill=X)
            
            account_label = Label(account_frame, text=account, font=('Arial', 14), 
                                bg='white', cursor="hand2")
            account_label.pack(anchor=W)
            account_label.bind("<Button-1>", lambda e, acc=account: show_account(acc))
            
            Label(account_frame, text=f"{balance:.2f} EUR", 
                  font=('Arial', 14, 'bold'), bg='white').pack(anchor=W)

        expenses_frame = Frame(self, bg='white')
        expenses_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(expenses_frame, text="Expenses", font=('Arial', 16, 'bold'), bg='white').pack(anchor=W)
        
        total_expenses = sum(abs(t['amount']) for t in Transaction_history if t['amount'] < 0)
        Label(expenses_frame, text=f"{total_expenses:.2f} EUR", 
              font=('Arial', 24, 'bold'), bg='white', fg='#FF6600').pack(anchor=W)
        
        detailed_label = Label(expenses_frame, text="Detailed view", 
                             font=('Arial', 12), bg='white', fg='#FF6600', cursor="hand2")
        detailed_label.pack(anchor=W)
        detailed_label.bind("<Button-1>", lambda e: show_expenses())

class AccountView(View):
    def __init__(self, parent, account_number):
        super().__init__(parent)
        self.account_number = account_number
        self.setup_ui()

    def setup_ui(self):
        header = Frame(self, bg='white')
        header.pack(fill=X, padx=20, pady=(20,0))
        
        Button(header, text="←", font=('Arial', 20), bg='white', bd=0, command=show_overview).pack(side=LEFT)
        Label(header, text=self.account_number, font=('Arial', 14), bg='white').pack(side=LEFT, padx=10)
        
        balance_frame = Frame(self, bg='white')
        balance_frame.pack(fill=X, padx=20, pady=(20,0))
        
        balance = Konts.get(self.account_number, 0) if self.account_number in Konts else Krājkonts.get(self.account_number, 0)
        Label(balance_frame, text=f"{balance:.2f}", font=('Arial', 36, 'bold'), bg='white').pack(anchor=W)
        Label(balance_frame, text="EUR", font=('Arial', 16), bg='white').pack(anchor=W)
        
        Label(self, text="Transactions", font=('Arial', 16, 'bold'), bg='white').pack(anchor=W, padx=20)
        
        transactions_frame = Frame(self, bg='white')
        transactions_frame.pack(fill=X, padx=20)
        
        for transaction in Transaction_history:
            if transaction["account"] == self.account_number:
                trans_item = Frame(transactions_frame, bg='white')
                trans_item.pack(fill=X, pady=5)
                
                Label(trans_item, text=transaction.get("description", "Transaction"), bg='white').pack(anchor=W)
                amount = transaction["amount"]
                color = "green" if amount > 0 else "red"
                Label(trans_item, text=f"{amount:+.2f} EUR", fg=color, bg='white').pack(anchor=W)

class ExpensesView(View):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        header = Frame(self, bg='white')
        header.pack(fill=X, padx=20, pady=(20,0))
        
        Label(header, text="Expenses", font=('Arial', 24, 'bold'), bg='white', fg='black').pack(anchor=W)
        
        expenses_frame = Frame(self, bg='white')
        expenses_frame.pack(fill=BOTH, expand=True, padx=20, pady=(20,0))
        
        canvas = Canvas(expenses_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(expenses_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        total_expenses = 0
        for transaction in Transaction_history:
            amount = transaction['amount']
            if amount < 0:
                total_expenses += abs(amount)
                
                transaction_frame = Frame(scrollable_frame, bg='white', pady=10)
                transaction_frame.pack(fill=X)
                
                Label(transaction_frame, text=transaction['date'], 
                      font=('Arial', 12), bg='white', fg='gray').pack(anchor=W)
                      
                description_text = transaction['description']
                if description_text.startswith("Payment to "):
                    description_text = description_text.replace("Payment to ", "")
                    if ": " in description_text:
                        account, desc = description_text.split(": ", 1)
                        description_text = f"Payment to {account}\n{desc}"
                
                Label(transaction_frame, text=description_text,
                      font=('Arial', 14), bg='white').pack(anchor=W)
                      
                amount_color = '#FF6600' if amount < 0 else 'green'
                Label(transaction_frame, text=f"{abs(amount):.2f} EUR",
                      font=('Arial', 14, 'bold'), bg='white', 
                      fg=amount_color).pack(anchor=W)
                      
                ttk.Separator(scrollable_frame, orient='horizontal').pack(fill=X, pady=(5,0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        total_frame = Frame(self, bg='white')
        total_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(total_frame, text="Total Expenses:",
              font=('Arial', 16), bg='white').pack(side=LEFT)
        Label(total_frame, text=f"{total_expenses:.2f} EUR",
              font=('Arial', 16, 'bold'), bg='white', fg='#FF6600').pack(side=LEFT, padx=(10,0))

class TransfersView(View):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        header = Frame(self, bg='white')
        header.pack(fill=X, padx=20, pady=(20,0))
        
        Label(header, text="Transfers", font=('Arial', 24, 'bold'), bg='white', fg='black').pack(anchor=W)

        operation_frame = Frame(self, bg='white')
        operation_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(operation_frame, text="Operation Type", font=('Arial', 14), bg='white').pack(anchor=W)
        self.operation_var = StringVar(self)
        self.operation_var.set("Transfer")
        operation_menu = OptionMenu(operation_frame, self.operation_var, "Transfer", "Transaction", 
                                  command=self.update_operation_view)
        operation_menu.config(bg='white', bd=1, relief=SOLID)
        operation_menu.pack(fill=X, pady=(5,0))

        self.transfer_frame = Frame(self, bg='white')
        self.transfer_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(self.transfer_frame, text="From Account", font=('Arial', 14), bg='white').pack(anchor=W)
        self.from_var = StringVar(self)
        accounts = list(Konts.keys()) + list(Krājkonts.keys())
        if accounts:
            self.from_var.set(accounts[0])
        from_menu = OptionMenu(self.transfer_frame, self.from_var, *accounts)
        from_menu.config(bg='white', bd=1, relief=SOLID)
        from_menu.pack(fill=X, pady=(5,0))

        Label(self.transfer_frame, text="To Account", font=('Arial', 14), bg='white').pack(anchor=W)
        self.to_var = StringVar(self)
        if len(accounts) > 1:
            self.to_var.set(accounts[1])
        else:
            self.to_var.set(accounts[0])
        to_menu = OptionMenu(self.transfer_frame, self.to_var, *accounts)
        to_menu.config(bg='white', bd=1, relief=SOLID)
        to_menu.pack(fill=X, pady=(5,0))

        self.transaction_frame = Frame(self, bg='white')
        
        Label(self.transaction_frame, text="Transaction Type", font=('Arial', 14), bg='white').pack(anchor=W)
        self.transaction_type_var = StringVar(self)
        self.transaction_type_var.set("Income")
        transaction_type_menu = OptionMenu(self.transaction_frame, self.transaction_type_var, "Income", "Expense")
        transaction_type_menu.config(bg='white', bd=1, relief=SOLID)
        transaction_type_menu.pack(fill=X, pady=(5,0))

        Label(self.transaction_frame, text="Your Account", font=('Arial', 14), bg='white').pack(anchor=W)
        self.your_account_var = StringVar(self)
        if accounts:
            self.your_account_var.set(accounts[0])
        your_account_menu = OptionMenu(self.transaction_frame, self.your_account_var, *accounts)
        your_account_menu.config(bg='white', bd=1, relief=SOLID)
        your_account_menu.pack(fill=X, pady=(5,0))

        Label(self.transaction_frame, text="Other Party Account", font=('Arial', 14), bg='white').pack(anchor=W)
        self.account_entry = Entry(self.transaction_frame, font=('Arial', 16), bd=1, relief=SOLID)
        self.account_entry.pack(fill=X, pady=(5,0))

        amount_frame = Frame(self, bg='white')
        amount_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(amount_frame, text="Amount (EUR)", font=('Arial', 14), bg='white').pack(anchor=W)
        self.amount_entry = Entry(amount_frame, font=('Arial', 16), bd=1, relief=SOLID)
        self.amount_entry.pack(fill=X, pady=(5,0))

        description_frame = Frame(self, bg='white')
        description_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(description_frame, text="Description", font=('Arial', 14), bg='white').pack(anchor=W)
        self.description_entry = Entry(description_frame, font=('Arial', 16), bd=1, relief=SOLID)
        self.description_entry.pack(fill=X, pady=(5,0))

        button_frame = Frame(self, bg='white')
        button_frame.pack(fill=X, padx=20, pady=(20,0))
        
        self.status_label = Label(button_frame, text="", font=('Arial', 12), bg='white')
        self.status_label.pack(pady=(0,10))
        
        self.action_button = Button(button_frame, text="Transfer", font=('Arial', 14), 
                                  bg='#FF6600', fg='white', bd=0,
                                  command=self.process_operation)
        self.action_button.pack(fill=X, ipady=10)

    def update_operation_view(self, *args):
        if self.operation_var.get() == "Transfer":
            self.transaction_frame.pack_forget()
            self.transfer_frame.pack(fill=X, padx=20, pady=(20,0))
            self.action_button.config(text="Transfer")
        else:
            self.transfer_frame.pack_forget()
            self.transaction_frame.pack(fill=X, padx=20, pady=(20,0))
            self.action_button.config(text="Add Transaction")

    def process_operation(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            
            if self.operation_var.get() == "Transfer":
                self.make_transfer(amount, description)
            else:
                self.make_transaction(amount, description)
                
        except ValueError:
            self.status_label.config(text="Please enter a valid amount", fg='red')

    def make_transfer(self, amount, description):
        from_acc = self.from_var.get()
        to_acc = self.to_var.get()
        
        if amount <= 0:
            self.status_label.config(text="Please enter a positive amount", fg='red')
            return
            
        if from_acc == to_acc:
            self.status_label.config(text="Cannot transfer to the same account", fg='red')
            return

        from_dict = Konts if from_acc in Konts else Krājkonts
        to_dict = Konts if to_acc in Konts else Krājkonts
        
        if from_dict[from_acc] < amount:
            self.status_label.config(text="Insufficient funds", fg='red')
            return
        
        from_dict[from_acc] -= amount
        to_dict[to_acc] += amount
        
        add_transaction(from_acc, -amount, f"Transfer to {to_acc}: {description}")
        add_transaction(to_acc, amount, f"Transfer from {from_acc}: {description}")
        
        self.amount_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.status_label.config(text="Transfer successful", fg='green')
        
        save_accounts()

    def make_transaction(self, amount, description):
        your_account = self.your_account_var.get()
        other_account = self.account_entry.get().strip()
        
        if not other_account:
            self.status_label.config(text="Please enter the other party's account number", fg='red')
            return
            
        if self.transaction_type_var.get() == "Expense":
            amount = abs(amount)  
            account_dict = Konts if your_account in Konts else Krājkonts
            
            if your_account in Konts:
                rounded_amount = math.ceil(amount)
                savings_amount = rounded_amount - amount
        
                if account_dict[your_account] < rounded_amount:
                    self.status_label.config(text="Insufficient funds (including roundup)", fg='red')
                    return
                    
                account_dict[your_account] -= rounded_amount
                add_transaction(your_account, -amount, f"Payment to {other_account}: {description}")
                add_transaction(other_account, amount, f"Payment from {your_account}: {description}")
                
                savings_account = list(Krājkonts.keys())[0]  
                Krājkonts[savings_account] += savings_amount
                add_transaction(your_account, -savings_amount, f"Roundup savings transfer")
                add_transaction(savings_account, savings_amount, f"Roundup from expense to {other_account}")
                
            else:
                if account_dict[your_account] < amount:
                    self.status_label.config(text="Insufficient funds", fg='red')
                    return
                    
                account_dict[your_account] -= amount
                add_transaction(your_account, -amount, f"Payment to {other_account}: {description}")
                add_transaction(other_account, amount, f"Payment from {your_account}: {description}")
        else:
            amount = abs(amount)
            account_dict = Konts if your_account in Konts else Krājkonts
            account_dict[your_account] += amount
            add_transaction(your_account, amount, f"Income from {other_account}: {description}")
            add_transaction(other_account, -amount, f"Payment to {your_account}: {description}")
        
        self.amount_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.account_entry.delete(0, END)
        self.status_label.config(text="Transaction added successfully", fg='green')
        
        save_accounts()

def show_overview():
    global current_view
    if current_view:
        current_view.pack_forget()
    current_view = OverviewView(root)
    current_view.pack(fill=BOTH, expand=True)

def show_account(account_number):
    global current_view
    if current_view:
        current_view.pack_forget()
    current_view = AccountView(root, account_number)
    current_view.pack(fill=BOTH, expand=True)

def show_expenses():
    global current_view
    if current_view:
        current_view.destroy()
    current_view = ExpensesView(root)
    current_view.pack(fill=BOTH, expand=True)

def show_transfers():
    global current_view
    if current_view:
        current_view.pack_forget()
    current_view = TransfersView(root)
    current_view.pack(fill=BOTH, expand=True)

nav_bar = Frame(root, bg='#F8F8F8', height=50)
nav_bar.pack(side=BOTTOM, fill=X)

nav_items = [
    ("Overview", "overview.png", show_overview),
    ("Transfers", "transfers.png", show_transfers),
    ("Cards", "cards.png", lambda: None),
    ("Services", "services.png", lambda: None),
    ("Contacts", "contacts.png", lambda: None)
]

for text, icon, command in nav_items:
    btn = Button(nav_bar, text=text, bg='#F8F8F8', bd=0, command=command)
    btn.pack(side=LEFT, expand=True, pady=10)

show_overview()

root.mainloop()
