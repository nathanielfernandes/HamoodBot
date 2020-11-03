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

post_cache = {}


def getSubReddit():
    sub_list = []
    subs = open(file, "r", encoding="utf-8")
    subs = subs.readlines()
    for line in subs:
        sub_list.append(line)

    redditSub = str(random.choice(sub_list))
    redditSub = redditSub.rstrip("\n")

    return redditSub


def fillCache(sub):
    try:
        post_submissions = list(reddit.subreddit(sub).hot())
    except Exception:
        post_submissions = False

    post_cache[sub] = [post_submissions, 0]
    return post_submissions


def findPost(sub):
    if sub in post_cache.keys():
        post_submissions, count = post_cache[sub]
        post_cache[sub][1] += 1
        if count >= 30:
            fillCache(sub)
            print(f"r/{sub} cache has been refilled")
    else:
        post_submissions = fillCache(sub)
        print(f"r/{sub} cache has been filled")

    sample = random.sample(range(100), 100)
    for i in sample:
        if (
            (".jpg" in post_submissions[i].url)
            or (".jpeg" in post_submissions[i].url)
            or (".png" in post_submissions[i].url)
        ):
            return post_submissions[i].url

    return

