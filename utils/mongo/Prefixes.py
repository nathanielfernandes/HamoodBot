import os
import datetime
import pymongo

from utils.mongo.Documents import Documents


class Prefixes(Documents):
    def __init__(self, MONGO):
        super().__init__("games", "prefixes", MONGO)
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
