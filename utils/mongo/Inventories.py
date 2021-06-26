import os
import datetime
import pymongo

from utils.mongo.Documents import Documents


class Inventories(Documents):
    def __init__(self, MONGO):
        """
        Connects to the inventories document in the games database
        """
        super().__init__("games", "inventories", MONGO)
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
