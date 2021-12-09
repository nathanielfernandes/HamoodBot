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
        self.bot.add_check(self.allowed_check, call_once=True)

        self.prefixes_list = {}
        self.find_prefix = lambda guild_id: self.prefixes_list.get(guild_id, ".")
        self.timeout_list = []
        self.filepath = (
            f"{os.path.split(os.getcwd())[0]}/{os.path.split(os.getcwd())[1]}"
        )
        self.active_games = {}
        self.active_feeds = {}
        self.command_invocations = 0
        self.cog_invokes = {}
        self.total_gens = 0
        self.total_gen_bytes = 0

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
        self.PremiumUsers = [
            485138947115057162,
            248909528387551233,
            222865938771345408,
            555085307431747584,
            680164554952671234,
            616148871499874310,
            616148871499874310,
        ]
        print(ANSI.ENDC, end="")
        self.cprint(
            f"----------------------------- {self.deltaT():0.2f}s",
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
            3, 3, commands.BucketType.user
        )

        self.start_tstamp = self.tstamp()

        # debug
        # self.bot.load_extension("jishaku")

    def run(self):
        self.load_cogs()
        self.STARTUP = datetime.datetime.now()
        self.market.update_items.start()
        self.update_premiums.start()
        self.bot.run(self.TOKEN)

    def deltaT(self):
        return time.perf_counter() - self.tic

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
                if scope == "public":
                    self.cog_invokes[name] = 0
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
            f"----------------------------- {self.deltaT():0.2f}s",
            ANSI.OKGREEN,
        )
        for cog in os.listdir("./cogs/private"):
            self.load_cog(cog, "private")
        self.cprint(
            f"----------------------------- {self.deltaT():0.2f}s",
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
            f"----------------------------- {self.deltaT():0.2f}s",
            ANSI.OKGREEN,
        )

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

    async def run_async_t(self, blocking_func, *args, **kwargs):
        tic = time.perf_counter()
        out = await self.run_async(blocking_func, *args, **kwargs)
        toc = time.perf_counter()
        return out, f"took {toc-tic:0.2f}s"

    def save_name(self, ext: str = "png") -> str:
        return f"{self.tstamp()}.{ext}"

    def tstamp(self) -> str:
        return f"{datetime.datetime.now().timestamp():0.3f}".replace(".", "")

    def cdnsave(self, ext: str = "png") -> tuple[str, str]:
        name = self.save_name(ext)
        return f"{self.filepath}/temp/{name}", f"{self.CDN_URL}/{name}"

    async def allowed_check(self, ctx):
        self.command_invocations += 1
        if ctx.cog.public:
            self.cog_invokes[ctx.cog.qualified_name] += 1
        return True

    async def spam_prev(self, ctx):
        self.command_invocations += 1
        if ctx.cog.public:
            self.cog_invokes[ctx.cog.qualified_name] += 1
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

    async def user_is_premium(self, user_id):
        return user_id in self.PremiumUsers

    # @tasks.loop(minutes=30, reconnect=True)
    # async def update_premiums(self):
    #     await self.bot.wait_until_ready()
    #     try:
    #         supporter = self.bot.get_guild(854249588341080104)
    #         self.PremiumUsers = []
    #         for m in supporter.members:
    #             if any(r.name == "supporter" for r in m.roles):
    #                 self.PremiumUsers.append(m.id)
    #         print(
    #             f"{ANSI.WARNING}Updated Premium Members: {ANSI.ENDC} {ANSI.OKGREEN}{len(self.PremiumUsers)}{ANSI.ENDC}"
    #         )

    #     except:
    #         self.cprint("Could Not Update Premium Members", ANSI.FAIL)


# @tasks.loop(hours=1, reconnect=True)
# async def clear_temp(self):
#     files = os.listdir(f"{self.filepath}/temp")
#     s, e = 0, 0
#     for f in files:
#         clean = f.split(".")[0]
#         if clean.isdigit():
#             if int(clean) < int(self.start_tstamp):
#                 try:
#                     os.remove(f"{self.filepath}/temp/{f}")
#                 except:
#                     e += 1
#                 else:
#                     s += 1

#     self.start_tstamp = self.tstamp()
#     print(
#         f"{ANSI.WARNING}Cleared Temp:{ANSI.ENDC} \t {ANSI.OKGREEN}{s} files deleted{ANSI.ENDC}"
#         + (f"\t {ANSI.FAIL}{e} files failed{ANSI.ENDC}" if e > 0 else "")
#     )
