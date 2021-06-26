import os
import datetime
import pymongo

from utils.mongo.Documents import Documents


class Members(Documents):
    def __init__(self, MONGO):
        """
        Connects to the members document in the games database
        """
        super().__init__("games", "members", MONGO)
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
