import random
import praw
import formatMsg
import os
import pathlib

CLIENTID = os.environ['CLIENTID']
CLIENTSECRET = os.environ['CLIENTSECRET']
USERAGENT = os.environ['USERAGENT']

reddit = praw.Reddit(client_id=CLIENTID,
                     client_secret=CLIENTSECRET,
                     user_agent=USERAGENT)

path = os.path.dirname(os.path.realpath(__file__))
file = path + '/' + "subreddits.txt"

def getSubReddit():
    sub_list = []
    subs = open(file,"r",encoding='utf-8')
    subs = subs.readlines()
    for line in subs:
        sub_list.append(line)

    redditSub = str(random.choice(sub_list))
    redditSub = redditSub.rstrip("\n")

    return redditSub

def addSubReddit(sub):
    sub = formatMsg.remove(sub, '(', ')', "'", ",")

    sub_list = []
    sub = sub + "\n"
    subs = open(file,"r+",encoding='utf-8')
    sub_list = subs.readlines()
    sub_list = sub
    subs.writelines(sub_list)

    sub_list = sub_list.rstrip("\n")

    return sub_list

def findPost(sub):
    post_submissions = reddit.subreddit(sub).hot()
    post_to_pick = random.randint(1, 100)

    for i in range(0, post_to_pick):
        submission = next(x for x in post_submissions if not x.stickied)
        
    return submission

