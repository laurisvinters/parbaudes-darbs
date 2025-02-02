from tkinter import *
from tkinter import ttk
import math
import json
from datetime import datetime

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
        Konts = {"LV16HABA0551052320753": 22.20}
        Krājkonts = {"LV59HABA0552060057732": 990.24}
        Transaction_history = []
        save_accounts()

load_accounts()

def add_transaction(account, amount, description=""):
    transaction_record = {
        "account": account,
        "amount": amount,
        "date": datetime.now().strftime("%d/%m/%Y, %H:%M"),
        "description": description
    }
    Transaction_history.insert(0, transaction_record)
    save_accounts()

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
        
        account_frame = Frame(self, bg='white')
        account_frame.pack(fill=X, padx=20, pady=(20,0))
        
        for acc_num, balance in Konts.items():
            Label(account_frame, text=acc_num, font=('Arial', 12), bg='white', fg='gray').pack(anchor=W)
            Label(account_frame, text=f"{balance:.2f} EUR", font=('Arial', 16, 'bold'), bg='white').pack(anchor=W)
        
        savings_frame = Frame(self, bg='white')
        savings_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(savings_frame, text="Savings", font=('Arial', 16), bg='white').pack(anchor=W)
        for acc_num, balance in Krājkonts.items():
            Label(savings_frame, text=f"{balance:.2f} EUR", font=('Arial', 16, 'bold'), bg='white').pack(anchor=W)
        
        expenses_frame = Frame(self, bg='white')
        expenses_frame.pack(fill=X, padx=20, pady=(20,0))
        
        exp_header = Frame(expenses_frame, bg='white')
        exp_header.pack(fill=X)
        Label(exp_header, text="Expenses", font=('Arial', 16), bg='white').pack(side=LEFT)
        Label(exp_header, text="Detailed view", font=('Arial', 12), bg='white', fg='#007AFF').pack(side=RIGHT)
        
        Label(expenses_frame, text="This month", font=('Arial', 12), bg='white', fg='gray').pack(anchor=W)
        Label(expenses_frame, text="189.22 EUR", font=('Arial', 16, 'bold'), bg='white').pack(anchor=W)

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
        
        balance = Konts.get(self.account_number, 0)
        Label(balance_frame, text=f"{balance:.2f}", font=('Arial', 36, 'bold'), bg='white').pack(anchor=W)
        Label(balance_frame, text="EUR", font=('Arial', 16), bg='white').pack(anchor=W)

        Button(self, text="Request", font=('Arial', 12), bg='#FFF5E6', fg='black', bd=0, padx=20, pady=10).pack(pady=20)
        
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

nav_bar = Frame(root, bg='#F8F8F8', height=50)
nav_bar.pack(side=BOTTOM, fill=X)

nav_items = [
    ("Overview", "overview.png"),
    ("Transfers", "transfers.png"),
    ("Cards", "cards.png"),
    ("Services", "services.png"),
    ("Contacts", "contacts.png")
]

for text, icon in nav_items:
    btn = Button(nav_bar, text=text, bg='#F8F8F8', bd=0)
    btn.pack(side=LEFT, expand=True, pady=10)

show_overview()

root.mainloop()
