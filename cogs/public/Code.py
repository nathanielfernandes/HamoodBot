# import requests
import aiohttp
import discord
from discord.ext import commands
import os
import json


class Code(commands.Cog):
    """Test your big brain code `NEW`"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.language_info = json.load(
            open(f"{self.Hamood.filepath}/data/languageinfo.json")
        )

    def addcodecommands(self):
        for lang in self.language_info:

            @commands.command(
                name=lang,
                help=f"<code>|||Executes your {self.language_info[lang]['name']} code.",
                aliases=self.language_info[lang]["aliases"],
            )
            @commands.cooldown(1, 5, commands.BucketType.channel)
            @commands.max_concurrency(1, commands.BucketType.default, wait=True)
            async def cmd(
                self, ctx, *, code: commands.clean_content(remove_markdown=True)
            ):
                await self.run_code(ctx, ctx.command.name, code)

            cmd.cog = self
            self.__cog_commands__ = self.__cog_commands__ + (cmd,)
            self.bot.add_command(cmd)

    async def run_code(self, ctx, language, code):
        data = {
            "language": language,
            "source": code,
        }
        r = await self.Hamood.ahttp.post(
            url="https://emkc.org/api/v1/piston/execute",
            data=data,
            return_type="json",
            timeout=10,
        )

        if "message" not in r:
            output = (
                r["output"]
                if len(r["output"]) <= 1900
                else r["output"][:1900] + " Exceded Character Limit!"
            )

            embed = discord.Embed(
                description=f"{ctx.author.mention}'s Code:```yaml\n{output}```",
                color=discord.Color.from_rgb(96, 181, 221),
            )

            embed.set_author(
                name="Powered by Piston",
                url="https://github.com/engineer-man/piston",
                icon_url="https://cdn.discordapp.com/attachments/790722696219983902/853802396274130944/unknown.png",
            )
            embed.set_footer(
                text=f"{self.language_info[r['language']]['name']} - {r['version']}",
                icon_url=self.language_info[r["language"]]["logo"],
            )
            await ctx.reply(embed=embed, mention_author=False)
        else:
            return await ctx.send("`Sorry, I couldn't run code at that moment`")


def setup(bot):
    cog = Code(bot)
    bot.add_cog(cog)
    cog.addcodecommands()
