import os
import datetime
import pymongo

from utils.mongo.Documents import Documents


class Leaderboards(Documents):
    def __init__(self, MONGO):
        """
        Connects to the leaderboards document in the games database
        """
        super().__init__("games", "leaderboards", MONGO)
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
