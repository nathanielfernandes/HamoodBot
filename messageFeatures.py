import os 
import pathlib
import random
import ast

def profCheck(content):
    path = os.path.dirname(os.path.realpath(__file__))
    file = path + '/' + 'textFiles' + '/' + "profanity.txt"

    lst = []
    lst.append(content)

    words = [i for item in lst for i in item.split()]

    profanity_list = []
    profane = False

    badword = []
    
    badWords = open(file,"r",encoding='utf-8')
    badWords = badWords.readlines()

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
    path = os.path.dirname(os.path.realpath(__file__))
    file = path + '/' + 'textFiles' + '/' + "roasts.txt"

    roast_list = []
    roasts = open(file,"r",encoding='utf-8')
    roasts = roasts.readlines()

    for line in roasts:
        roast_list.append(line)
    roast = (random.choice(roast_list))
    return roast


#formatMsg
def remove(content, *useless: str):
    for char in useless:
        content = (str(content)).replace(char, '')
    return content

def convertList(_list, _split=False):
    string = ' '.join(_list)
    if _split:
        string = string.split(', ')
    return string


def convert_to_dict(file):
    with open(file,"r",encoding='utf-8') as f:
        info = f.read()
    dictionary = ast.literal_eval(info)
    return dictionary

