from matplotlib import pyplot as plt
import tkinter as tk
import random

d20 = list(range(1, 21))

class env():
    volcano = 0

class meta():
    eruption_day = []
    day = 0
    roll = -1

    rainbow = ["red", "orange", "yellow", "green", "blue", "purple"]

def volcanoErupts(display_stats=False):
    meta.day = meta.day + 1
    feedback = ""
    roll = random.choice(d20)
    meta.roll = roll
    
    if roll == 1:
        env.volcano = 100
    elif 20 > roll > 1:
        env.volcano = env.volcano + (20 - roll)
    elif roll == 20:
        env.volcano = env.volcano / 2

    if display_stats == True:
        print("Day: ", meta.day)
        print("Roll: ", meta.roll)
        print("Score: ", env.volcano)

    if env.volcano >= 100:
        feedback = "Eruption!"
        env.volcano = 0
        meta.eruption_day.append(meta.day)
        meta.day = 0
    elif 80 < env.volcano < 100:
        feedback = "Black smoke pours from the top of the volcano"
    elif env.volcano <= 80:
        feedback = "Nothing happens"

    return feedback

##call volcanoErupts for 500 days, record day of each eruption
##at each eruption day is set back to zero

def thousandDays():
    plt.clf()
    
    meta.eruption_day = []

    for n in range(0,1000):
        volcanoErupts()

    plt.hist(meta.eruption_day, 20, color=random.choice(meta.rainbow))
    plt.show()

    meta.day = 0
    env.volcano = 0

    return meta.eruption_day

######

def volcanoEruptsButton():
    print(volcanoErupts(display_stats=True))
    print("")
    

root = tk.Tk()

day = tk.Button(
   root, 
   text = "Next Day", 
   command = volcanoEruptsButton)
day.grid(row=1, column=1)

sim = tk.Button(
    root,
    text = "Graph",
    command = thousandDays)
sim.grid(row=1, column=2)

root.mainloop()
