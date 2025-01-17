from tkinter import *
import math

logs = Tk()
logs.title("Swedbank krājrīks")
logs.geometry("1000x600")

swedbank_interest = 2.5

def calculate():
    allocated = int(iemaksa_entry.get())
    procenta_summa = allocated * (swedbank_interest / 100)
    if procenta_summa % 1 >= 0.5:
        procenta_summa = math.ceil(procenta_summa)
    else:
        procenta_summa = math.floor(procenta_summa)
    
    procenta_summa_value.config(text=str(procenta_summa))


iemaksa_entry = Entry(logs, font=("Arial", 16))
iemaksa_entry.pack(pady=20)

iemaksas_label = Label(logs, text="Iemaksa", font=("Arial", 16))
iemaksas_label.pack(pady=20)

calculate_button = Button(logs, text="Aprēķināt", font=("Arial", 16), command=calculate)
calculate_button.pack(pady=20)

procenta_summa = Label(logs, text="Procenta summa", font=("Arial", 16))
procenta_summa.pack(pady=20)

procenta_summa_value = Label(logs, text="0", font=("Arial", 16))
procenta_summa_value.pack(pady=20)

logs.mainloop()