from tkinter import *
import math

logs = Tk()
logs.title("Swedbank")
logs.geometry("1000x600")

Konts =  {"Swedbank": 1000}
Krājkonts = {}
for account in Konts:
    Krājkonts[account + " krājkonts"] = 0

Transaction_history = []

def add_to_history(account, amount):
    transaction_record = {
        "account": account,
        "amount": amount,
    }
    Transaction_history.append(transaction_record)
    update_history_display()

def update_history_display():
    history_text.delete(1.0, END)
    for record in reversed(Transaction_history):
        amount_text = f"{record['amount']:+.2f} €"
        history_text.insert(END, f"{record['account']}: {amount_text}\n")

def transaction(konts):
    krājkonts = konts + " krājkonts"
    try:
        transaction = float(transaction_entry.get())

        if transaction < 0:
            decimal = round(abs(transaction - math.floor(transaction)), 2)

            if abs(transaction) > Konts[konts]:
                status_label.config(text="Transaction failed: Insufficient funds", fg="red")
                return

            if decimal == 0:
                Konts[konts] += transaction
                add_to_history(konts, transaction)
                transaction_value.config(text=f"{konts} {Konts[konts]} €")
                status_label.config(text="Transaction successful", fg="green")

            else:
                Krājkonts[krājkonts] = round(Krājkonts[krājkonts] + decimal, 2)
                Konts[konts] += (transaction - decimal)
                add_to_history(konts, transaction)
                add_to_history(konts, -decimal)
                add_to_history(krājkonts, decimal)
                transaction_value.config(text=f"{konts} {Konts[konts]} €")
                krājkonts_value.config(text=f"{krājkonts} : {Krājkonts[krājkonts]} €")
                status_label.config(text="Transaction successful", fg="green")

        else:
            Konts[konts] += transaction
            add_to_history(konts, transaction)
            transaction_value.config(text=f"{konts} {Konts[konts]} €")
            status_label.config(text="Transaction successful", fg="green")
            
        transaction_entry.delete(0, END)
    except ValueError:
        status_label.config(text="Invalid amount entered", fg="red")

def transfer():
    from_account = transfer_from_var.get()
    to_account = transfer_to_var.get()
    try:
        transfer_amount = float(transfer_entry.get())
        
        if transfer_amount < 0:
            status_label.config(text="Transfer failed: Amount must be positive", fg="red")
            return
        
        if from_account == to_account:
            status_label.config(text="Transfer failed: Cannot transfer to same account", fg="red")
            return
        
        if from_account in Konts:
            from_balance = Konts[from_account]
        elif from_account in Krājkonts:
            from_balance = Krājkonts[from_account]
        else:
            status_label.config(text="Transfer failed: Invalid source account", fg="red")
            return
        
        if to_account in Konts or to_account in Krājkonts:
            pass
        else:
            status_label.config(text="Transfer failed: Invalid destination account", fg="red")
            return
        
        if transfer_amount > from_balance:
            status_label.config(text="Transfer failed: Insufficient funds", fg="red")
            return
        
        if from_account in Konts:
            Konts[from_account] -= transfer_amount
        else:
            Krājkonts[from_account] -= transfer_amount
        
        if to_account in Konts:
            Konts[to_account] += transfer_amount
        else:
            Krājkonts[to_account] += transfer_amount
        
        add_to_history(from_account, -transfer_amount)
        add_to_history(to_account, transfer_amount)
        
        transaction_value.config(text=f"{from_account} {from_balance - transfer_amount} €")
        status_label.config(text=f"Transfer successful from {from_account} to {to_account}", fg="green")
        update_history_display()
    except ValueError:
        status_label.config(text="Transfer failed: Invalid amount", fg="red")

def update_transaction_mode(*args):
    current_mode = transaction_type.get()
    if current_mode == "Pārnest":
        transfer_from_label.pack(pady=5)
        transfer_from_dropdown.pack(pady=5)
        transfer_to_label.pack(pady=5)
        transfer_to_dropdown.pack(pady=5)
        transfer_entry.pack(pady=10)
        transaction_button.pack(pady=10)
        
        transaction_from_label.pack_forget()
        transaction_from_dropdown.pack_forget()
        transaction_entry.pack_forget()
    else: 
        transfer_from_label.pack_forget()
        transfer_from_dropdown.pack_forget()
        transfer_to_label.pack_forget()
        transfer_to_dropdown.pack_forget()
        transfer_entry.pack_forget()
        
        transaction_from_label.pack(pady=5)
        transaction_from_dropdown.pack(pady=5)
        transaction_entry.pack(pady=10)
        transaction_button.pack(pady=10)

main_frame = Frame(logs)
main_frame.pack(fill="both", expand=True)

left_frame = Frame(main_frame)
left_frame.pack(side="left", fill="both", expand=True)
right_frame = Frame(main_frame)
right_frame.pack(side="right", fill="both", expand=True)


transaction_type = StringVar(logs)
transaction_type.set("Transakcija")
transaction_type_menu = OptionMenu(left_frame, transaction_type, "Pārnest", "Transakcija", command=update_transaction_mode)
transaction_type_menu.pack(pady=5)

transfer_from_label = Label(left_frame, text="No: ", font=("Arial", 12))
transfer_from_label.pack_forget()
transfer_from_var = StringVar(logs)
transfer_from_dropdown = OptionMenu(left_frame, transfer_from_var, *list(Konts.keys()))
transfer_from_dropdown.pack_forget()

transfer_to_label = Label(left_frame, text="Uz: ", font=("Arial", 12))
transfer_to_label.pack_forget()
transfer_to_var = StringVar(logs)
transfer_to_dropdown = OptionMenu(left_frame, transfer_to_var, *list(Konts.keys()), *list(Krājkonts.keys()))
transfer_to_dropdown.pack_forget()

transaction_from_label = Label(left_frame, text="No konta: ", font=("Arial", 12))
transaction_from_label.pack(pady=5)
transaction_from = StringVar(logs)
transaction_from_dropdown = OptionMenu(left_frame, transaction_from, *list(Konts.keys()))
transaction_from_dropdown.pack(pady=5)

transaction_entry = Entry(left_frame, font=("Arial", 16))
transaction_entry.pack(pady=10)

transfer_entry = Entry(left_frame, font=("Arial", 16))
transfer_entry.pack_forget()

transaction_button = Button(left_frame, text="Jauns darijums", font=("Arial", 16), command=lambda: transfer() if transaction_type.get() == "Pārnest" else transaction(transaction_from.get()))
transaction_button.pack(pady=10)

transaction_value = Label(right_frame, text="0 €", font=("Arial", 16))
transaction_value.pack(pady=10)

krājkonts_value = Label(right_frame, text="0 €", font=("Arial", 16))
krājkonts_value.pack(pady=10)

status_label = Label(left_frame, text="", font=("Arial", 12))
status_label.pack(pady=10)

history_frame = Frame(right_frame)
history_frame.pack(fill="both", expand=True, pady=10)

history_label = Label(history_frame, text="Transaction History", font=("Arial", 14, "bold"))
history_label.pack()

history_text = Text(history_frame, font=("Arial", 12), height=10, width=40)
history_text.pack(pady=10)

logs.mainloop()
