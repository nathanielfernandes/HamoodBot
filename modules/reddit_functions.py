import random
import praw
import os
import pathlib

try:
    CLIENTID = os.environ["CLIENTID"]
    CLIENTSECRET = os.environ["CLIENTSECRET"]
    USERAGENT = os.environ["USERAGENT"]
    do_cache = True
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    CLIENTID = os.environ.get("REDDITID")
    CLIENTSECRET = os.environ.get("REDDITSECRET")
    USERAGENT = os.environ.get("USERAGENT")

    do_cache = False

reddit = praw.Reddit(
    client_id=CLIENTID, client_secret=CLIENTSECRET, user_agent=USERAGENT
)

post_cache = {}


def cachePosts(sub):
    try:
        post_submissions = list(reddit.subreddit(sub).hot())
        post_submissions = [
            p.url
            for p in post_submissions
            if ".jpg" in p.url
            or ".jpeg" in p.url
            or ".png" in p.url
            or (
                ".gif" in p.url
                and "tenor" not in p.url
                and "giphy" not in p.url
                and "imgur" not in p.url
            )
        ]
    except Exception:
        post_submissions = []

    if len(post_submissions) < 1:
        post_cache[sub] = [[], 0]
    else:
        post_cache[sub] = [post_submissions, 0]

    return post_submissions


def findPost(sub):
    if sub in post_cache.keys():
        post_submissions, count = post_cache[sub]
        post_cache[sub][1] += 1
        if count >= 25:
            p = cachePosts(sub)
            print(f"{len(p)} r/{sub} posts recached")
    else:
        post_submissions = cachePosts(sub)
        print(f"{len(post_submissions)} r/{sub} posts cached")

    return random.choice(post_submissions) if post_submissions != [] else None
