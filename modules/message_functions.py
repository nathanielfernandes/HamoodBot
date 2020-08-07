import os 
import random
import ast

file = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/textFiles/profanity.txt'
badWords = open(file,"r",encoding='utf-8')
badWords = badWords.readlines()

def profCheck(content):

    lst = []
    lst.append(content)

    words = [i for item in lst for i in item.split()]

    profanity_list = []
    profane = False

    badword = []

    for line in badWords:
        profanity_list.append(line)

    for w in words:

        for i in range(len(profanity_list)):
            profanity_list[i] = profanity_list[i].rstrip("\n")

            if (profanity_list[i] == w):
                profane = True
                badword.append(w)

    badword = list(dict.fromkeys(badword))
    return profane, badword


def getRoast():
    file = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/textFiles/roasts.txt'

    roast_list = []
    roasts = open(file,"r",encoding='utf-8')
    roasts = roasts.readlines()

    for line in roasts:
        roast_list.append(line)
    roast = (random.choice(roast_list))
    return roast


def convert_to_dict(file):
    with open(file,"r",encoding='utf-8') as f:
        info = f.read()
    dictionary = ast.literal_eval(info)
    return dictionary

