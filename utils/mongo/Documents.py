import os
import datetime
import pymongo


class Documents:
    def __init__(self, collection_name, document_name, MONGO):
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
