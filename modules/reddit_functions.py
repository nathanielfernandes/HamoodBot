import random
import praw
import os
import pathlib

try:
    CLIENTID = os.environ["CLIENTID"]
    CLIENTSECRET = os.environ["CLIENTSECRET"]
    USERAGENT = os.environ["USERAGENT"]
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    CLIENTID = os.environ.get("REDDITID")
    CLIENTSECRET = os.environ.get("REDDITSECRET")
    USERAGENT = os.environ.get("USERAGENT")

reddit = praw.Reddit(
    client_id=CLIENTID, client_secret=CLIENTSECRET, user_agent=USERAGENT
)

file = f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}/data/subreddits.txt"


def getSubReddit():
    sub_list = []
    subs = open(file, "r", encoding="utf-8")
    subs = subs.readlines()
    for line in subs:
        sub_list.append(line)

    redditSub = str(random.choice(sub_list))
    redditSub = redditSub.rstrip("\n")

    return redditSub


def findPost(sub):
    post_submissions = reddit.subreddit(sub).hot()
    post_to_pick = random.randint(1, 100)

    for i in range(0, post_to_pick):
        submission = next(x for x in post_submissions if not x.stickied)

    return submission

