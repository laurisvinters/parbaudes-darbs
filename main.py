from tkinter import *
import math
logs = Tk()
logs.title("Swedbank")
logs.geometry("1000x600")

Konts =  {"Swedbank": 1000}
Krājkonts = {"Swedbank": 1000}

def transaction(konts):
    transaction = float(transaction_entry.get())
    print(f"transaction: {Konts[konts]}: {transaction} {konts}")
    if transaction < 0:
        decimal = transaction - math.floor(transaction)
        if decimal == 0:
            Konts[konts] += transaction
            transaction_value.config(text=f"{konts} " + str(Konts[konts]) + " €")
            
        else:
            Krājkonts[konts] += decimal
            Konts[konts] += (transaction - decimal)
            print(Krājkonts[konts])
            transaction_value.config(text=f"{konts} " + str(Konts[konts]) + " €")
            krājkonts_value.config(text=f"{konts} krājkonts: " + str(Krājkonts[konts]) + " €")
            
    
        
        print(Konts[konts])
        
    else:
        Konts[konts] += transaction
        transaction_value.config(text=f"{konts} " +str(Konts[konts]) + " €")

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

logs.mainloop()
