from tkinter import *
from tkinter import ttk
import json
import datetime
import math

root = Tk()
root.title("Swedbank")
root.geometry("402x874")  
root.configure(bg='white')
root.resizable(False, False)

Konts = {}
Krājkonts = {}
Transaction_history = []
current_view = None
views = {}

def saglabat_kontu():
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
        saglabat_kontu()

load_accounts()

def add_transaction(account, amount, description=""):
    transaction_record = {
        "account": account,
        "amount": amount,
        "date": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M"),
        "description": description
    }
    Transaction_history.insert(0, transaction_record)
    saglabat_kontu()

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
        
        Label(header, text="Pārskats", font=('Arial', 24, 'bold'), bg='white', fg='black').pack(anchor=W)

        accounts_frame = Frame(self, bg='white')
        accounts_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(accounts_frame, text="Konti", font=('Arial', 16, 'bold'), bg='white').pack(anchor=W)

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
            
            daily_interest = (balance * 0.025) / 365
            Label(account_frame, text=f"Procenta summa dienā: {daily_interest:.3f} EUR", 
                  font=('Arial', 12), bg='white', fg='#008800').pack(anchor=W)

        expenses_frame = Frame(self, bg='white')
        expenses_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(expenses_frame, text="Izmaksas", font=('Arial', 16, 'bold'), bg='white').pack(anchor=W)
        
        user_accounts = list(Konts.keys()) + list(Krājkonts.keys())
        total_expenses = sum(abs(t['amount']) for t in Transaction_history 
                           if t['amount'] < 0 and t['account'] in user_accounts)
        Label(expenses_frame, text=f"{total_expenses:.2f} EUR", 
              font=('Arial', 24, 'bold'), bg='white', fg='#FF6600').pack(anchor=W)
        
        detailed_label = Label(expenses_frame, text="Skatīt vairāk", 
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
        
        Label(self, text="Transakcijas", font=('Arial', 16, 'bold'), bg='white').pack(anchor=W, padx=20)
        
        transactions_frame = Frame(self, bg='white')
        transactions_frame.pack(fill=X, padx=20)
        
        for transaction in Transaction_history:
            if transaction["account"] == self.account_number:
                trans_item = Frame(transactions_frame, bg='white')
                trans_item.pack(fill=X, pady=5)
                
                Label(trans_item, text=transaction.get("description", "Transakcijas"), bg='white').pack(anchor=W)
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
        
        Label(header, text="Izmaksas", font=('Arial', 24, 'bold'), bg='white', fg='black').pack(anchor=W)
        
        expenses_frame = Frame(self, bg='white')
        expenses_frame.pack(fill=BOTH, expand=True, padx=20, pady=(20,0))
        
        canvas = Canvas(expenses_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(expenses_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg='white')

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 2))
        scrollbar.pack(side=RIGHT, fill=Y)
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor=NW)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox(ALL)))
        
        total_expenses = 0
        user_accounts = list(Konts.keys()) + list(Krājkonts.keys())
        
        for transaction in Transaction_history:
            amount = transaction['amount']
            account = transaction['account']
            if amount < 0 and account in user_accounts:  # Only show expenses from user's accounts
                total_expenses += abs(amount)
                
                transaction_frame = Frame(scrollable_frame, bg='white', pady=10)
                transaction_frame.pack(fill=X)
                
                Label(transaction_frame, text=transaction['date'], 
                      font=('Arial', 12), bg='white', fg='gray').pack(anchor=W)
                      
                description_text = transaction['description']
                if not description_text:
                    description_text = "Transakcija"
                    
                Label(transaction_frame, text=description_text,
                      font=('Arial', 14), bg='white').pack(anchor=W)
                      
                Label(transaction_frame, text=f"{amount:.2f} EUR",
                      font=('Arial', 14, 'bold'), bg='white', fg='red').pack(anchor=W)
                      
                ttk.Separator(scrollable_frame, orient='horizontal').pack(fill=X, pady=(5,0))
        
        total_frame = Frame(self, bg='white')
        total_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(total_frame, text="Kopējie tēriņi:",
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
        
        Label(header, text="Pārskaitijumi", font=('Arial', 24, 'bold'), bg='white', fg='black').pack(anchor=W)

        operation_frame = Frame(self, bg='white')
        operation_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(operation_frame, text="Darijuma veids", font=('Arial', 14), bg='white').pack(anchor=W)
        self.operation_var = StringVar(self)
        self.operation_var.set("Pārskaitīt")
        operation_menu = OptionMenu(operation_frame, self.operation_var, "Pārskaitīt", "Transakcija", 
                                  command=self.update_operation_view)
        operation_menu.config(bg='white', bd=1, relief=SOLID)
        operation_menu.pack(fill=X, pady=(5,0))

        self.transfer_frame = Frame(self, bg='white')
        self.transfer_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(self.transfer_frame, text="No Konta", font=('Arial', 14), bg='white').pack(anchor=W)
        self.from_var = StringVar(self)
        accounts = list(Konts.keys()) + list(Krājkonts.keys())
        if accounts:
            self.from_var.set(accounts[0])
        from_menu = OptionMenu(self.transfer_frame, self.from_var, *accounts)
        from_menu.config(bg='white', bd=1, relief=SOLID)
        from_menu.pack(fill=X, pady=(5,0))

        Label(self.transfer_frame, text="Uz kontu", font=('Arial', 14), bg='white').pack(anchor=W)
        self.to_var = StringVar(self)
        if len(accounts) > 1:
            self.to_var.set(accounts[1])
        else:
            self.to_var.set(accounts[0])
        to_menu = OptionMenu(self.transfer_frame, self.to_var, *accounts)
        to_menu.config(bg='white', bd=1, relief=SOLID)
        to_menu.pack(fill=X, pady=(5,0))

        self.transaction_frame = Frame(self, bg='white')
        
        Label(self.transaction_frame, text="Darijuma veids", font=('Arial', 14), bg='white').pack(anchor=W)
        self.transaction_type_var = StringVar(self)
        self.transaction_type_var.set("Ienākums")
        transaction_type_menu = OptionMenu(self.transaction_frame, self.transaction_type_var, "Ienākums", "Izmaksa",
                                         command=lambda *args: self.update_recipient_label())
        transaction_type_menu.config(bg='white', bd=1, relief=SOLID)
        transaction_type_menu.pack(fill=X, pady=(5,0))

        Label(self.transaction_frame, text="Tavs Konts", font=('Arial', 14), bg='white').pack(anchor=W)
        self.your_account_var = StringVar(self)
        if accounts:
            self.your_account_var.set(accounts[0])
        your_account_menu = OptionMenu(self.transaction_frame, self.your_account_var, *accounts)
        your_account_menu.config(bg='white', bd=1, relief=SOLID)
        your_account_menu.pack(fill=X, pady=(5,0))

        self.recipient_label = Label(self.transaction_frame, text="Sūta No", font=('Arial', 14), bg='white')
        self.recipient_label.pack(anchor=W)
        self.account_entry = Entry(self.transaction_frame, font=('Arial', 16), bd=1, relief=SOLID)
        self.account_entry.pack(fill=X, pady=(5,0))

        amount_frame = Frame(self, bg='white')
        amount_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(amount_frame, text="Daudzums (EUR)", font=('Arial', 14), bg='white').pack(anchor=W)
        self.amount_entry = Entry(amount_frame, font=('Arial', 16), bd=1, relief=SOLID)
        self.amount_entry.pack(fill=X, pady=(5,0))

        description_frame = Frame(self, bg='white')
        description_frame.pack(fill=X, padx=20, pady=(20,0))
        
        Label(description_frame, text="Apraksts", font=('Arial', 14), bg='white').pack(anchor=W)
        self.description_entry = Entry(description_frame, font=('Arial', 16), bd=1, relief=SOLID)
        self.description_entry.pack(fill=X, pady=(5,0))

        button_frame = Frame(self, bg='white')
        button_frame.pack(fill=X, padx=20, pady=(20,0))
        
        self.status_label = Label(button_frame, text="", font=('Arial', 12), bg='white')
        self.status_label.pack(pady=(0,10))
        
        self.action_button = Button(button_frame, text="Pārskaitīt", font=('Arial', 14), bg='#FFFFFF', fg='black', bd=0, command=self.process_operation)
        self.action_button.pack(fill=X, ipady=10)

    def update_operation_view(self, *args):
        if self.operation_var.get() == "Pārskaitīt":
            self.transaction_frame.pack_forget()
            self.transfer_frame.pack(fill=X, padx=20, pady=(20,0))
            self.action_button.config(text="Pārskaitīt")
        else:
            self.transfer_frame.pack_forget()
            self.transaction_frame.pack(fill=X, padx=20, pady=(20,0))
            self.action_button.config(text="Pievienot transakciju")

    def update_recipient_label(self):
        if self.transaction_type_var.get() == "Ienākums":
            self.recipient_label.config(text="Sūta No")
        else:
            self.recipient_label.config(text="Saņēmējs")

    def process_operation(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            
            if self.operation_var.get() == "Pārskaitīt":
                self.make_transfer(amount, description)
            else:
                self.make_transaction(amount, description)
                
        except ValueError:
            self.status_label.config(text="Ievadi derīgu skaitli", fg='red')

    def make_transfer(self, amount, description):
        from_acc = self.from_var.get()
        to_acc = self.to_var.get()
        
        if amount <= 0:
            self.status_label.config(text="Ievadi pozitīvu skaitli", fg='red')
            return
            
        if from_acc == to_acc:
            self.status_label.config(text="Nevar pārskaitīt uz to pašu kontu", fg='red')
            return

        from_dict = Konts if from_acc in Konts else Krājkonts
        to_dict = Konts if to_acc in Konts else Krājkonts
        
        if from_dict[from_acc] < amount:
            self.status_label.config(text="Nepietiekami līdzekļi", fg='red')
            return
        
        from_dict[from_acc] -= amount
        to_dict[to_acc] += amount
        
        add_transaction(from_acc, -amount, f"Pārskaita uz {to_acc}: {description}")
        add_transaction(to_acc, amount, f"Pārskaita no {from_acc}: {description}")
        
        self.amount_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.status_label.config(text="Pārskaitijums ir veiksmīgs", fg='green')
        
        save_accounts()

    def make_transaction(self, amount, description):
        your_account = self.your_account_var.get()
        other_account = self.account_entry.get().strip()
        
        if not other_account:
            self.status_label.config(text="Ievadi saņēmēja nosaukumu", fg='red')
            return
            
        if self.transaction_type_var.get() == "Izdevmi":
            amount = abs(amount)  
            account_dict = Konts if your_account in Konts else Krājkonts
            
            if your_account in Konts:
                rounded_amount = math.ceil(amount)
                savings_amount = rounded_amount - amount
        
                if account_dict[your_account] < rounded_amount:
                    self.status_label.config(text="Nepietiekami līdzekļi (ieskaitot apaļošanu)", fg='red')
                    return
                    
                account_dict[your_account] -= rounded_amount
                add_transaction(your_account, -amount, f"Maksājums uz {other_account}: {description}")
                add_transaction(other_account, amount, f"Maksājums no {your_account}: {description}")
                
                savings_account = list(Krājkonts.keys())[0]  
                if savings_amount != 0:
                    Krājkonts[savings_account] += savings_amount
                    add_transaction(your_account, -savings_amount, f"Apaļošanas pārskaitijums")
                    add_transaction(savings_account, savings_amount, f"Apaļošana no {other_account}")
                
            else:
                if account_dict[your_account] < amount:
                    self.status_label.config(text="Nepietiekami līdzekļi", fg='red')
                    return
                    
                account_dict[your_account] -= amount
                add_transaction(your_account, -amount, f"Maksājums uz {other_account}: {description}")
                add_transaction(other_account, amount, f"Maksājums no {your_account}: {description}")
        else:
            amount = abs(amount)
            account_dict = Konts if your_account in Konts else Krājkonts
            account_dict[your_account] += amount
            add_transaction(your_account, amount, f"Ienākums no {other_account}: {description}")
            add_transaction(other_account, -amount, f"Maksājums uz {your_account}: {description}")
        
        self.amount_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.account_entry.delete(0, END)
        self.status_label.config(text="Transakcija pievienota veiksmīgi", fg='green')
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
    ("Pārskats", "overview.png", show_overview),
    ("Jauns darijums", "transfers.png", show_transfers),
]

for text, icon, command in nav_items:
    btn = Button(nav_bar, text=text, bg='#F8F8F8', bd=0, command=command)
    btn.pack(side=LEFT, expand=True, pady=10)

show_overview()

root.mainloop()
