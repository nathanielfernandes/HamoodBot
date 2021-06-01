import os
import datetime
import pymongo
import motor.motor_asyncio

try:
    MONGOURI = os.environ["MONGOURI"]
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    MONGOURI = os.environ.get("MONGOURI")


MONGO = motor.motor_asyncio.AsyncIOMotorClient(str(MONGOURI))


class Documents:
    def __init__(self, collection_name, document_name):
        self.collection = MONGO[collection_name]
        self.db = self.collection[document_name]

    # -- Pointer Methods --
    async def get(self, guild_id):
        """
        Points to self.find_by_id
        """
        return await self.db.find_one({"_id": guild_id})

    # -- Actual Methods --
    async def find_by_id(self, guild_id):
        """
        Returns the document with the givin guild_id
        """
        return await self.db.find_one({"_id": guild_id})

    async def exists(self, guild_id):
        """
        Checks if a document exists with the given guild_id
        Returns a boolean value on the existence of the document
        """
        item = await self.find_by_id(guild_id)
        return True if item is not None else False

    async def delete_by_id(self, guild_id):
        """
        Deletes all items found with the given guild_id
        """
        if not await self.find_by_id(guild_id):
            return

        await self.db.delete_one({"_id": guild_id})

    async def upsert_server(self, guild_id):
        """
        Adds a server to a database document
        """
        try:
            await self.db.insert_one({"_id": guild_id})
        except pymongo.errors.DuplicateKeyError:
            return

    async def delete_member(self, guild_id, member_id):
        """
        Deletes a member from a server item
        """
        if await self.member_exists(guild_id, str(member_id)):
            await self.db.update_one(
                {"_id": guild_id}, {"$unset": {str(member_id): ""}}
            )

    async def upsert_member(self, guild_id, member_id, member_object):
        """
        Adds a member object to a server item
        """
        if await self.member_exists(guild_id, str(member_id)):
            return

        await self.db.update_one({"_id": guild_id}, {"$set": member_object})

    async def member_exists(self, guild_id, member_id):
        """
        Checks if a member exists with the given member_id and guild_id
        Returns a boolean value on the existence of the member
        """
        item = await self.find_by_id(guild_id)
        if item is not None:
            if str(member_id) in item:
                return True

        return False


class Prefixes(Documents):
    def __init__(self):
        super().__init__("games", "prefixes")
        print("Initialized Prefixes Database")

    async def add_server(self, guild_id, prefix):
        try:
            await self.db.insert_one({"_id": guild_id, "prefix": prefix})
        except pymongo.errors.DuplicateKeyError:
            return

    async def change_prefix(self, guild_id, new_prefix):
        server = await self.find_by_id(guild_id)
        if server is None:
            if new_prefix != ".":
                await self.add_server(guild_id, new_prefix)
        else:
            if new_prefix != ".":
                await self.db.update_one(
                    {"_id": guild_id}, {"$set": {"prefix": new_prefix}},
                )
            else:
                await self.delete_by_id(guild_id)


