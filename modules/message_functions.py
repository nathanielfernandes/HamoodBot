import os
import random
import ast

file = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/textFiles/profanity.txt"
badWords = [badword[:-1] for badword in open(file, "r", encoding="utf-8").readlines()]


def profCheck(content):
    badword = list(
        dict.fromkeys([bad for bad in badWords if bad in content and len(bad) > 4])
    )
    badword += list(
        dict.fromkeys(
            [bad for bad in badWords if bad in content.split() and len(bad) <= 4]
        )
    )
    profane = True if badword else False
    return profane, badword


def getRoast():
    file = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/textFiles/roasts.txt"

    roast_list = []
    roasts = open(file, "r", encoding="utf-8")
    roasts = roasts.readlines()

    for line in roasts:
        roast_list.append(line)
    roast = random.choice(roast_list)
    return roast


def convert_to_dict(file):
    with open(file, "r", encoding="utf-8") as f:
        info = f.read()
    dictionary = ast.literal_eval(info)
    return dictionary

