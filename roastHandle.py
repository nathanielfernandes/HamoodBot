import random
import formatMsg
import os
import pathlib

path = os.path.dirname(os.path.realpath(__file__))
file = path + '/' + "roasts.txt"

def getRoast():
    roast_list = []
    roasts = open(file,"r",encoding='utf-8')
    roasts = roasts.readlines()

    for line in roasts:
        roast_list.append(line)
    roast = (random.choice(roast_list))

    return roast


def addRoast(roast):
    roast = formatMsg.remove(roast, '(', ')', "'", ",")

    roast_list = []
    roast = roast + "\n"
    roasts = open(file,"r+",encoding='utf-8')
    roast_list = roasts.readlines()
    roast_list = roast
    roasts.writelines(roast_list)

    roast_list = roast_list.rstrip("\n")

    return roast_list
