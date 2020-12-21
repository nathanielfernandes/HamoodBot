import discord
from discord.ext import commands

import modules.checks as checks


class Items(commands.Cog):
    """Commands that reach into ur pockets"""

    def __init__(self, bot):
        self.bot = bot

        self.colors = {
            "common": discord.Color.from_rgb(169, 169, 169),
            "uncommon": discord.Color.from_rgb(100, 237, 111),
            "rare": discord.Color.from_rgb(54, 161, 247),
            "epic": discord.Color.from_rgb(189, 69, 230),
            "legendary": discord.Color.from_rgb(242, 206, 75),
            "black market": discord.Color.from_rgb(214, 41, 41),
            "dev": discord.Color.from_rgb(1, 1, 1),
        }

        self.cash = lambda n: f"[⌬ {n:,}](https://top.gg/bot/699510311018823680)"

    def to_id(self, name):
        return name.replace(" ", "_").lower()

    def to_name(self, name):
        return name.replace("_", " ").title()

    def valid_item(self, name):
        return self.to_id(name) in self.bot.items

    async def give_item(self, guild_id, member_id, item_id, amount):
        amount = int(amount)

        if self.valid_item(item_id):
            if await self.bot.inventories.member_has_space(guild_id, member_id, amount):
                await self.bot.inventories.add_inventory(guild_id)
                await self.bot.inventories.add_member(guild_id, member_id)
                await self.bot.inventories.add_item(
                    guild_id, member_id, self.to_id(item_id), amount
                )

                return True
            else:
                return False

    @commands.command()
    async def get_item(self, ctx, item, amount):
        if await self.give_item(ctx.guild.id, ctx.author.id, item, amount):
            await ctx.send(f"you recieved {amount} {item} item")
        else:
            await ctx.send(f"U dont have the space for that!")

    @commands.command()
    async def inventory(self, ctx):
        items = await self.bot.inventories.get_items(ctx.guild.id, ctx.author.id)

        if items is not None:

            total = 0
            desc = ""
            for i in items:
                if i != "item_space":
                    desc += f"{self.bot.items[i]['emoji']} - **{self.to_name(i)}** `x{items[i]}` **|** {self.cash(self.bot.items[i]['price']*int(items[i]))}\n"
                    total += self.bot.items[i]["price"] * int(items[i])

            embed = discord.Embed(
                title=f"{ctx.author}'s Inventory ({items['item_space']['total']}/{items['item_space']['max']})",
                description=f"{desc}",
                timestamp=ctx.message.created_at,
                color=ctx.author.color,
            )

            embed.add_field(name="**⎻**" * 30, value=f"**Total Value:** {self.cash(total)}")

        else:
            embed = discord.Embed(
                title=f"{ctx.author}'s Inventory (0/10)",
                description="This inventory is empty!",
                timestamp=ctx.message.created_at,
                color=ctx.author.color,
            )

        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def iteminfo(self, ctx, *, name: commands.clean_content):
        if self.valid_item(name):
            name = self.to_id(name)
            desc = "\n".join([f"{self.bot.items[name]['info']}"])
            embed = discord.Embed(
                title=f"{self.to_name(name)} | ***{self.bot.items[name]['rarity'].upper()}***",
                description=f"{desc}",
                color=self.colors[self.bot.items[name]["rarity"]],
                timestamp=ctx.message.created_at,
            )

            if self.bot.items[name]["price"] > self.bot.items[name]["value"]:
                arrow = "<:up:790476638034198539>"
            elif self.bot.items[name]["price"] < self.bot.items[name]["value"]:
                arrow = "<:down:790476638319149066>"
            else:
                arrow = ""

            embed.add_field(
                name="**⎻**" * 30,
                value=f"**Current Price**: {self.cash(self.bot.items[name]['price'])} {arrow}\n**Regular Price**: {self.cash(self.bot.items[name]['value'])}",
            )
            embed.set_thumbnail(url=self.bot.items[name]["image"])

            await ctx.send(embed=embed)

        # for i in items:

        # for i in items:
        #     if i.isdigit():
        #         await ctx.send(self.bot.items[i])


def setup(bot):
    bot.add_cog(Items(bot))
