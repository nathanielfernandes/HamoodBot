import discord
from discord.ext import commands

import modules.checks as checks


class Money(commands.Cog):
    """Commands to manage your funds `NEW`"""

    def __init__(self, bot):
        self.bot = bot
        self.cash = lambda n: f"[⌬ {n:,}](https://top.gg/bot/699510311018823680)"
        self.leaderboard_emojis = [
            ":first_place:",
            ":second_place:",
            ":third_place:",
            ":clap:",
            ":clap:",
            ":clap:",
            ":thumbsup:",
            ":thumbsup:",
            ":thumbsup:",
            ":poop:",
        ]

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

    @commands.command(aliases=["bal", "bank", "wallet"])
    @checks.isAllowedCommand()
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def balance(self, ctx, upgrade="nah"):
        """``balance`` get your current balance."""
        bal = await self.bot.currency.get_currency(ctx.guild.id, ctx.author.id)
        if upgrade.lower() == "upgrade":
            if bal is not None:
                if bal["wallet"] >= bal["bank_max"]:
                    n = (bal["bank_max"] * 2) - (bal["bank_max"] // 2)
                    c = n - bal["bank_max"]

                    await self.bot.currency.update_wallet(
                        ctx.guild.id, ctx.author.id, -1 * bal["bank_max"]
                    )

                    await self.bot.currency.update_bank_max(
                        ctx.guild.id, ctx.author.id, c,
                    )

                    embed = discord.Embed(
                        title=f"Bought Bank Upgrade | ⌬ {bal['bank_max']:,} to ⌬ {n:,}",
                        description=f"{ctx.author.mention} successfully purchased `bank upgrade` `+⌬ {c:,}` for {self.cash(bal['bank_max'])}",
                        color=ctx.author.color,
                        timestamp=ctx.message.created_at,
                    )
                    return await ctx.send(embed=embed)

            await ctx.send(
                "`Insufficient Funds!` bank upgrades can only be bought using your wallet balance."
            )

        else:
            p = self.bot.find_prefix(ctx.guild.id)
            items_v = await self.get_items_value(ctx)
            if bal is not None:
                ask = f"\n \nUse `{p}balance upgrade` to increase your max bank storage from ⌬ {bal['bank_max']:,} to ⌬ {(bal['bank_max']*2) - (bal['bank_max']//2):,} for {self.cash(bal['bank_max'])}"

                embed = discord.Embed(
                    title=f"{ctx.author}'s Balance",
                    description=f"**Wallet:** {self.cash(bal['wallet'])}\n**Bank:** {self.cash(bal['bank'])} / ⌬ {bal['bank_max']:,}\n**Items:** {self.cash(items_v)}\n**Networth:** {self.cash(bal['wallet']+bal['bank']+items_v)}{ask if bal['wallet'] >= bal['bank_max'] else ''}",
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
    @commands.cooldown(1, 5, commands.BucketType.user)
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
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, amount):
        """``withdraw [amount]`` withdraws money from the bank into your wallet."""
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
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def transfer(self, ctx, recipient: discord.Member = None, amount=1):
        """``transfer [@member] [amount]`` Transfer funds to another member."""
        if recipient is not None and recipient.id != ctx.author.id:
            amount = abs(int(amount))
            sender = ctx.author
            sender_bal = await self.bot.currency.get_currency(ctx.guild.id, sender.id)

            if sender_bal is not None and sender_bal["bank"] >= amount:
                await self.bot.currency.add_member(ctx.guild.id, recipient.id)
                await self.bot.currency.update_wallet(
                    ctx.guild.id, recipient.id, amount
                )
                await self.bot.currency.update_bank(
                    ctx.guild.id, sender.id, -1 * amount
                )

                embed = discord.Embed(
                    title=f"`{sender}` transfered `⌬ {amount}` to `{recipient}`",
                    description=f"{sender.mention} successfully transfered {self.cash(amount)} to {recipient.mention}",
                    color=ctx.author.color,
                    timestamp=ctx.message.created_at,
                )

                return await ctx.send(embed=embed)

            else:
                await ctx.send(
                    "`Insufficient Funds` Your bank balance can only be transfered."
                )
        else:
            await ctx.send("`The transfer recipient was not specified`")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def richest(self, ctx):
        """``richest`` See the richest members in the server."""
        server = await self.bot.currency.get(ctx.guild.id)

        members = []
        if server is not None:
            for i in server:
                if i != "_id" and server[i]["wallet"] + server[i]["bank"] > 0:
                    members.append(
                        [
                            server[i]["wallet"] + server[i]["bank"],
                            str(self.bot.get_user(int(i))),
                        ]
                    )
        else:
            return await ctx.send("`not enough members have money`")

        players = len(members)
        if players > 10:
            players = 10
        elif players == 0:
            return await ctx.send("`not enough members have money`")

        members = sorted(members)[::-1][:players]
        members = [
            f"{self.leaderboard_emojis[i]} {self.cash(members[i][0])} - {members[i][1]}"
            for i in range(len(members))
        ]

        embed = discord.Embed(
            title=f"{players} Richest Members in this server",
            description="\n".join(members),
            color=discord.Color.gold(),
            timestamp=ctx.message.created_at,
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Money(bot))