class Leaderboards(Documents):
    def __init__(self):
        """
        Connects to the leaderboards document in the games database
        """
        super().__init__("games", "leaderboards")
        print("Initialized Leaderboards Database")

    # -- Pointer Methods --
    async def add_leaderboard(self, guild_id):
        """
        Points to self.upsert_server
        """
        await self.upsert_server(guild_id)

    async def add_member(self, guild_id, member_id):
        """
        Points to self.add_member_to_leaderboard
        """
        await self.add_member_to_leaderboard(guild_id, member_id)

    async def add_game(self, guild_id, member_id, game):
        """
        Points to self.add_game_to_member
        """
        await self.add_game_to_member(guild_id, member_id, game)

    async def incr_game_won(self, guild_id, member_id, game):
        """
        Points to self.incr_game_stats
        Increments a game's won value by 1
        """
        await self.incr_game_stats(guild_id, member_id, game, "won")

    async def incr_game_lost(self, guild_id, member_id, game):
        """
        Points to self.incr_game_stats
        Increments a game's lost value by 1
        """
        await self.incr_game_stats(guild_id, member_id, game, "lost")

    # -- Actual Methods --

    async def add_member_to_leaderboard(self, guild_id, member_id):
        """
        Adds a member object to a server leaderboard 
        """
        member = {str(member_id): {"total": {"won": 0, "lost": 0}}}
        await self.upsert_member(guild_id, member_id, member)

    async def add_game_to_member(self, guild_id, member_id, game):
        """
        Adds a game object to a member object in a server leaderboard 
        """
        server = await self.find_by_id(guild_id)

        if server is not None:
            try:
                if game not in server[str(member_id)]:
                    server[str(member_id)][game] = {
                        "won": 0,
                        "lost": 0,
                    }
                    await self.db.update_one(
                        {"_id": guild_id},
                        {"$set": {f"{member_id}": server[str(member_id)]}},
                    )
            except KeyError:
                return

    async def incr_game_stats(
        self, guild_id, member_id, game, stat, incr_total=True, check_error=False
    ):
        """
        Increments the won or lost value of a member's game
        """
        if check_error:
            server = await self.find_by_id(guild_id)

            if server is not None:
                try:
                    if game not in server[str(member_id)]:
                        return
                except KeyError:
                    return

        if incr_total:
            await self.db.update_one(
                {"_id": guild_id}, {"$inc": {f"{member_id}.total.{stat}": 1}}
            )
        await self.db.update_one(
            {"_id": guild_id}, {"$inc": {f"{member_id}.{game}.{stat}": 1}}
        )

    async def get_game_stats(self, guild_id, member_id, game):
        """
        Returns the stats of a member's game
        """
        server = await self.find_by_id(guild_id)

        if server is not None:
            try:
                stats = server[str(member_id)][game]
            except KeyError:
                return

            return stats

    async def find_all_of_member(self, member_id):
        cursor = self.db.find({str(member_id): {"$exists": True}})
        won = 0
        lost = 0
        for document in await cursor.to_list(length=100):
            won += document[str(member_id)]["total"]["won"]
            lost += document[str(member_id)]["total"]["won"]

        return won, lost


