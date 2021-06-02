import os
import datetime
import pymongo

from utils.mongo.Documents import Documents


class Currency(Documents):
    def __init__(self, MONGO):
        """
        Connects to the inventories document in the games database
        """
        super().__init__("games", "currency", MONGO)
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
