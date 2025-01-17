from datetime import date
from tkinter import *

logs = Tk()
logs.title("Swedbank krājrīks")
logs.geometry("1000x600")

swedbank_interest = 2.5
today = date.today()

def calculate():
    allocated = int(iemaksa_entry.get())
    print("Jums ir {} krājkontā, un ar swedbank interesi jūs pelnīsiet {} gadā.".format(allocated, allocated * (swedbank_interest / 100)))



iemaksa_entry = Entry(logs, font=("Arial", 16))
iemaksa_entry.pack(pady=20)

iemaksas_label = Label(logs, text="Iemaksa", font=("Arial", 16))
iemaksas_label.pack(pady=20)

calculate_button = Button(logs, text="Aprēķināt", font=("Arial", 16), command=calculate)
calculate_button.pack(pady=20)

logs.mainloop()