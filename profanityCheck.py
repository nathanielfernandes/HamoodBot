import os 
import pathlib
import formatMsg

path = os.path.dirname(os.path.realpath(__file__))
file = path + '/' + "profanity.txt"

def profCheck(content):

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


def profAdd(content):
    content = formatMsg.remove(content, '(', ')', "'", ",")

    profanity_list = []
    content = content + "\n"
    badWords = open(file,"r+",encoding='utf-8')
    profanity_list = badWords.readlines()
    profanity_list = content
    badWords.writelines(profanity_list)

    profanity_list = profanity_list.rstrip("\n")

    return profanity_list

