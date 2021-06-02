import discord
import random
from discord.ext import commands
from datetime import datetime
import modules.checks as checks


class Items(commands.Cog):
    """Commands to manage your inventory `NEW`"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

        self.colors = {
            "common": discord.Color.from_rgb(169, 169, 169),
            "uncommon": discord.Color.from_rgb(100, 237, 111),
            "rare": discord.Color.from_rgb(54, 161, 247),
            "epic": discord.Color.from_rgb(189, 69, 230),
            "legendary": discord.Color.from_rgb(242, 206, 75),
            "blackmarket": discord.Color.from_rgb(214, 41, 41),
            "dev": discord.Color.from_rgb(1, 1, 1),
        }

        self.rare_ranking = dict(list(self.Hamood.market.all_items.items())[::-1])

        self.cash = lambda n: f"[⌬ {n:,}](https://top.gg/bot/699510311018823680)"

    def get_percent(self, item_id):
        if self.Hamood.market.all_items[item_id]["value"] > 0:
            percent = round(
                (
                    (
                        self.Hamood.market.all_items[item_id]["price"]
                        - self.Hamood.market.all_items[item_id]["value"]
                    )
                    / self.Hamood.market.all_items[item_id]["value"]
                )
                * 100
            )
            return f"`{'+' if percent > 0 else ''}{percent}%`" if percent != 0 else ""
        else:
            return ""

    def get_arrow(self, name):
        name = self.to_id(name)
        if (
            self.Hamood.market.all_items[name]["price"]
            > self.Hamood.market.all_items[name]["value"]
        ):
            return "<:up:790784452321476628>"
        elif (
            self.Hamood.market.all_items[name]["price"]
            < self.Hamood.market.all_items[name]["value"]
        ):
            return "<:down:790784452132732959>"
        else:
            return ""

    def to_id(self, name):
        return name.replace(" ", "_").lower()

    def to_name(self, name):
        return name.replace("_", " ").title()

    def valid_item(self, name):
        return self.to_id(name) in self.Hamood.market.all_items

    # @commands.command()
    # async def item_ids(self, ctx, sort_by="rarity"):
    #     """A list of every item id"""
    #     if sort_by == "rarity":
    #         tit = "All Items Sorted"
    #     embed = discord.Embed(title=f"{group} Items | Sorted by {}")
    # async def give_item(self, guild_id, member_id, item_id, amount):
    #     amount = int(amount)

    #     if self.valid_item(item_id):
    #         if await self.Hamood.Inventories.member_has_space(guild_id, member_id, amount):
    #             await self.Hamood.Inventories.add_inventory(guild_id)
    #             await self.Hamood.Inventories.add_member(guild_id, member_id)
    #             await self.Hamood.Inventories.add_item(
    #                 guild_id, member_id, self.to_id(item_id), amount
    #             )ƒ\
    #             return True
    #         else:
    #             return False

    async def give_item(self, guild_id, member_id, item_id, amount):
        amount = int(amount)
        # await self.Hamood.Inventories.add_inventory(guild_id)
        await self.Hamood.Inventories.add_member(guild_id, member_id)
        await self.Hamood.Inventories.add_item(
            guild_id, member_id, self.to_id(item_id), amount
        )

    @commands.command(aliases=["inv"])
    @checks.isAllowedCommand()
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def inventory(self, ctx, sort_by="price", page=1):
        """``inventory [sorting] [page]`` view your current inventory."""
        items = await self.Hamood.Inventories.get_items(ctx.guild.id, ctx.author.id)

        if sort_by.lower() == "upgrade":
            await self.Hamood.Inventories.add_member(ctx.guild.id, ctx.author.id)
            bal = await self.Hamood.Currency.get_currency(ctx.guild.id, ctx.author.id)
            if bal is not None:
                cost = (items["item_space"]["max"] ** 3) // (
                    items["item_space"]["max"] // 6
                )

                if bal["bank"] >= cost:
                    c = items["item_space"]["max"]
                    n = (items["item_space"]["max"] * 2) - (
                        items["item_space"]["max"] // 2
                    )

                    await self.Hamood.Currency.update_bank(
                        ctx.guild.id, ctx.author.id, -1 * cost
                    )

                    await self.Hamood.Inventories.incr_item_max(
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
                        self.Hamood.market.all_items[i]["price"] * int(items[i])
                        for i in items
                        if i != "item_space"
                    )

                    desc, n = await self.sort_items("inventory", sort_by, page, items)

                    if desc != None:
                        msg = f"Sorted by {sort_by.capitalize()}\n{desc}"
                    else:
                        msg = f"`No items that match the criteria`"

                    p = self.Hamood.find_prefix(ctx.guild.id)
                    embed = discord.Embed(
                        title=f"{ctx.author}'s Inventory ({items['item_space']['total']}/{items['item_space']['max']})",
                        description=msg,
                        timestamp=ctx.message.created_at,
                        color=ctx.author.color,
                    )

                    embed.add_field(
                        name=f"<:blank:794679084890193930>",
                        value=f"**Total Value:** {self.cash(total)}\n \nUse `{p}inventory{f' {sort_by} ' if sort_by != 'price' else ' '}{page+1 if page+1 <= n else 1}` to view the next page.\nUse `{p}inventory upgrade` to increase your max inventory space from `{items['item_space']['max']}` to `{(items['item_space']['max']*2)-items['item_space']['max']//2}` for {self.cash((items['item_space']['max'] ** 3) // (items['item_space']['max'] // 6))}\n",
                    )

                    embed.set_footer(text=f"Page ({page}/{n})")
                    done = True

            if not done:
                embed = discord.Embed(
                    title=f"{ctx.author}'s Inventory",
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
            desc = "\n".join([f"{self.Hamood.market.all_items[name]['info']}"])
            embed = discord.Embed(
                title=f"{self.to_name(name)} | ***{self.Hamood.market.all_items[name]['rarity'].upper()}*** {' | `In Shop`' if name in self.Hamood.market.shop else ''}",
                description=f"{desc}",
                color=self.colors[self.Hamood.market.all_items[name]["rarity"]],
                timestamp=ctx.message.created_at,
            )
            p = self.Hamood.find_prefix(ctx.guild.id)
            buy = f"Use `{p}buy {name} 1` to purchase."

            embed.add_field(
                name=f"<:blank:794679084890193930>",
                value=f"**Current Price**: {self.cash(self.Hamood.market.all_items[name]['price'])} {self.get_arrow(name)}{self.get_percent(name)}\n**Regular Price**: {self.cash(self.Hamood.market.all_items[name]['value'])}\n \nitem_id: `{name}`\n{buy if name in self.Hamood.market.shop else ''}type: `{self.Hamood.market.all_items[name]['type']}`",
            )
            embed.set_thumbnail(url=self.Hamood.market.all_items[name]["image"])

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
        p = self.Hamood.find_prefix(ctx.guild.id)
        embed = discord.Embed(
            title=f"All Items | Sorted by {sort_by.capitalize()} ({page}/{n})",
            description=f"{items}\n<:blank:794679084890193930>\nUse `{p}itemlist{f' {sort_by} ' if sort_by != 'price' else ' '}{page+1 if page+1 <= n else 1}` to view the next page.\nUse `{p}iteminfo [item name]` to find out more about an item.",
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
        if item_id in self.Hamood.market.crates:
            inv = await self.Hamood.Inventories.get_items(ctx.guild.id, ctx.author.id)

            if inv is not None and item_id in inv:
                if await self.Hamood.Inventories.member_has_space(
                    ctx.guild.id,
                    ctx.author.id,
                    self.Hamood.market.crates[item_id]["contains"],
                ):
                    reward = {}
                    for i in range(self.Hamood.market.crates[item_id]["contains"]):
                        ran = random.randint(1, 100)
                        if item_id == "blackmarket_crate":
                            if ran <= 80:
                                choice = self.Hamood.market.rare_items
                            elif ran <= 93:
                                choice = self.Hamood.market.epic_items
                            elif ran <= 98:
                                choice = self.Hamood.market.legendary_items
                            else:
                                choice = self.Hamood.market.blackmarket_items

                        elif item_id == "rare_crate":
                            if ran <= 20:
                                choice = self.Hamood.market.common_items
                            elif ran <= 50:
                                choice = self.Hamood.market.uncommon_items
                            else:
                                choice = self.Hamood.market.rare_items

                        k, v = random.choice(list(choice.items()))

                        reward[k] = 1 if k not in reward else reward[k] + 1

                    for item in reward:
                        await self.Hamood.Inventories.incr_item_amount(
                            ctx.guild.id, ctx.author.id, item, reward[item]
                        )

                    await self.Hamood.Inventories.decr_item_amount(
                        ctx.guild.id, ctx.author.id, item_id, 1
                    )

                    item_desc = (
                        lambda i: f"{self.Hamood.market.all_items[i]['emoji']} - **{self.to_name(i)}** `x{reward[i]}` **|** {self.cash(self.Hamood.market.all_items[i]['price']*int(reward[i]))}"
                    )

                    desc = "\n".join([item_desc(i) for i in reward])

                    embed = discord.Embed(
                        title=f"Opened {self.to_name(item_id)}",
                        description=f"{ctx.author.mention} opened a `{item_id}` and recieved\n<:blank:794679084890193930>\n{desc}",
                        color=ctx.author.color,
                        timestamp=ctx.message.created_at,
                    )
                    embed.set_thumbnail(url=self.Hamood.market.crates[item_id]["image"])

                    await ctx.send(embed=embed)

                else:
                    await ctx.send("`Insufficient Space!`")
            else:
                await ctx.send("`You dont have that item!`")
        else:
            await ctx.send(
                f"`Invalid Item` Use `{self.Hamood.find_prefix(ctx.guild.id)}iteminfo [item name]` to find its `item_id`"
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
            if self.to_id(item_id) in self.Hamood.market.shop:
                if await self.Hamood.Inventories.member_has_space(
                    ctx.guild.id, ctx.author.id, amount
                ):
                    bal = await self.Hamood.Currency.get_currency(
                        ctx.guild.id, ctx.author.id
                    )
                    if bal is not None:
                        item_id = self.to_id(item_id)
                        item = self.Hamood.market.all_items[item_id]

                        cost = item["price"] * amount

                        if bal["bank"] >= cost:
                            await self.Hamood.Currency.update_bank(
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
                                url=self.Hamood.market.all_items[item_id]["image"]
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
                f"`Invalid Item` Use `{self.Hamood.find_prefix(ctx.guild.id)}iteminfo [item name]` to find its `item_id`"
            )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sell(self, ctx, item_id, amount=1):
        """``sell [item_id] [amount]`` sell your items for cash."""
        if isinstance(amount, str) and amount.lower() == "all":
            amount = abs(int(amount))
            if amount == 0:
                amount = 1
        if self.valid_item(item_id):
            item_id = self.to_id(item_id)
            item = self.Hamood.market.all_items[item_id]
            if item["type"] != "sellable":
                return await ctx.send("`That Item cannot be sold`")
            items = await self.Hamood.Inventories.get_items(ctx.guild.id, ctx.author.id)
            if items is not None and item_id in items:
                if isinstance(amount, str) and amount.lower() == "all":
                    amount = items[item_id]
                if items[item_id] >= amount:
                    value = item["price"] * amount
                    # await self.Hamood.Currency.add_server(ctx.guild.id)
                    await self.Hamood.Currency.add_member(ctx.guild.id, ctx.author.id)
                    await self.Hamood.Currency.update_wallet(
                        ctx.guild.id, ctx.author.id, value
                    )
                    await self.Hamood.Inventories.decr_item_amount(
                        ctx.guild.id, ctx.author.id, item_id, amount
                    )

                    embed = discord.Embed(
                        title=f"Sold {self.to_name(item_id)} `x{amount}`",
                        description=f"{ctx.author.mention} successfully sold `{item_id}` `x{amount}` for {self.cash(value)}",
                        color=ctx.author.color,
                        timestamp=ctx.message.created_at,
                    )
                    embed.set_thumbnail(
                        url=self.Hamood.market.all_items[item_id]["image"]
                    )

                    return await ctx.send(embed=embed)

            await ctx.send("`Insufficient Items!`")
        else:
            await ctx.send(
                f"`Invalid Item` Use `{self.Hamood.find_prefix(ctx.guild.id)}iteminfo [item name]` to find its `item_id`"
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
            item = self.Hamood.market.all_items[item_id]
            items = await self.Hamood.Inventories.get_items(ctx.guild.id, ctx.author.id)
            if items is not None and item_id in items:
                if isinstance(amount, str) and amount.lower() == "all":
                    amount = item[item_id]
                if items[item_id] >= amount:
                    # await self.Hamood.Currency.add_server(ctx.guild.id)
                    await self.Hamood.Currency.add_member(ctx.guild.id, ctx.author.id)
                    await self.Hamood.Inventories.decr_item_amount(
                        ctx.guild.id, ctx.author.id, item_id, amount
                    )
                    embed = discord.Embed(
                        title=f"Trashed {self.to_name(item_id)} `x{amount}`",
                        description=f"{ctx.author.mention} successfully trashed `{item_id}` `x{amount}`",
                        color=ctx.author.color,
                        timestamp=ctx.message.created_at,
                    )
                    embed.set_thumbnail(
                        url=self.Hamood.market.all_items[item_id]["image"]
                    )

                    return await ctx.send(embed=embed)

            await ctx.send("`Insufficient Items!`")
        else:
            await ctx.send(
                f"`Invalid Item` Use `{self.Hamood.find_prefix(ctx.guild.id)}iteminfo [item name]` to find its `item_id`"
            )

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def gift(
        self, ctx, recipient: discord.Member = None, item_id="1234", amount=1
    ):
        """``gift [@member] [item_id] [amount]`` Gift items to other members. 5 items max."""
        if recipient is not None and recipient.id != ctx.author.id:
            if self.valid_item(item_id):
                amount = abs(int(amount))
                if amount > 5:
                    amount = 5
                sender = ctx.author
                sender_items = await self.Hamood.Inventories.get_items(
                    ctx.guild.id, sender.id
                )

                if sender_items is not None and item_id in sender_items:
                    if sender_items[item_id] >= amount:
                        await self.Hamood.Inventories.add_member(
                            ctx.guild.id, recipient.id
                        )
                        if await self.Hamood.Inventories.member_has_space(
                            ctx.guild.id, recipient.id, amount
                        ):
                            await self.Hamood.Inventories.decr_item_amount(
                                ctx.guild.id, sender.id, item_id, amount
                            )
                            await self.Hamood.Inventories.incr_item_amount(
                                ctx.guild.id, recipient.id, item_id, amount
                            )

                            embed = discord.Embed(
                                title=f"`{sender}` gifted `{recipient}` **{self.to_name(item_id)}**",
                                description=f"{sender.mention} successfully gifted {recipient.mention} `{self.to_id(item_id)}` `x{amount}`",
                                color=ctx.author.color,
                                timestamp=ctx.message.created_at,
                            )
                            embed.set_thumbnail(
                                url=self.Hamood.market.all_items[item_id]["image"]
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
        ctx.command.reset_cooldown(ctx)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def shop(self, ctx, page=1):
        """``shop [page]`` view the current items you can buy."""
        items, n = await self.sort_items("shop", "shop", page)
        p = self.Hamood.find_prefix(ctx.guild.id)
        embed = discord.Embed(
            title=f"Item Shop ({page}/{n})",
            description=f"<:blank:794679084890193930>\n{items}\n<:blank:794679084890193930>\nUse `{p}buy [item_id] [amount]` to buy an item.\nUse `{p}shop {page+1 if page+1 <= n else 1}` to view the next page.\nUse `{p}iteminfo [item name]` to find out more about an item.",
            color=ctx.author.color,
        )

        time_left = (
            3600 - (datetime.now() - self.Hamood.market.last_refresh).total_seconds()
        )
        embed.set_footer(
            text=f"Page ({page}/{n}). Prices refresh in {self.Hamood.pretty_time_delta(time_left)}"
        )
        await ctx.send(embed=embed)

    async def sort_items(self, og="itemlist", sort_by="price", page=1, inv=None):
        n = 12
        if sort_by == "price":
            temp = sorted(
                [
                    [self.Hamood.market.all_items[i]["price"], i]
                    for i in self.Hamood.market.all_items
                ]
            )

            temp = {i[1]: self.Hamood.market.all_items[i[1]] for i in temp}
        elif sort_by == "shop":
            n = 10
            temp = self.Hamood.market.shop
        elif sort_by == "rarity":
            temp = self.rare_ranking
        elif sort_by == "common":
            temp = self.Hamood.market.common_items
        elif sort_by == "uncommon":
            temp = self.Hamood.market.uncommon_items
        elif sort_by == "rare":
            temp = self.Hamood.market.rare_items
        elif sort_by == "epic":
            temp = self.Hamood.market.epic_items
        elif sort_by == "legendary":
            temp = self.Hamood.market.legendary_items
        elif sort_by == "blackmarket":
            temp = self.Hamood.market.blackmarket_items
        elif sort_by == "dev":
            temp = self.Hamood.market.dev_items
        elif sort_by == "crates":
            temp = self.Hamood.market.crates

        if og == "itemlist":
            item_desc = (
                lambda items, i: [
                    f"{items[i]['emoji']} - **{self.to_name(i)}** **|** {self.cash(items[i]['price'])} {self.get_arrow(i)} {'`In Shop`' if i in self.Hamood.market.shop else ''}"
                ]
                if items[i]["type"] != "crate" or sort_by == "crates"
                else []
            )
        elif og == "inventory":
            item_desc = (
                lambda items, i: [
                    f"{items[i]['emoji']} - **{self.to_name(i)}** `x{inv[i]}` **|** {self.cash(self.Hamood.market.all_items[i]['price']*int(inv[i]))} {self.get_arrow(i)}{self.get_percent(i)}"
                ]
                if i in inv
                else []
            )
        elif og == "shop":
            item_desc = lambda items, i: [
                f"{items[i]['emoji']} - **{self.to_name(i)}** **|** {self.cash(items[i]['price'])} {self.get_arrow(i)}{self.get_percent(i)}\n    **↳** `{self.to_id(i)}` ***{items[i]['rarity']}***\n"
            ]

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
