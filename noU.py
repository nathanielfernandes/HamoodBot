import os
import pathlib
import random 

def unoCard():
    path = os.path.dirname(os.path.realpath(__file__))
    folder = path + '/' + "unoCards"
    
    mix = random.randint(0,3)
    card = os.listdir(folder)
    card = folder + '/' + card[mix]

    return card