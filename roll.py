import random as random

def roll(d=20):
    print(random.choice(list(range(1,d+1))))

for n in range(0,100):
    d = int(input("Roll a d: "))
    roll(d)

