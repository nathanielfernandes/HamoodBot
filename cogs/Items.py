import discord
import random
from discord.ext import commands

import modules.checks as checks


class Items(commands.Cog):
    """Commands to manage your inventory `NEW`"""

    def __init__(self, bot):
        self.bot = bot

        self.colors = {
            "common": discord.Color.from_rgb(169, 169, 169),
            "uncommon": discord.Color.from_rgb(100, 237, 111),
            "rare": discord.Color.from_rgb(54, 161, 247),
            "epic": discord.Color.from_rgb(189, 69, 230),
            "legendary": discord.Color.from_rgb(242, 206, 75),
            "blackmarket": discord.Color.from_rgb(214, 41, 41),
            "dev": discord.Color.from_rgb(1, 1, 1),
        }

        self.rare_ranking = dict(list(self.bot.all_items.items())[::-1])

        self.cash = lambda n: f"[⌬ {n:,}](https://top.gg/bot/699510311018823680)"

    def get_arrow(self, name):
        name = self.to_id(name)
        if self.bot.all_items[name]["price"] > self.bot.all_items[name]["value"]:
            return "<:up:790784452321476628>"
        elif self.bot.all_items[name]["price"] < self.bot.all_items[name]["value"]:
            return "<:down:790784452132732959>"
        else:
            return ""

    def to_id(self, name):
        return name.replace(" ", "_").lower()

    def to_name(self, name):
        return name.replace("_", " ").title()

    def valid_item(self, name):
        return self.to_id(name) in self.bot.all_items

    # @commands.command()
    # async def item_ids(self, ctx, sort_by="rarity"):
    #     """A list of every item id"""
    #     if sort_by == "rarity":
    #         tit = "All Items Sorted"
    #     embed = discord.Embed(title=f"{group} Items | Sorted by {}")
    # async def give_item(self, guild_id, member_id, item_id, amount):
    #     amount = int(amount)

    #     if self.valid_item(item_id):
    #         if await self.bot.inventories.member_has_space(guild_id, member_id, amount):
    #             await self.bot.inventories.add_inventory(guild_id)
    #             await self.bot.inventories.add_member(guild_id, member_id)
    #             await self.bot.inventories.add_item(
    #                 guild_id, member_id, self.to_id(item_id), amount
    #             )ƒ\
    #             return True
    #         else:
    #             return False

    async def give_item(self, guild_id, member_id, item_id, amount):
        amount = int(amount)
        # await self.bot.inventories.add_inventory(guild_id)
        await self.bot.inventories.add_member(guild_id, member_id)
        await self.bot.inventories.add_item(
            guild_id, member_id, self.to_id(item_id), amount
        )

    @commands.command(aliases=["inv"])
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def inventory(self, ctx, sort_by="price", page=1):
        """``inventory [sorting] [page]`` view your current inventory."""
        items = await self.bot.inventories.get_items(ctx.guild.id, ctx.author.id)

        if sort_by.lower() == "upgrade":
            await self.bot.inventories.add_member(ctx.guild.id, ctx.author.id)
            bal = await self.bot.currency.get_currency(ctx.guild.id, ctx.author.id)
            if bal is not None:
                cost = (items["item_space"]["max"] ** 3) // (
                    items["item_space"]["max"] // 3
                )

                if bal["bank"] >= cost:
                    c = items["item_space"]["max"]
                    n = (items["item_space"]["max"] * 2) - (
                        items["item_space"]["max"] // 2
                    )

                    await self.bot.currency.update_bank(
                        ctx.guild.id, ctx.author.id, -1 * cost
                    )

                    await self.bot.inventories.incr_item_max(
                        ctx.guild.id, ctx.author.id, n - c,
                    )

                    embed = discord.Embed(
                        title=f"Bought Inventory Upgrade | `{c}` to `{n}`",
                        description=f"{ctx.author.mention} successfully purchased `inventory upgrade` `+{n-c} space` for {self.cash(cost)}",
                        color=ctx.author.color,
                        timestamp=ctx.message.created_at,
                    )

                    return await ctx.send(embed=embed)

            await ctx.send(
                "`Insufficient Funds!` upgrades can only be bought using your bank balance."
            )

        else:
            if sort_by.isdigit():
                page = int(sort_by)
                sort_by = "price"

            sort_by = sort_by.lower()

            done = False
            if items is not None:
                if items["item_space"]["total"] != 0:
                    total = sum(
                        self.bot.all_items[i]["price"] * int(items[i])
                        for i in items
                        if i != "item_space"
                    )

                    desc, n = await self.sort_items("inventory", sort_by, page, items)

                    if desc != None:
                        msg = f"Sorted by {sort_by.capitalize()}\n{desc}"
                    else:
                        msg = f"`No items that match the criteria`"

                    embed = discord.Embed(
                        title=f"{ctx.author}'s Inventory ({items['item_space']['total']}/{items['item_space']['max']})",
                        description=msg,
                        timestamp=ctx.message.created_at,
                        color=ctx.author.color,
                    )

                    embed.add_field(
                        name=f"<:blank:794679084890193930>",
                        value=f"**Total Value:** {self.cash(total)}\n \nUse `.inventory{f' {sort_by} ' if sort_by != 'price' else ' '}{page+1 if page+1 <= n else 1}` to view the next page.\nUse `.inventory upgrade` to increase your max inventory space from `{items['item_space']['max']}` to `{(items['item_space']['max']*2)-items['item_space']['max']//2}` for {self.cash((items['item_space']['max']**3)//(items['item_space']['max']//3))}\n",
                    )

                    embed.set_footer(text=f"Page ({page}/{n})")
                    done = True

            if not done:
                embed = discord.Embed(
                    title=f"{ctx.author}'s Inventory (0/10)",
                    description="This inventory is empty!",
                    timestamp=ctx.message.created_at,
                    color=ctx.author.color,
                )

                embed.set_footer(text=f"Go get some items.")

            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def iteminfo(self, ctx, *, name: commands.clean_content):
        """``iteminfo [item name]`` get information on an item."""
        if self.valid_item(name):
            name = self.to_id(name)
            desc = "\n".join([f"{self.bot.all_items[name]['info']}"])
            embed = discord.Embed(
                title=f"{self.to_name(name)} | ***{self.bot.all_items[name]['rarity'].upper()}*** {' | `In Shop`' if name in self.bot.shop else ''}",
                description=f"{desc}",
                color=self.colors[self.bot.all_items[name]["rarity"]],
                timestamp=ctx.message.created_at,
            )

            buy = f"Use `.buy {name} 1` to purchase."

            embed.add_field(
                name=f"<:blank:794679084890193930>",
                value=f"**Current Price**: {self.cash(self.bot.all_items[name]['price'])} {self.get_arrow(name)}\n**Regular Price**: {self.cash(self.bot.all_items[name]['value'])}\n \nitem_id: `{name}`\n{buy if name in self.bot.shop else ''}type: `{self.bot.all_items[name]['type']}`",
            )
            embed.set_thumbnail(url=self.bot.all_items[name]["image"])

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"`that item does not exist`")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def itemlist(self, ctx, sort_by="price", page=1):
        """``itemlist [sorting] [page]`` View all the items that you could get."""
        if sort_by.isdigit():
            page = int(sort_by)
            sort_by = "price"

        sort_by = sort_by.lower()

        items, n = await self.sort_items("itemlist", sort_by, page)

        embed = discord.Embed(
            title=f"All Items | Sorted by {sort_by.capitalize()} ({page}/{n})",
            description=f"{items}\n<:blank:794679084890193930>\nUse `.itemlist{f' {sort_by} ' if sort_by != 'price' else ' '}{page+1 if page+1 <= n else 1}` to view the next page.\nUse `.iteminfo [item name]` to find out more about an item.",
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
        )

        embed.set_footer(text=f"Page ({page}/{n})")
        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def open(self, ctx, item_id):
        """``open [crate_id]`` used to open crates"""
        item_id = self.to_id(item_id)
        if item_id in self.bot.crates:
            inv = await self.bot.inventories.get_items(ctx.guild.id, ctx.author.id)

            if inv is not None and item_id in inv:
                if await self.bot.inventories.member_has_space(
                    ctx.guild.id, ctx.author.id, self.bot.crates[item_id]["contains"]
                ):
                    reward = {}
                    for i in range(self.bot.crates[item_id]["contains"]):
                        ran = random.randint(1, 100)
                        if item_id == "blackmarket_crate":
                            if ran <= 80:
                                choice = self.bot.rare_items
                            elif ran <= 93:
                                choice = self.bot.epic_items
                            elif ran <= 98:
                                choice = self.bot.legendary_items
                            else:
                                choice = self.bot.blackmarket_items

                        elif item_id == "rare_crate":
                            if ran <= 20:
                                choice = self.bot.common_items
                            elif ran <= 50:
                                choice = self.bot.uncommon_items
                            else:
                                choice = self.bot.rare_items

                        k, v = random.choice(list(choice.items()))

                        reward[k] = 1 if k not in reward else reward[k] + 1

                    for item in reward:
                        await self.bot.inventories.incr_item_amount(
                            ctx.guild.id, ctx.author.id, item, reward[item]
                        )

                    await self.bot.inventories.decr_item_amount(
                        ctx.guild.id, ctx.author.id, item_id, 1
                    )

                    item_desc = (
                        lambda i: f"{self.bot.all_items[i]['emoji']} - **{self.to_name(i)}** `x{reward[i]}` **|** {self.cash(self.bot.all_items[i]['price']*int(reward[i]))}"
                    )

                    desc = "\n".join([item_desc(i) for i in reward])

                    embed = discord.Embed(
                        title=f"Opened {self.to_name(item_id)}",
                        description=f"{ctx.author.mention} opened a `{item_id}` and recieved\n<:blank:794679084890193930>\n{desc}",
                        color=ctx.author.color,
                        timestamp=ctx.message.created_at,
                    )
                    embed.set_thumbnail(url=self.bot.crates[item_id]["image"])

                    await ctx.send(embed=embed)

                else:
                    await ctx.send("`Insufficient Space!`")
            else:
                await ctx.send("`You dont have that item!`")
        else:
            await ctx.send(
                "`Invalid Item` Use `.iteminfo [item name]` to find its `item_id`"
            )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buy(self, ctx, item_id, amount=1):
        """``buy [item_id] [amount]`` buy an item using your bank's funds."""
        amount = abs(int(amount))
        if amount == 0:
            amount = 1
        if self.valid_item(item_id):
            if self.to_id(item_id) in self.bot.shop:
                if await self.bot.inventories.member_has_space(
                    ctx.guild.id, ctx.author.id, amount
                ):
                    bal = await self.bot.currency.get_currency(
                        ctx.guild.id, ctx.author.id
                    )
                    if bal is not None:
                        item_id = self.to_id(item_id)
                        item = self.bot.all_items[item_id]

                        cost = item["price"] * amount

                        if bal["bank"] >= cost:
                            await self.bot.currency.update_bank(
                                ctx.guild.id, ctx.author.id, -1 * cost
                            )
                            await self.give_item(
                                ctx.guild.id, ctx.author.id, item_id, amount
                            )

                            embed = discord.Embed(
                                title=f"Bought {self.to_name(item_id)} `x{amount}`",
                                description=f"{ctx.author.mention} successfully purchased `{item_id}` `x{amount}` for {self.cash(cost)}",
                                color=ctx.author.color,
                                timestamp=ctx.message.created_at,
                            )

                            embed.set_thumbnail(
                                url=self.bot.all_items[item_id]["image"]
                            )

                            return await ctx.send(embed=embed)
                    await ctx.send(
                        "`Insufficient Funds!` Items can only be bought using your bank balance."
                    )
                else:
                    await ctx.send("`Insufficient Space!`")
            else:
                await ctx.send("`That item cannot currently be bought`")
        else:
            await ctx.send(
                "`Invalid Item` Use `.iteminfo [item name]` to find its `item_id`"
            )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sell(self, ctx, item_id, amount=1):
        """``sell [item_id] [amount]`` sell your items for cash."""
        if isinstance(amount, str) and amount.lower() == "all":
            amount = abs(int(amount))
            if amount == 0:
                amount = 1
        if self.valid_item(item_id):
            item_id = self.to_id(item_id)
            item = self.bot.all_items[item_id]
            if item["type"] != "sellable":
                return await ctx.send("`That Item cannot be sold`")
            items = await self.bot.inventories.get_items(ctx.guild.id, ctx.author.id)
            if items is not None and item_id in items:
                if isinstance(amount, str) and amount.lower() == "all":
                    amount = items[item_id]
                if items[item_id] >= amount:
                    value = item["price"] * amount
                    # await self.bot.currency.add_server(ctx.guild.id)
                    await self.bot.currency.add_member(ctx.guild.id, ctx.author.id)
                    await self.bot.currency.update_wallet(
                        ctx.guild.id, ctx.author.id, value
                    )
                    await self.bot.inventories.decr_item_amount(
                        ctx.guild.id, ctx.author.id, item_id, amount
                    )

                    embed = discord.Embed(
                        title=f"Sold {self.to_name(item_id)} `x{amount}`",
                        description=f"{ctx.author.mention} successfully sold `{item_id}` `x{amount}` for {self.cash(value)}",
                        color=ctx.author.color,
                        timestamp=ctx.message.created_at,
                    )
                    embed.set_thumbnail(url=self.bot.all_items[item_id]["image"])

                    return await ctx.send(embed=embed)

            await ctx.send("`Insufficient Items!`")
        else:
            await ctx.send(
                "`Invalid Item` Use `.iteminfo [item name]` to find its `item_id`"
            )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def trash(self, ctx, item_id, amount=1):
        """``trash [item_id] [amount]`` Throw out unwanted items."""
        if isinstance(amount, str) and amount.lower() == "all":
            amount = abs(int(amount))
        if self.valid_item(item_id):
            item_id = self.to_id(item_id)
            item = self.bot.all_items[item_id]
            items = await self.bot.inventories.get_items(ctx.guild.id, ctx.author.id)
            if items is not None and item_id in items:
                if isinstance(amount, str) and amount.lower() == "all":
                    amount = item[item_id]
                if items[item_id] >= amount:
                    # await self.bot.currency.add_server(ctx.guild.id)
                    await self.bot.currency.add_member(ctx.guild.id, ctx.author.id)
                    await self.bot.inventories.decr_item_amount(
                        ctx.guild.id, ctx.author.id, item_id, amount
                    )
                    embed = discord.Embed(
                        title=f"Trashed {self.to_name(item_id)} `x{amount}`",
                        description=f"{ctx.author.mention} successfully trashed `{item_id}` `x{amount}`",
                        color=ctx.author.color,
                        timestamp=ctx.message.created_at,
                    )
                    embed.set_thumbnail(url=self.bot.all_items[item_id]["image"])

                    return await ctx.send(embed=embed)

            await ctx.send("`Insufficient Items!`")
        else:
            await ctx.send(
                "`Invalid Item` Use `.iteminfo [item name]` to find its `item_id`"
            )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gift(
        self, ctx, recipient: discord.Member = None, item_id="1234", amount=1
    ):
        """``gift [@member] [item_id] [amount]`` Gift items to other members."""
        if recipient is not None and recipient.id != ctx.author.id:
            if self.valid_item(item_id):
                amount = abs(int(amount))
                sender = ctx.author
                sender_items = await self.bot.inventories.get_items(
                    ctx.guild.id, sender.id
                )

                if sender_items is not None and item_id in sender_items:
                    if sender_items[item_id] >= amount:
                        await self.bot.inventories.add_member(
                            ctx.guild.id, recipient.id
                        )
                        if await self.bot.inventories.member_has_space(
                            ctx.guild.id, recipient.id, amount
                        ):
                            await self.bot.inventories.decr_item_amount(
                                ctx.guild.id, sender.id, item_id, amount
                            )
                            await self.bot.inventories.incr_item_amount(
                                ctx.guild.id, recipient.id, item_id, amount
                            )

                            embed = discord.Embed(
                                title=f"`{sender}` gifted `{recipient}` **{self.to_name(item_id)}**",
                                description=f"{sender.mention} successfully gifted {recipient.mention} `{self.to_id(item_id)}` `x{amount}`",
                                color=ctx.author.color,
                                timestamp=ctx.message.created_at,
                            )
                            embed.set_thumbnail(
                                url=self.bot.all_items[item_id]["image"]
                            )

                            return await ctx.send(embed=embed)

                        else:
                            await ctx.send(
                                f"`{recipient}'s inventory does not have the space required`"
                            )
                    else:
                        await ctx.send("'Insufficient Items'")
                else:
                    await ctx.send("`You dont have that item`")
            else:
                await ctx.send("`That item does not exist`")
        else:
            await ctx.send("`The gift recipient was not specified`")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def shop(self, ctx, page=1):
        """``shop [page]`` view the current items you can buy."""
        items, n = await self.sort_items("shop", "shop", page)

        embed = discord.Embed(
            title=f"Item Shop ({page}/{n})",
            description=f"<:blank:794679084890193930>\n{items}\n<:blank:794679084890193930>\nUse `.buy [item_id] [amount]` to buy an item.\nUse `.shop {page+1 if page+1 <= n else 1}` to view the next page.\nUse `.iteminfo [item name]` to find out more about an item.",
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
        )

        embed.set_footer(text=f"Page ({page}/{n}). Prices and stock change hourly")
        await ctx.send(embed=embed)

    async def sort_items(self, og="itemlist", sort_by="price", page=1, inv=None):
        n = 12
        if sort_by == "price":
            temp = sorted(
                [[self.bot.all_items[i]["price"], i] for i in self.bot.all_items]
            )

            temp = {i[1]: self.bot.all_items[i[1]] for i in temp}
        elif sort_by == "shop":
            n = 10
            temp = self.bot.shop
        elif sort_by == "rarity":
            temp = self.rare_ranking
        elif sort_by == "common":
            temp = self.bot.common_items
        elif sort_by == "uncommon":
            temp = self.bot.uncommon_items
        elif sort_by == "rare":
            temp = self.bot.rare_items
        elif sort_by == "epic":
            temp = self.bot.epic_items
        elif sort_by == "legendary":
            temp = self.bot.legendary_items
        elif sort_by == "blackmarket":
            temp = self.bot.blackmarket_items
        elif sort_by == "dev":
            temp = self.bot.dev_items
        elif sort_by == "crates":
            temp = self.bot.crates

        if og == "itemlist":
            item_desc = (
                lambda items, i: [
                    f"{items[i]['emoji']} - **{self.to_name(i)}** **|** {self.cash(items[i]['price'])} {self.get_arrow(i)} {'`In Shop`' if i in self.bot.shop else ''}"
                ]
                if items[i]["type"] != "crate" or sort_by == "crates"
                else []
            )
        elif og == "inventory":
            item_desc = (
                lambda items, i: [
                    f"{items[i]['emoji']} - **{self.to_name(i)}** `x{inv[i]}` **|** {self.cash(self.bot.all_items[i]['price']*int(inv[i]))}"
                ]
                if i in inv
                else []
            )
        elif og == "shop":
            item_desc = lambda items, i: [
                f"{items[i]['emoji']} - **{self.to_name(i)}** **|** {self.cash(items[i]['price'])} {self.get_arrow(i)}\n    **↳** `{self.to_id(i)}` ***{items[i]['rarity']}***\n"
            ]
        # elif og == "shop":
        #     item_desc = lambda items, i: [
        #         f"{items[i]['emoji']} - **{self.to_name(i)}** **|** {self.cash(items[i]['price'])} {self.get_arrow(i)}"
        #     ]

        pages = []
        for i in temp:
            pages += item_desc(temp, i)

        pages = [pages[i * n : (i + 1) * n] for i in range((len(pages) + n - 1) // n)]

        if len(pages) == 0:
            return None, 1

        if page < 1:
            page = 1
        elif page > len(pages):
            page = len(pages)

        select_page = "\n".join(pages[int(page) - 1])

        return select_page, len(pages)


def setup(bot):
    bot.add_cog(Items(bot))
