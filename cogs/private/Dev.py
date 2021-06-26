import os
import discord
from discord.ext import commands
import asyncio
import re, json


class Dev(commands.Cog):
    """Dev Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

    #  self.courses = json.load(open("junk/aggrCourses.json"))
    @commands.is_owner()
    def to_id(self, name):
        return name.replace(" ", "_").lower()

    @commands.command()
    @commands.is_owner()
    async def make_premium(self, ctx, _id: int):
        """s|||s"""
        self.Hamood.PremiumUsers.append(int(_id))

    @commands.command()
    @commands.is_owner()
    async def premiums(self, ctx):
        """s|||s"""
        await ctx.send(":" + "\n".join(str(i) for i in self.Hamood.PremiumUsers))
        # self.Hamood.quick_embed(title=course_info["name"], description=course_info["description"], color)

    @commands.command()
    @commands.is_owner()
    async def html(self, ctx):
        icons = {
            "Games": "fas fa-gamepad",
            "Subreddits": "fab fa-reddit",
            "MemeGen": "fas fa-images",
            "Math": "fas fa-square-root-alt",
            "Chemistry": "fas fa-atom",
            "Items": "fas fa-box-open",
            "Money": "fas fa-wallet",
            "Jobs": "fas fa-briefcase",
            "Mod": "fas fa-gavel",
            "Utility": "fas fa-cogs",
            "Code": "fas fa-code",
            "Fonts": "fas fa-font",
            "Fun": "fas fa-laugh-wink",
            "General": "fas fa-align-left",
            "User": "fas fa-user",
            "About": "fas fa-info",
        }

        f = open("commands.html", "w")
        s = lambda s: re.findall("``([^``]*)``", s)

        html = ""
        for cog in icons:
            html += '<div class="command-section">\n'
            html += f'<h1><i class="{icons[cog]}"></i> {cog}</h1>\n'
            for c in self.bot.get_cog(cog).get_commands():
                if c.help != None:
                    h = c.help.split("|||")
                    html += f"<li><b>{c.name} {h[0].replace('<', '&lt;').replace('>', '&gt;')}</b> {h[1]}</li>\n"

            html += "</div>\n\n"

        f.write(html)
        f.close()
        # print(html)
        await ctx.send(file=discord.File("commands.html"))

    # @commands.command()
    # async def test1(self, ctx):
    #     embed = discord.Embed(
    #         title="<:cac:828227363611082752>",
    #         description="<:cac:828227363611082752>\n[`♠k`](https://top.gg/bot/699510311018823680)",
    #     )

    #     await ctx.send(embed=embed)

    #     meme = f"{self.Hamood.filepath}/memePics/video0.mov"

    #     name = os.path.basename(meme)
    #     embed = discord.Embed()

    #     embed.set_image(url=f"attachment://{name}")

    #     await ctx.send(file=discord.File(meme), embed=embed)
    # embed = self.Hamood.quick_embed(member=ctx.author, rainbow=True, requested=True)
    # self.bot.S3.schedule_upload(
    #     f"{self.Hamood.filepath}/memePics/10mbtest.jpg",
    #     ctx.channel.id,
    #     embed=embed,
    #     delete_file=False,
    # )

    @commands.command()
    async def cliffhanger(self, ctx):
        """``cliffhanger`` the day hamood died"""
        await ctx.send(
            "https://cdn.discordapp.com/attachments/767568685568753664/804052279195467796/unknown.png"
        )

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        """``logout`` logs hamood out"""
        await ctx.send("**goodbye**")
        await self.Hamood.ahttp.close()
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, aType: str, uRL: str, *, aName: commands.clean_content):
        """``status [type] [url] [activity]`` lets me change hamoods status"""
        if aType == "playing":
            await self.bot.change_presence(activity=discord.Game(name=aName))
        elif aType == "listening":
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening, name=aName
                )
            )
        elif aType == "watching":
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=aName
                )
            )
        elif aType == "streaming":
            await self.bot.change_presence(
                activity=discord.Streaming(name=aName, url=uRL)
            )

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        """``reload [cog name]`` reloads the requested cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            loaded = self.bot.get_cog(cog.split(".")[1])
            loaded.public = "public" in cog
            await ctx.send(f"`{cog} got reloaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be loaded`")
            raise e

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog):
        """``unload [cog name]`` unloads the requested cog"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog} got unloaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be unloaded:`")
            raise e

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog):
        """``load [cog name]`` loads the requested cog"""
        try:
            self.bot.load_extension(f"cogs.{cog}")
            loaded = self.bot.get_cog(cog.split(".")[1])
            loaded.public = "public" in cog
            await ctx.send(f"`{cog} got loaded`")
        except Exception as e:
            await ctx.send(f"`{cog} cannot be loaded:`")
            raise

    @commands.command()
    @commands.is_owner()
    async def gameslog(self, ctx):
        await ctx.send("```" + str(self.Hamood.active_games) + "```")
        # log = "\n".join([f"{self.Hamood.active_games_log[k]} | {k}" for k in self.Hamood.active_games_log])
        # await ctx.send(f"```{len(self.Hamood.active_games_log)} Games:\n{log}```")

    @commands.command()
    @commands.is_owner()
    async def get_item(self, ctx, item_id, amount=1):
        """``get_item [item_id] [amount]`` get any item"""
        amount = int(amount)
        await self.Hamood.Inventories.add_inventory(ctx.guild.id)
        await self.Hamood.Inventories.add_member(ctx.guild.id, ctx.author.id)
        await self.Hamood.Inventories.add_item(
            ctx.guild.id, ctx.author.id, self.to_id(item_id), int(amount)
        )
        await ctx.send(f"`You recieved {item_id} x{amount}`")

    @commands.command()
    @commands.is_owner()
    async def print_money(self, ctx, amount):
        """``print_money [amount]`` get any amount of money"""
        await self.Hamood.Currency.add_server(ctx.guild.id)
        await self.Hamood.Currency.add_member(ctx.guild.id, ctx.author.id)
        await self.Hamood.Currency.update_wallet(
            ctx.guild.id, ctx.author.id, int(amount)
        )

        await ctx.send(f"`You recieved ⌬ {int(amount):,}`")

    @commands.command()
    @commands.is_owner()
    async def wipe(self, ctx, member: discord.Member = None):
        if member is not None:
            # await self.Hamood.Leaderboards.delete_member(member.guild.id, member.id)
            await self.Hamood.Currency.delete_member(member.guild.id, member.id)
            await self.Hamood.Inventories.delete_member(member.guild.id, member.id)

            await ctx.send(f"{member.mention} has been wiped from the db")

    @commands.command()
    @commands.is_owner()
    async def silence(self, ctx, member: discord.Member = None, hours=None):
        if member is not None:
            if member.id in self.Hamood.timeout_list:
                self.Hamood.timeout_list.remove(member.id)
                await ctx.send(f"**{member}** has been taken out of time out.")
            else:
                self.Hamood.timeout_list.append(member.id)
                if hours is None:
                    await ctx.send(
                        f"**{member}** has been put in time out. `Indefinitely`"
                    )
                else:
                    time = 3600 * hours
                    await ctx.send(
                        f"**{member}** has been put in time out for {self.Hamood.pretty_dt(time)}"
                    )
                    await asyncio.sleep(time)
                    self.Hamood.timeout_list.remove(member.id)

    @commands.command()
    @commands.is_owner()
    async def inspect(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        content = await ctx.send(
            f"`Gathering information on {member}...` <a:loading:856302946274246697>"
        )
        await asyncio.sleep(3)

        msg = f"```ini\n[username]: {member}"
        msg += f"\n[id]: {member.id}"
        msg += f"\n[created at]: {member.created_at}"
        msg += f"\n[is bot?]: {member.bot}"
        msg += f"\n[in timeout?]: {member.id in self.Hamood.timeout_list}\n"

        servers, bal = await self.Hamood.Currency.find_all_of_member(member.id)
        total = await self.Hamood.Inventories.find_all_of_member(member.id)
        won, lost = await self.Hamood.Leaderboards.find_all_of_member(member.id)
        servers = [self.bot.get_guild(int(g)) for g in servers]
        servers = "\n - ".join(
            [f"{g.name} ({g.member_count} users)" for g in servers if g is not None]
        )
        msg += f"\n[known servers]:\n - {servers}\n"
        try:
            ready, time, streak = await self.Hamood.Members.is_daily_ready(member.id)
            msg += f"\n[daily]:\n - ready?: {ready}\n - timeleft: {time:0.0f}s\n - streak: {streak}\n"
        except:
            pass

        msg += f"\n[total balance (across {bal['total']} servers)]:\n - wallet: ⌬ {bal['wallet']:,}\n - bank: ⌬ {bal['bank']:,}\n"
        msg += f"\n[total items (across {bal['total']} servers)]:\n - {total:,}\n"
        msg += f"\n[total leaderboard (across {bal['total']} servers)]:\n - won: {won:,}\n - lost: {lost:,}\n"
        msg += "```"

        embed = discord.Embed(
            title=f"User Details (Hamood) - {member.display_name}",
            colour=member.color,
            timestamp=ctx.message.created_at,
            description=msg,
        )

        embed.set_thumbnail(url=member.avatar_url)
        await content.edit(embed=embed, content=None)

    @commands.command()
    @commands.is_owner()
    async def timeout_corner(self, ctx):
        corner = "\n".join(
            [str(self.bot.get_user(id_)) for id_ in self.Hamood.timeout_list]
        )
        await ctx.send(f"```{corner}```")

    @commands.command()
    async def imposter(self, ctx):
        await ctx.send(
            "**jali-clarke** is *sussy*\nhttps://github.com/nathanielfernandes/HamoodBot/pull/42"
        )

    # @commands.command()
    # async def mac(self, ctx, *, course: commands.clean_content):
    #     course = course.upper()

    #     course_info = self.courses.get(course)
    #     if course_info:
    #         name = course_info["name"].split(" - ")
    #         desc = f"{course_info['description']}\n"
    #         embed = discord.Embed(
    #             title=f"`{name[0]}` | {course_info['units']}",
    #             description=f"**{name[1]}**\n" + course_info["description"] + "\n",
    #             color=discord.Color.from_rgb(148, 0, 73),
    #             timestamp=ctx.message.created_at,
    #         )
    #         embed.set_author(name="McMaster Course Information",)
    #         embed.add_field(
    #             name="Extra Information",
    #             value=course_info["other"]
    #             .replace("Prerequisite(s):", "**Prerequisite(s):**")
    #             .replace("Antirequisite(s):", "**Antirequisite(s):**")
    #             .replace("Cross-list(s):", "**Cross-list(s):**"),
    #         )

    #         embed.set_thumbnail(
    #             url="https://www.mcmasterforum.org/images/default-source/default-album/op_visual-media_web-photo_logo_mcmaster_400x400_maroon.png?sfvrsn=7a0255d5_0"
    #         )

    #         embed.set_footer(text=f"Requested by {ctx.author}")
    #         await ctx.reply(embed=embed)
    #     else:
    #         await ctx.reply(f"Could not find information on the course `{course}`")


def setup(bot):
    bot.add_cog(Dev(bot))