class Inventories(Documents):
    def __init__(self):
        """
        Connects to the inventories document in the games database
        """
        super().__init__("games", "inventories")
        print("Initialized Inventories Database")

    # -- Pointer Methods --
    async def add_inventory(self, guild_id):
        """
        Points to self.upsert_server
        """
        await self.upsert_server(guild_id)

    async def add_member(self, guild_id, member_id):
        """
        Points to self.add_member_to_inventory
        """
        await self.add_member_to_inventory(guild_id, member_id)

    async def add_item(self, guild_id, member_id, item_id, amount):
        """
        Points to self.add_item_to_member
        """
        await self.add_item_to_member(guild_id, member_id, item_id, amount)

    async def get_items(self, guild_id, member_id):
        """
        Points to self.get_member_items
        """
        return await self.get_member_items(guild_id, member_id)

    async def get_space(self, guild_id, member_id):
        """
        Points to self.get_member_space
        """
        return await self.get_member_space(guild_id, member_id)

    # -- Actual Methods --
    async def member_has_space(self, guild_id, member_id, amount=1):
        """
        Returns a boolean value on whether a member has the space for an item
        """
        space = await self.get_member_space(guild_id, member_id)

        if space is not None:
            if space["max"] - space["total"] >= amount:
                return True
        else:
            if amount <= 10:
                return True

        return False

    async def get_member_space(self, guild_id, member_id):
        """
        Returns a member's item_space
        """
        server = await self.find_by_id(guild_id)

        if server is not None:
            try:
                items = server[str(member_id)]["item_space"]
            except KeyError:
                return

            return items

    async def add_member_to_inventory(self, guild_id, member_id):
        """
        Adds a member object to a server inventory document
        """
        member = {str(member_id): {"item_space": {"total": 0, "max": 10}}}
        await self.upsert_server(guild_id)
        await self.upsert_member(guild_id, member_id, member)

    async def add_item_to_member(self, guild_id, member_id, item_id, amount=1):
        """
        Adds an item to a members items
        """
        server = await self.find_by_id(guild_id)

        if server is not None:
            try:
                if str(item_id) not in server[str(member_id)]:
                    server[str(member_id)][str(item_id)] = amount

                    await self.db.update_one(
                        {"_id": guild_id},
                        {"$set": {f"{member_id}": server[str(member_id)]}},
                    )
                    await self.incr_item_total(guild_id, member_id, amount)
                else:
                    await self.incr_item_amount(guild_id, member_id, item_id, amount)
            except KeyError:
                return

    async def incr_item_total(self, guild_id, member_id, amount):
        """
        Increments the total number of items a member has
        """
        await self.db.update_one(
            {"_id": guild_id}, {"$inc": {f"{member_id}.item_space.total": amount}}
        )

    async def incr_item_max(self, guild_id, member_id, amount=10):
        """
        Increments the total number of items a member has
        """
        await self.db.update_one(
            {"_id": guild_id}, {"$inc": {f"{member_id}.item_space.max": amount}}
        )

    async def incr_item_amount(self, guild_id, member_id, item_id, amount=1):
        """
        Increments an item's amount in a member's inventory
        """
        await self.db.update_many(
            {"_id": guild_id}, {"$inc": {f"{member_id}.{item_id}": amount}}
        )
        await self.incr_item_total(guild_id, member_id, amount)

    async def incr_all_invs(self, member_id, item_id, amount=1):
        """
        Updates the wallet amount of a member_id
        """
        await self.db.update_many(
            {str(member_id): {"$exists": True}},
            {"$inc": {f"{member_id}.{item_id}": amount}},
        )
        await self.db.update_many(
            {str(member_id): {"$exists": True}},
            {"$inc": {f"{member_id}.item_space.total": amount}},
        )

    async def decr_item_amount(self, guild_id, member_id, item_id, amount=-1):
        """
        Decrements an item's amount in a member's inventory
        """
        amount = abs(amount) * -1

        await self.db.update_one(
            {"_id": guild_id}, {"$inc": {f"{member_id}.{item_id}": amount}}
        )

        server = await self.find_by_id(guild_id)
        if server[str(member_id)][str(item_id)] <= 0:
            del server[str(member_id)][str(item_id)]

            await self.db.update_one(
                {"_id": guild_id}, {"$set": {f"{member_id}": server[str(member_id)]}},
            )

        await self.incr_item_total(guild_id, member_id, amount)

    async def get_member_items(self, guild_id, member_id):
        """
        Returns the items a member has
        """
        server = await self.find_by_id(guild_id)

        if server is not None:
            try:
                items = server[str(member_id)]
            except KeyError:
                return

            return items

    async def find_all_of_member(self, member_id):
        cursor = self.db.find({str(member_id): {"$exists": True}})
        total = 0

        for document in await cursor.to_list(length=100):
            total += document[str(member_id)]["item_space"]["total"]

        return total


