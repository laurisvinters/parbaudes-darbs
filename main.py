from tkinter import *
import math

logs = Tk()
logs.title("Swedbank")
logs.geometry("1000x600")

Konts =  {"Swedbank": 1000}
Krājkonts = {"Swedbank": 0}
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
    krājkonts = konts+ " krājkonts"
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
                Krājkonts[konts] = round(Krājkonts[konts] + decimal, 2)
                Konts[konts] += (transaction - decimal)
                add_to_history(konts, transaction)
                add_to_history(konts, -decimal)
                add_to_history(krājkonts, decimal)
                transaction_value.config(text=f"{konts} {Konts[konts]} €")
                krājkonts_value.config(text=f"{konts} krājkonts: {Krājkonts[konts]} €")
                status_label.config(text="Transaction successful", fg="green")
                
        else:
            Konts[konts] += transaction
            add_to_history(konts, transaction)
            transaction_value.config(text=f"{konts} {Konts[konts]} €")
            status_label.config(text="Transaction successful", fg="green")
            
        transaction_entry.delete(0, END)
    except ValueError:
        status_label.config(text="Invalid amount entered", fg="red")

main_frame = Frame(logs)
main_frame.pack(fill="both", expand=True)

left_frame = Frame(main_frame)
left_frame.pack(side="left", fill="both", expand=True)
right_frame = Frame(main_frame)
right_frame.pack(side="right", fill="both", expand=True)

transaction_entry = Entry(left_frame, font=("Arial", 16))
transaction_entry.pack(pady=20)

transaction_button = Button(left_frame, text="Jauns darijums", font=("Arial", 16), command=lambda: transaction("Swedbank"))
transaction_button.pack(pady=20)

transaction_value = Label(right_frame, text="0 €", font=("Arial", 16))
transaction_value.pack(pady=20)

krājkonts_value = Label(right_frame, text="0 €", font=("Arial", 16))
krājkonts_value.pack(pady=20)

status_label = Label(left_frame, text="", font=("Arial", 12))
status_label.pack(pady=10)

history_frame = Frame(right_frame)
history_frame.pack(fill="both", expand=True, pady=20)

history_label = Label(history_frame, text="Transaction History", font=("Arial", 14, "bold"))
history_label.pack()

history_text = Text(history_frame, font=("Arial", 12), height=10, width=40)
history_text.pack(pady=10)

logs.mainloop()
