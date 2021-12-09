import random, re
import asyncpraw

from utils.StackTypes import DictStack
from utils.CONSTANTS import ANSI

VALIDURL = re.compile(
    r"https?:(?:(?!tenor|giphy|imgur)[/|.|\w|\s|-])*\.(?:jpg|gif|png|jpeg|PNG|JPG|GIF|JPEG)"
)


class CleanPost:
    __slots__ = (
        "subreddit",
        "_id",
        "title",
        "description",
        "image_url",
        "hasimage",
        "upvotes",
        "is_nsfw",
        "permalink",
        "thumbnail",
    )

    def __init__(self, post, fetched=False):
        self.subreddit = post.subreddit.display_name
        self._id = post.id
        self.title = post.title[:256]
        self.description = (
            f"{post.selftext[:1900]}{'...' if len(post.selftext) >= 1980 else ''}"
            + (
                "\n[**video link**]"
                + f"(https://www.rvdl.com{post.permalink}) from rvdl"
                if any(
                    ext in post.url for ext in ("tenor", "giphy", "imgur", "v.redd.it")
                )
                else ""
            )
        )
        self.image_url = post.url
        self.hasimage = VALIDURL.search(post.url) is not None
        self.upvotes = post.score
        self.is_nsfw = post.over_18
        self.permalink = f"https://www.reddit.com{post.permalink}"
        self.thumbnail = None
        if fetched:
            try:
                self.thumbnail = post.preview["images"][0]["source"]["url"]
            except:
                pass

    def __repr__(self):
        return self._id


class Reddit:
    def __init__(self, CLIENTID, CLIENTSECRET, USERAGENT):
        self.red = asyncpraw.Reddit(
            client_id=CLIENTID, client_secret=CLIENTSECRET, user_agent=USERAGENT
        )
        self.SubredditCache = DictStack(data={}, stack_size=100)
        self.TempPostCache = DictStack(data={}, stack_size=20)

    async def fetch_feed(self, subreddit: str):
        try:
            submissions = await self.red.subreddit(subreddit, fetch=True)
        except Exception:
            return {}
        else:
            feed = {}
            async for post in submissions.hot():
                feed[post.id] = CleanPost(post)  # self.to_dict(post)
            print(f"Fetched feed from {ANSI.WARNING}r/{subreddit}{ANSI.ENDC}")
            return feed

    async def cache_posts(self, subreddit: str):
        try:
            submissions = await self.red.subreddit(subreddit, fetch=True)
        except:
            return False
        else:
            self.SubredditCache[subreddit] = {}
            async for post in submissions.hot():
                self.SubredditCache[subreddit][post.id] = CleanPost(
                    post
                )  # self.to_dict(post)
            print(
                f"Cached {ANSI.OKGREEN}{len(self.SubredditCache[subreddit])}{ANSI.ENDC} posts from {ANSI.WARNING}r/{subreddit}{ANSI.ENDC}"
            )
            return True

    async def get_random_post(self, subreddit, image_only=False, stop=False):
        if subreddit in self.SubredditCache:
            _ids = [
                post_id
                for post_id in self.SubredditCache[subreddit].keys()
                if (
                    self.SubredditCache[subreddit][post_id].hasimage
                    if image_only
                    else True
                )
            ]

            if len(_ids) >= 3:
                post_id = random.choice(_ids)
                return self.SubredditCache[subreddit].pop(post_id)
        if not stop:
            cached = await self.cache_posts(subreddit)
            return (
                await self.get_random_post(subreddit, image_only, True)
                if cached
                else None
            )

    async def fetch_post(self, post_id: str):
        if post_id in self.TempPostCache:
            return self.TempPostCache[post_id]
        else:
            try:
                post = await self.red.submission(id=post_id)
            except:
                return
            else:
                print(
                    f"{ANSI.OKGREEN}Fetched Post:{ANSI.ENDC} {ANSI.WARNING}{post_id}{ANSI.ENDC}"
                )
                post = CleanPost(post, True)  # self.to_dict(post, loaded=True)
                self.TempPostCache[post_id] = post

                return post

    # def to_dict(self, post, loaded=False):
    #     thumb = None
    #     if loaded:
    #         try:
    #             thumb = post.preview["images"][0]["source"]["url"]
    #         except:
    #             pass
    #     return {c
    #         "title": post.title,
    #         "text": f"{post.selftext}"
    #         + (
    #             "\n[**video link**]"
    #             + f"(https://www.rvdl.com{post.permalink}) from rvdl"
    #             if any(
    #                 ext in post.url for ext in ("tenor", "giphy", "imgur", "v.redd.it")
    #             )
    #             else ""
    #         ),
    #         "url": post.url,
    #         "upvotes": post.score,
    #         # "ratio": post.upvote_ratio,
    #         "nsfw": post.over_18,
    #         "permalink": f"https://www.reddit.com{post.permalink}",
    #         "subreddit": post.subreddit.display_name,
    #         "hasimage": self.hasimage(post.url),
    #         "thumbnail": thumb,
    #     }
