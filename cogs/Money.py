import discord
from discord.ext import commands

import modules.checks as checks


class Money(commands.Cog):
    """Commands that reach into ur pockets"""

    def __init__(self, bot):
        self.bot = bot
        self.cash = lambda n: f"[⌬ {n:,}](https://top.gg/bot/699510311018823680)"

    async def get_items_value(self, ctx):
        items = await self.bot.inventories.get_items(ctx.guild.id, ctx.author.id)

        if items is not None:
            total = sum(
                self.bot.all_items[i]["price"] * int(items[i])
                for i in items
                if i != "item_space"
            )
            return total
        else:
            return 0

    @commands.command(aliases=["bal"])
    @checks.isAllowedCommand()
    async def balance(self, ctx):
        """``balance`` get your current balance."""
        bal = await self.bot.currency.get_currency(ctx.guild.id, ctx.author.id)
        items_v = await self.get_items_value(ctx)
        if bal is not None:
            embed = discord.Embed(
                title=f"{ctx.author}'s Balance",
                description=f"**Wallet:** {self.cash(bal['wallet'])}\n**Bank:** {self.cash(bal['bank'])} / ⌬ {bal['bank_max']:,}\n**Items:** {self.cash(items_v)}\n**Networth:** {self.cash(bal['wallet']+bal['bank']+items_v)}",
                timestamp=ctx.message.created_at,
                color=ctx.author.color,
            )
        else:
            embed = discord.Embed(
                title=f"{ctx.author}'s Balance",
                description=f"**Wallet:** {self.cash(0)}\n**Bank:** {self.cash(0)} / ⌬ {500:,}\n**Items:** {self.cash(items_v)}\n**Networth:** {self.cash(items_v)}",
                timestamp=ctx.message.created_at,
                color=ctx.author.color,
            )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["dep"])
    @checks.isAllowedCommand()
    async def deposit(self, ctx, amount):
        """``deposit [amount]`` deposit money into the bank for safe keeping."""
        if amount == "all" or amount == "max":
            amount = 100000000000000000000000000

        a = await self.bot.currency.wallet_to_bank(
            ctx.guild.id, ctx.author.id, abs(int(amount))
        )

        if isinstance(a, str):
            msg = (
                f"{ctx.author.mention} you don't have the funds to do that."
                if a == "broke"
                else f"{ctx.author.mention} your bank is full."
            )
        else:
            if a is not None:
                msg = f"{ctx.author.mention} {self.cash(a)} was deposited to your bank."
            else:
                msg = f"{ctx.author.mention} you don't have the funds to do that."

        embed = discord.Embed(
            title="ATM Depositing",
            description=msg,
            timestamp=ctx.message.created_at,
            color=ctx.author.color,
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=["wit"])
    @checks.isAllowedCommand()
    async def withdraw(self, ctx, amount):
        """``withdraw [amount]`` withdraw's money from the bank into your wallet."""
        if amount == "all" or amount == "max":
            amount = 100000000000000000000000000

        a = await self.bot.currency.bank_to_wallet(
            ctx.guild.id, ctx.author.id, abs(int(amount))
        )

        if a is None:
            msg = f"{ctx.author.mention} you don't have the funds to do that."
        else:
            msg = f"{ctx.author.mention} {self.cash(a)} was withdrawn from your bank."

        embed = discord.Embed(
            title="ATM Withdrawing",
            description=msg,
            timestamp=ctx.message.created_at,
            color=ctx.author.color,
        )

        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    async def print_money(self, ctx, amount):
        """this not fo u"""
        await self.bot.currency.add_server(ctx.guild.id)
        await self.bot.currency.add_member(ctx.guild.id, ctx.author.id)
        await self.bot.currency.update_wallet(ctx.guild.id, ctx.author.id, int(amount))

        await ctx.send("printed da money dawg")


def setup(bot):
    bot.add_cog(Money(bot))
