import requests, os, re
from dotenv import load_dotenv

from utils.helpers import *

load_dotenv()


def load_constants(self):
    self.TOKEN = os.environ.get("TOKEN")
    self.REDDITID = os.environ.get("REDDITID")
    self.REDDITSECRET = os.environ.get("REDDITSECRET")
    self.USERAGENT = os.environ.get("USERAGENT")
    self.MONGOURI = os.environ.get("MONGOURI")
    self.TOPGG = os.environ.get("TOPGG")
    self.TOPGGAUTH = os.environ.get("TOPGGAUTH")
    self.ISLIVE = os.environ.get("ISLIVE") == "True"
    self.PORT = os.environ.get("PORT", 5000)
    self.URBANDICTKEY = os.environ.get("URBANDICTKEY")
    self.URBANDICTHOST = os.environ.get("URBANDICTHOST")
    self.DISCORDSUBHUB = os.environ.get("DISCORDSUBHUB")
    self.GOOGLE_SEARCH_LINK = os.environ.get("GOOGLE_SEARCH")

    self.BADWORDS = [
        badword.strip("\n")
        for badword in open(f"data/profanity.txt", "r", encoding="utf-8").readlines()
    ]
    self.RANDOMWORDS = requests.get(
        "https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json"
    ).json()
    self.RANDOMEMOJIS = [
        "😳",
        "😭",
        "🤗",
        "😴",
        "😪",
        "🤡",
        "💩",
        "👽",
        "😋",
        "👍",
        "👎",
        "👏",
        "👑",
        "🦋",
        "🐸",
        "🐝",
        "🐍",
        "🐄",
        "🦧",
        "🐄",
        "🐈",
        "🍄",
        "💐",
        "🌈",
        "✨",
        "❄️",
        "🍆",
        "🍑",
        "🍒",
        "🥑",
        "🌽",
        "🥐",
        "🧀",
        "🥞",
        "🌭",
        "🍭",
        "🍰",
        "🍺",
        "🧂",
        "⚽",
        "🚀",
        "✈️",
        "🗿",
        "🌋",
        "☎️",
        "💎",
        "🔪",
        "🦠",
        "💉",
        "🛀",
        "🎁",
        "🎈",
        "🧮",
        "📝",
        "❤️",
        "🆘",
        "❌",
        "💯",
        "🔞",
        "🆒",
        "🎶",
    ]
    self.CDN_URL = "https://cdn.hamood.app"
    self.URL = "https://hamood.app"


def add_regexes(self):
    self.re_validChannel = re.compile(
        r"^(?:https?:)?\/\/?(?:www|m)\.?(?:youtube\.com|youtu.be)\/(?:[\w\-]+\?v=|embed\/|v\/)?([\w\-]+)/(\S+)?$"
    )

    self.re_getID_backup = re.compile(
        r"<link rel=\"alternate\" type=\"application/rss\+xml\" title=\"RSS\" href=\"https://www\.youtube\.com/feeds/videos\.xml\?channel_id=(\S+)?\">"
    )
    self.re_YoutubeID = re.compile(
        r"<meta property=\"og:url\" content=\"https://www\.youtube\.com/channel/(\S+)?\">"
    )
    self.re_YoutubeImage = re.compile(
        r"<meta property=\"og:image\" content=\"(\S+)?\">"
    )
    self.re_YoutubeName = re.compile(r"<meta property=\"og:title\" content=\"(\S+)?\">")

    self.re_RedditUrl = re.compile(
        r"reddit\.com\/(?:r|u|user)\/\S{2,}\/comments\/([0-9a-z]+)"
    )
    self.re_ValidImageUrl = re.compile(
        r"(https?:(?:(?!tenor|giphy|imgur)[/|.|\w|\s|-])*\.(?:jpg|gif|png))"
    )

    self.re_member = re.compile(r"(<@!?\d+>)")
    self.re_emoji = re.compile(r"(<a?:\w+:?\d+>)")
    self.re_role = re.compile(r"(<@&\d+>)")
    self.re_channel = re.compile(r"(<#\d+>)")


def add_helpers(self):
    self.pretty_dt = pretty_dt
    self.quick_embed = quick_embed
    self.pastel_color = pastel_color
    self.flatten = flatten
    self.named_flatten = named_flatten


class ANSI:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    BLUE = "\u001b[34m"
    ORANGE = "\033[48:5:208:0m%s\033[m"
    DORANGE = "\033[48:5:166:0m%s\033[m\n"


HAMOOD = """
██╗  ██╗ █████╗ ███╗   ███╗ ██████╗  ██████╗ ██████╗ 
██║  ██║██╔══██╗████╗ ████║██╔═══██╗██╔═══██╗██╔══██╗
███████║███████║██╔████╔██║██║   ██║██║   ██║██║  ██║
██╔══██║██╔══██║██║╚██╔╝██║██║   ██║██║   ██║██║  ██║
██║  ██║██║  ██║██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝"""
