from tkinter import *
import math

logs = Tk()
logs.title("Swedbank krājrīka kaukulātors")
logs.geometry("1000x600")

swedbank_interest = 2.5

def calculate():
    vienreizējā_iemaksa = int(iemaksa_entry.get())
    ikmenesa_iemaksa = int(ikmenesa_iemaksa_entry.get())
    
    ikmenesa_iemaksa_value.config(text=str(ikmenesa_iemaksa * 12 + vienreizējā_iemaksa))
    
    procenta_summa = vienreizējā_iemaksa * (swedbank_interest / 100)

    monthly_sum = 0
    for month in range(11, -1, -1):
        monthly_interest = ikmenesa_iemaksa * (swedbank_interest / 100) * ((month + 1) / 12)
        monthly_sum += monthly_interest
    
    procenta_summa += monthly_sum
    
    procenta_summa = round(procenta_summa, 2)
    procenta_summa = math.ceil(procenta_summa) if procenta_summa % 1 >= 0.5 else math.floor(procenta_summa)
    
    procenta_summa_value.config(text=str(procenta_summa))

main_frame = Frame(logs)
main_frame.pack(fill="both", expand=True)

left_frame = Frame(main_frame)
left_frame.pack(side="left", fill="both", expand=True)
right_frame = Frame(main_frame)
right_frame.pack(side="right", fill="both", expand=True)

iemaksa_entry = Entry(left_frame, font=("Arial", 16))
iemaksa_entry.pack(pady=20)

iemaksas_label = Label(left_frame, text="Iemaksa", font=("Arial", 16))
iemaksas_label.pack(pady=20)

ikmenesa_iemaksa_entry = Entry(left_frame, font=("Arial", 16))
ikmenesa_iemaksa_entry.pack(pady=20)

ikmenesas_label = Label(left_frame, text="Ikmenesā iemaksa", font=("Arial", 16))
ikmenesas_label.pack(pady=20)

calculate_button = Button(right_frame, text="Aprēķināt", font=("Arial", 16), command=calculate)
calculate_button.pack(pady=20)

procenta_summa = Label(right_frame, text="Procenta summa", font=("Arial", 16))
procenta_summa.pack(pady=20)

procenta_summa_value = Label(right_frame, text="0", font=("Arial", 16))
procenta_summa_value.pack(pady=20)

ikmenesa_iemaksa = Label(right_frame, text="Manas Iemaksas", font=("Arial", 16))
ikmenesa_iemaksa.pack(pady=20)

ikmenesa_iemaksa_value = Label(right_frame, text="0", font=("Arial", 16))
ikmenesa_iemaksa_value.pack(pady=20)

logs.mainloop()