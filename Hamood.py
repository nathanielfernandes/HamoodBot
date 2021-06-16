# dependancies
import os, discord, datetime, time, re, asyncio
from discord.ext import commands, tasks
import dbl
from random import randint
import motor.motor_asyncio
from functools import partial

from utils.mongo import *
from utils.market import Market
from utils.helpers import *
from utils.ahttp import HTTP
from utils.reddit import Reddit
from utils.CONSTANTS import load_constants, add_regexes, add_helpers, ANSI, HAMOOD


class Hamood:
    def __init__(self):
        self.tic = time.perf_counter()

        load_constants(self)
        add_regexes(self)
        add_helpers(self)

        intents = discord.Intents().default()
        intents.members = True

        self.bot = commands.Bot(
            command_prefix=self.get_prefix,
            case_insensitive=True,
            intents=intents,
            help_command=None,
            owner_ids={485138947115057162, 616148871499874310},
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=f"Lofi Beats"
            ),
        )
        self.bot.Hamood = self
        self.bot.on_message = self.on_message
        self.bot.on_ready = self.on_ready
        self.bot.add_check(self.spam_prev, call_once=True)

        self.prefixes_list = {}
        self.find_prefix = lambda guild_id: self.prefixes_list.get(guild_id, ".")
        self.timeout_list = []
        self.filepath = (
            f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}"
        )
        self.active_games = {}
        self.active_feeds = {}
        self.command_invocations = 0

        self.market = Market(self.bot)
        self.ahttp = HTTP()

        self.cstr = lambda string, c: f"{c}{string}{ANSI.ENDC}"
        self.cprint = lambda string, c: print(self.cstr(string, c))

        self.cprint("-----------------------------", ANSI.OKGREEN)
        print(ANSI.OKBLUE, end="")
        self.MONGO = motor.motor_asyncio.AsyncIOMotorClient(self.MONGOURI)
        self.Prefixdb = Prefixes(self.MONGO)
        self.Leaderboards = Leaderboards(self.MONGO)
        self.Inventories = Inventories(self.MONGO)
        self.Currency = Currency(self.MONGO)
        self.Members = Members(self.MONGO)
        self.PremiumUsers = []
        self.PremiumGuilds = []
        print(ANSI.ENDC, end="")
        self.cprint(
            f"----------------------------- {time.perf_counter()-self.tic:0.2f}s",
            ANSI.OKGREEN,
        )

        self.Reddit = Reddit(self.REDDITID, self.REDDITSECRET, self.USERAGENT)

        self.dblpy = dbl.DBLClient(
            self.bot,
            self.TOPGG,
            autopost=self.ISLIVE,
            # webhook_path="/dblwebhook",
            # webhook_auth=self.TOPGGAUTH,
            # webhook_port=self.PORT,
        )

        self._cd = commands.CooldownMapping.from_cooldown(
            3, 5, commands.BucketType.user
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
                name = cog.replace(".py", "")
                cog = f"cogs.{scope}.{name}"
                self.bot.load_extension(cog)
                loaded = self.bot.get_cog(name)
                loaded.public = scope == "public"
                self.cprint(f"{cog} Loaded", ANSI.OKCYAN)
            except Exception as e:
                self.cprint(f"{cog} cannot be loaded:", ANSI.FAIL)
                raise e

    def load_cogs(self):
        self.cprint("-----------------------------", ANSI.OKGREEN)
        for cog in os.listdir("./cogs/public"):
            self.load_cog(cog, "public")
        self.cprint(
            f"----------------------------- {time.perf_counter()-self.tic:0.2f}s",
            ANSI.OKGREEN,
        )
        for cog in os.listdir("./cogs/private"):
            self.load_cog(cog, "private")
        self.cprint(
            f"----------------------------- {time.perf_counter()-self.tic:0.2f}s",
            ANSI.OKGREEN,
        )

    async def get_prefix(self, bot, message):
        if message.guild.id not in self.prefixes_list:
            server = await self.Prefixdb.find_by_id(str(message.guild.id))
            if server is None:
                self.prefixes_list[message.guild.id] = "."
            else:
                self.prefixes_list[message.guild.id] = server["prefix"]
        return self.prefixes_list.get(message.guild.id, ".")

    async def on_ready(self):
        self.cprint("-----------------------------", ANSI.OKGREEN)
        self.cprint(HAMOOD, ANSI.OKBLUE)
        self.cprint(f"Logged in as {self.bot.user}", ANSI.BLUE)
        self.cprint(
            f"----------------------------- {time.perf_counter()-self.tic:0.2f}s",
            ANSI.OKGREEN,
        )

        try:
            await self.market.update_items.start()
        except RuntimeError:
            pass

    def ignore_check(self, message):
        return (
            message.author.bot
            or message.guild is None
            or message.author.id in self.timeout_list
        )

    async def on_message(self, message):
        if self.ignore_check(message):
            return

        p = self.find_prefix(message.guild.id)
        if message.content.strip() == f"<@!{self.bot.user.id}>":
            await message.channel.send(f"**The Server Prefix is `{p}`**")
        elif message.content.startswith(".help") and p != ".":
            await message.channel.send(f"Use `{p}help` instead!")

        await self.bot.process_commands(message)

    async def run_async(self, blocking_func, *args, **kwargs):
        func = partial(blocking_func, *args, **kwargs)
        return await self.bot.loop.run_in_executor(None, func)

    def save_name(self, ext: str = "png") -> str:
        return f'{"".join([str(randint(0, 9)) for _ in range(18)])}.{ext}'

    async def spam_prev(self, ctx):
        self.command_invocations += 1
        return await self.spam_check(ctx.message)

    async def spam_check(self, message, alert=True):
        if message.author.id not in self.timeout_list:
            bucket = self._cd.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                if alert:
                    embed = discord.Embed(
                        title=f"Spam Detected! | {message.author}",
                    )
                    embed.set_footer(
                        text="I'm gonna ignore you for the next 15 seconds",
                    )
                    await message.channel.send(embed=embed)
                self.timeout_list.append(message.author.id)
                await asyncio.sleep(15)
                self.timeout_list.remove(message.author.id)
            else:
                return True
        else:
            return False

    async def user_is_premium(self, user_id: int):
        return user_id in self.PremiumUsers