class Currency(Documents):
    def __init__(self):
        """
        Connects to the inventories document in the games database
        """
        super().__init__("games", "currency")
        print("Initialized Currency Database")

    # -- Pointer Methods --
    async def add_server(self, guild_id):
        """
        Points to self.upsert_server
        """
        await self.upsert_server(guild_id)

    async def add_member(self, guild_id, member_id):
        """
        Points to self.add_member_to_currencydat
        """
        await self.add_member_to_currencydat(guild_id, member_id)

    # -- Actual Methods --
    async def add_member_to_currencydat(self, guild_id, member_id):
        """
        Adds a member object to a server currency document
        """
        await self.upsert_server(guild_id)
        member = {str(member_id): {"wallet": 0, "bank": 0, "bank_max": 500}}
        await self.upsert_member(guild_id, member_id, member)

    async def update_wallet(self, guild_id, member_id, amount):
        """
        Updates the wallet amount of a member_id
        """
        await self.db.update_one(
            {"_id": guild_id}, {"$inc": {f"{member_id}.wallet": int(amount)}}
        )

    async def update_all_wallets(self, member_id, amount):
        """
        Updates the wallet amount of a member_id
        """
        await self.db.update_many(
            {str(member_id): {"$exists": True}},
            {"$inc": {f"{member_id}.wallet": int(amount)}},
        )

    async def update_bank(self, guild_id, member_id, amount):
        """
        Updates the bank amount of a member_id
        """
        await self.db.update_one(
            {"_id": guild_id}, {"$inc": {f"{member_id}.bank": int(amount)}}
        )

    async def update_bank_max(self, guild_id, member_id, amount):
        """
        Updates the bank_max amount of a member_id
        """
        await self.db.update_one(
            {"_id": guild_id}, {"$inc": {f"{member_id}.bank_max": int(amount)}}
        )

    async def wallet_to_bank(self, guild_id, member_id, amount=1):
        """
        Transfers an amount from a member's wallet to their bank
        """
        curr = await self.get_currency(guild_id, member_id)

        if curr is not None:
            wallet = curr["wallet"]
            bank = curr["bank"]
            bank_max = curr["bank_max"]

            if wallet != 0:
                if amount > wallet:
                    amount = wallet

                if wallet >= amount:
                    if bank_max - bank != 0:
                        if bank_max - bank >= amount:
                            await self.update_bank(guild_id, member_id, amount)
                            await self.update_wallet(
                                guild_id, member_id, int(-1 * amount)
                            )
                            return amount
                        else:
                            await self.update_bank(guild_id, member_id, bank_max - bank)
                            await self.update_wallet(
                                guild_id, member_id, int(-1 * (bank_max - bank))
                            )
                            return bank_max - bank
                    return "max"
            else:
                return "broke"
        else:
            return "broke"

    async def bank_to_wallet(self, guild_id, member_id, amount=1):
        """
        Transfers an amount from a member's bank to their wallet
        """
        curr = await self.get_currency(guild_id, member_id)

        if curr is not None:
            wallet = curr["wallet"]
            bank = curr["bank"]
            bank_max = curr["bank_max"]

            if bank != 0:
                if amount > bank:
                    amount = bank

                if bank >= amount:
                    await self.update_bank(guild_id, int(member_id, -1 * amount))
                    await self.update_wallet(guild_id, member_id, amount)
                    return amount
            else:
                return
        else:
            return

    async def get_currency(self, guild_id, member_id):
        """
        Returns the currency object for a member
        """
        server = await self.find_by_id(guild_id)

        if server is not None:
            try:
                item = server[str(member_id)]
            except KeyError:
                return

            return item

    async def find_all_of_member(self, member_id):
        cursor = self.db.find({str(member_id): {"$exists": True}})
        servers = []
        bal = {"wallet": 0, "bank": 0, "total": 0}

        for document in await cursor.to_list(length=100):
            servers.append(document["_id"])
            bal["wallet"] += document[str(member_id)]["wallet"]
            bal["bank"] += document[str(member_id)]["bank"]
            bal["total"] += 1
        return servers, bal


class Members(Documents):
    def __init__(self):
        """
        Connects to the members document in the games database
        """
        super().__init__("games", "members")
        print("Initialized Members Database")

    # -- Actual Methods --
    async def add_member(self, member_id):
        """
        Adds a member object to the members document
        """
        member = {"_id": member_id, "daily": datetime.datetime.now(), "streak": 0}
        try:
            await self.db.insert_one(member)
        except pymongo.errors.DuplicateKeyError:
            return

        return True

    async def is_daily_ready(self, member_id):
        member = await self.get(member_id)
        if member is not None:
            change = (datetime.datetime.now() - member["daily"]).total_seconds()

            if change > 86400:
                return True, "Ready Now", member["streak"]
            else:
                return False, 86400 - change, member["streak"]
        else:
            return True, "Ready Now", 0

    async def reset_daily(self, member_id):
        await self.db.update_one(
            {"_id": member_id}, {"$set": {"daily": datetime.datetime.now()}}
        )
        await self.db.update_one({"_id": member_id}, {"$inc": {"streak": 1}})

