import os
import pymongo
import logging
import collections
import motor.motor_asyncio

try:
    MONGOURI = os.environ["MONGOURI"]
except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    MONGOURI = os.environ.get("MONGOURI")


class Documents:
    def __init__(self, connection, document_name):
        connection = motor.motor_asyncio.AsyncIOMotorClient(str(MONGOURI))
        self.db = connection[document_name]

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


class Leaderboards(Documents):
    def __init__(self):
        """
        Connects to the leaderboards document in the games database
        """
        self.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(MONGOURI))
        self.db = self.mongo["games"]["leaderboards"]

        print("Initialized Leaderboards Database")

    # -- Pointer Methods --
    async def add_leaderboard(self, guild_id):
        """
        Points to self.add_leaderboard_to_games
        """
        await self.add_leaderboard_to_games(guild_id)

    async def add_member(self, guild_id, member_id):
        """
        Points to self.add_member_to_leaderboards
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
    async def delete_member(self, guild_id, member_id):
        """
        Deletes a member from a guild leaderboard
        """
        if await self.member_exists(guild_id, str(member_id)):
            await self.db.update_one(
                {"_id": guild_id}, {"$unset": {str(member_id): ""}}
            )

    async def member_exists(self, guild_id, member_id):
        """
        Checks if a member exists with the given member_id nad guild_id
        Returns a boolean value on the existence of the member
        """
        leaderboard = await self.find_by_id(guild_id)
        if leaderboard is not None:
            if str(member_id) in leaderboard:
                return True

        return False

    async def add_leaderboard_to_games(self, guild_id):
        """
        Adds a server leaderboard to the leaderboards document
        """
        leaderboard = {"_id": guild_id}
        try:
            await self.db.insert_one(leaderboard)
        except pymongo.errors.DuplicateKeyError:
            return

    async def add_member_to_leaderboard(self, guild_id, member_id, check_error=False):
        """
        Adds a member object to a server leaderboard 
        """
        if await self.member_exists(guild_id, str(member_id)):
            return

        member = {str(member_id): {"total": {"won": 0, "lost": 0}}}
        await self.db.update_one({"_id": guild_id}, {"$set": member})

    async def add_game_to_member(self, guild_id, member_id, game):
        """
        Adds a game object to a member object in a server leaderboard 
        """
        leaderboard = await self.find_by_id(guild_id)

        if leaderboard is not None:
            try:
                if game not in leaderboard[str(member_id)]:
                    leaderboard[str(member_id)][game] = {
                        "won": 0,
                        "lost": 0,
                    }
                    await self.db.update_one(
                        {"_id": guild_id},
                        {"$set": {f"{member_id}": leaderboard[str(member_id)]}},
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
            leaderboard = await self.find_by_id(guild_id)

            if leaderboard is not None:
                try:
                    if game not in leaderboard[str(member_id)]:
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
        leaderboard = await self.find_by_id(guild_id)

        if leaderboard is not None:
            try:
                stats = leaderboard[str(member_id)][game]
            except KeyError:
                return

            return stats


# class Inventory(Documents):
#     def __init__(self):
#         """
#         Connects to the inventory
#         """
