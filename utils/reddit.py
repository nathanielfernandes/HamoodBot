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


class Redditing:
    def __init__(self):
        self.red = praw.Reddit(
            client_id=CLIENTID, client_secret=CLIENTSECRET, user_agent=USERAGENT
        )
        self.all_posts_cache = {}
        self.image_posts_cache = {}

    def to_dict(self, post):
        return {
            "title": post.title,
            "text": post.selftext,
            "url": post.url,
            "upvotes": post.score,
            "ratio": post.upvote_ratio,
        }

    def url_contains_image(self, url):
        for i in [".jpg", ".jpeg", ".png", ".webp" ".JPG", ".JPEG", ".PNG", ".WEBP"]:
            if i in url:
                return True
        if (
            (".gif" in url)
            and ("tenor" not in url)
            and ("giphy" not in url)
            and ("imgur" not in url)
        ):
            return True
        return False

    def cache_posts(self, sub, image_only=False):
        try:
            post_submissions = list(self.red.subreddit(sub).hot())
            if image_only:
                temp_image_posts = {
                    post.id: self.to_dict(post)
                    for post in post_submissions
                    if self.url_contains_image(post.url)
                }

                if len(temp_image_posts) >= 1:
                    self.image_posts_cache[sub] = temp_image_posts
                    return True

            else:
                temp_all_posts = {
                    post.id: self.to_dict(post)
                    for post in post_submissions
                    if self.url_contains_image(post.url) or post.selftext != ""
                }

                if len(temp_all_posts) >= 1:
                    self.all_posts_cache[sub] = temp_all_posts
                    return True

            return False

        except Exception:
            return False

    def get_post(self, sub, image_only=False):
        if image_only:
            posts = self.image_posts_cache
        else:
            posts = self.all_posts_cache

        if sub in posts:
            post_id = random.choice(list(posts[sub].keys()))
            post = posts[sub].get(post_id)
            posts[sub].pop(post_id)
            if len(posts[sub]) <= 0:
                posts.pop(sub)
        else:
            cached = self.cache_posts(sub, image_only)
            if cached:
                print(f"Cached {len(posts[sub])} posts from r/{sub}")
                post_id = random.choice(list(posts[sub].keys()))
                post = posts[sub].get(post_id)
                posts[sub].pop(post_id)
                if len(posts[sub]) <= 0:
                    posts.pop(sub)
            else:
                post = None

        return post

