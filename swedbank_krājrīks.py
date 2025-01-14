from datetime import date
from tkinter import *

allocated = 0
today = date.today()
swedbank_interest = 2.5

def accured_interest():
    return allocated * (swedbank_interest / 100)

allocated = int(input("Ievadi cik krājkontā jums ir naudas: "))

print("Jums ir {} krājkontā, un ar swedbank interesi jūs pelnīsiet {} gadā.".format(allocated, accured_interest()))


