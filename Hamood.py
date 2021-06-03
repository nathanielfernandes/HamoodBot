# dependancies
import os, discord, datetime, requests, time
from discord.ext import commands, tasks
import dbl
import motor.motor_asyncio

from utils.mongo import *
from utils.market import Market
from utils.helpers import pretty_time_delta, quick_embed
from utils.http import HTTP
from utils.reddit import Reddit
from dotenv import load_dotenv

load_dotenv()


class Hamood:
    def __init__(self):
        self.tic = time.perf_counter()

        # Constants
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
        self.MONGO = motor.motor_asyncio.AsyncIOMotorClient(self.MONGOURI)
        self.BADWORDS = [
            badword.strip("\n")
            for badword in open(
                f"data/profanity.txt", "r", encoding="utf-8"
            ).readlines()
        ]
        self.RANDOMWORDS = requests.get(
            "https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json"
        ).json()
        # End

        intents = discord.Intents().default()
        intents.members = True

        self.bot = commands.Bot(
            command_prefix=self.get_prefix,
            case_insensitive=True,
            intents=intents,
            help_command=None,
            owner_ids={485138947115057162, 616148871499874310},
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=f"Lofi Beats",
            ),
        )
        self.bot.Hamood = self
        self.bot.on_message = self.on_message
        self.bot.on_ready = self.on_ready

        self.prefixes_list = {}
        self.find_prefix = lambda guild_id: self.prefixes_list.get(guild_id, ".")
        self.timeout_list = []
        self.filepath = (
            f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}"
        )

        self.pretty_time_delta = pretty_time_delta
        self.active_games = {}
        self.quick_embed = quick_embed

        self.market = Market(self.bot)
        self.ahttp = HTTP()

        print("-----------------------------")
        self.Prefixdb = Prefixes(self.MONGO)
        self.Leaderboards = Leaderboards(self.MONGO)
        self.Inventories = Inventories(self.MONGO)
        self.Currency = Currency(self.MONGO)
        self.Members = Members(self.MONGO)
        print(f"----------------------------- {time.perf_counter()-self.tic:0.2f}s")

        self.Reddit = Reddit(self.REDDITID, self.REDDITSECRET, self.USERAGENT)

        self.dblpy = dbl.DBLClient(
            self.bot,
            self.TOPGG,
            autopost=self.ISLIVE,
            webhook_path="/dblwebhook",
            webhook_auth=self.TOPGGAUTH,
            webhook_port=self.PORT,
        )

    def run(self):
        self.load_cogs()
        self.STARTUP = datetime.datetime.now()
        self.bot.run(self.TOKEN)

    def profCheck(self, content: str) -> bool:
        return any(
            (len(badword) > 4 and badword in content)
            or (len(badword) <= 4 and badword in content.split())
            for badword in self.BADWORDS
        )

    def load_cog(self, cog, scope):
        if cog.endswith(".py"):
            try:
                cog = f"cogs.{scope}.{cog.replace('.py', '')}"
                self.bot.load_extension(cog)
                print(f"{cog} Loaded")
            except Exception as e:
                print(f"{cog} cannot be loaded:")
                raise e

    def load_cogs(self):
        print("-----------------------------")
        for cog in os.listdir("./cogs/public"):
            self.load_cog(cog, "public")
        print(f"----------------------------- {time.perf_counter()-self.tic:0.2f}s")
        for cog in os.listdir("./cogs/private"):
            self.load_cog(cog, "private")
        print(f"----------------------------- {time.perf_counter()-self.tic:0.2f}s")

    async def get_prefix(self, bot, message):
        if message.guild.id not in self.prefixes_list:
            server = await self.Prefixdb.find_by_id(str(message.guild.id))
            if server is None:
                self.prefixes_list[message.guild.id] = "."
            else:
                self.prefixes_list[message.guild.id] = server["prefix"]
        return self.prefixes_list.get(message.guild.id, ".")

    async def on_ready(self):
        print("-----------------------------")
        print(f"Logged in as {self.bot.user}")
        print(f"----------------------------- {time.perf_counter()-self.tic:0.2f}s")

        try:
            await self.market.update_items.start()
        except RuntimeError:
            pass

    async def on_message(self, message):
        if message.author.bot and message.guild is not None:
            return

        p = self.find_prefix(message.guild.id)

        if message.content.strip() == f"<@!{self.bot.user.id}>":
            await message.channel.send(f"**The Server Prefix is `{p}`**")
        elif message.content.startswith(".help") and p != ".":
            await message.channel.send(f"Use `{p}help` instead!")

        await self.bot.process_commands(message)

