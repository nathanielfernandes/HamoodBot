import os
import discord
from discord.ext import commands

from games.Chess import Chess
from games.Trivia import Trivia
from games.Filler import Filler
from games.ConnectFour import ConnectFour
import modules.checks as checks


class Games(commands.Cog):
    """Play Games!"""  # all games auto delete if theres no input for 2 minutes

    def __init__(self, bot):
        self.bot = bot
        self.game_names = ["total", "filler", "connect4", "chess", "trivia"]
        self.leaderboard_emojis = [
            ":first_place:",
            ":second_place:",
            ":third_place:",
            ":clap:",
            ":clap:",
            ":clap:",
            ":thumbsup:",
            ":thumbsup:",
            ":thumbsup:",
            ":poop:",
        ]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            _id = str(payload.guild_id) + str(payload.user_id)
            if _id in self.bot.games:
                await self.bot.games[_id].on_reaction(payload)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def connect4(self, ctx, member: discord.Member = None, wager=0):
        """``connect [@opponent] [wager:optional]`` starts a new connect 4 game"""
        wager = int(wager)
        game = ConnectFour(playerTwo=member, ctx=ctx, bot=self.bot, wager=wager)
        await game.setup_game()

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def filler(self, ctx, member: discord.Member = None, wager=0):
        """``filler [@opponent] [wager:optional]`` starts a new filler game"""
        wager = int(wager)
        game = Filler(playerTwo=member, ctx=ctx, bot=self.bot, wager=wager)
        await game.setup_game()

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def trivia(
        self, ctx, member: discord.Member = None, category="any", wager=0,
    ):
        """``trivia [@opponent] [category] [wager:optional]`` play a game of trivia with someone!\n \n**Categories include:** `any`, `general`, `books`, `film`, `music`, `musicals`, `theatres`, `tv`, `video games`, `board games`, `nature`, `computers`, `mathematics`, `mythology`, `sports`, `geography`, `history`, `politics`, `art`, `celebrities`, `animals`, `vehicles`, `comics`, `gadgets`, `anime`, `manga`, `cartoon`, `animation`"""
        wager = int(wager)
        game = Trivia(
            playerTwo=member, ctx=ctx, bot=self.bot, category=category, wager=wager,
        )
        await game.setup_game()

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 60, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def chess(self, ctx, member: discord.Member = None, wager=0):
        """``chess [@opponent] [wager:optional]`` starts a new chess game. Use .move to play `BETA`"""
        wager = int(wager)
        game = Chess(playerTwo=member, ctx=ctx, bot=self.bot, wager=wager)
        await game.setup_game()

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 10, commands.BucketType.channel)
    @commands.has_permissions(embed_links=True)
    async def move(self, ctx, *, content: commands.clean_content = None):
        """``move [coords of peice] [coords to move peice to]`` can only be used if you are in a chess match!. """
        _id = str(ctx.guild.id) + str(ctx.author.id)
        if _id not in self.bot.games:
            return await ctx.send("`You are not currently in a game!`")

        msg = await self.bot.games[_id].game_update(
            member=ctx.author, move=content.lower().replace(" ", "").replace(",", "")
        )
        if msg is not None:
            await ctx.send(f"`{msg}`")

        await ctx.message.delete()

    @commands.command()
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def leave(self, ctx):
        """``leave`` leaves any game you are currently in."""
        _id = str(ctx.guild.id) + str(ctx.author.id)
        if _id not in self.bot.games:
            return await ctx.send("`You are not currently in a game!`")

        await self.bot.games[_id].delete_game(member=ctx.author)
        await ctx.send(f"{ctx.author.mention}, you have left your game!")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 10, commands.BucketType.guild)
    async def stats(self, ctx, member: discord.Member = None, game="total"):
        """``stats [@player] [stat]`` see a players game stats"""
        member = ctx.author if member is None else member

        leaderboard = await self.bot.leaderboards.get(ctx.guild.id)
        if leaderboard is None:
            return await ctx.send("`No games have been played on this server`")

        if str(member.id) not in leaderboard:
            return await ctx.send(
                "`The member has not played any games on this server`"
            )

        if game in self.game_names:
            game = game
        elif game in ["connect", "connectfour"]:
            game = "connect4"
        elif game == "all":
            game = "total"
        else:
            return await ctx.send(
                "`Game Name` (`all`, `filler`, `chess`, `connect4`, `trivia`)"
            )

        if game not in leaderboard[str(member.id)]:
            return await ctx.send("`The member has no stats for that game`")

        stat = leaderboard[str(member.id)][game]

        embed = discord.Embed(
            title=f"{member}'s {game.capitalize()} Stats",
            description=f"**Wins:** {stat['won']}\n**Losses:** {stat['lost']}\n**SR:** {round((stat['won'] / (stat['lost'] if stat['lost'] != 0 else stat['lost'] + 1)) * (500 * (1-1/(stat['won']+(stat['lost'])))))}",
            timestamp=ctx.message.created_at,
            color=member.color,
        )

        embed.set_thumbnail(url=member.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["leaderboards"])
    @checks.isAllowedCommand()
    @commands.cooldown(3, 10, commands.BucketType.channel)
    async def leaderboard(self, ctx, game="total", stat="won"):
        """``leaderboard [game] [stat]`` a leaderboard of the servers players"""
        leaderboard = await self.bot.leaderboards.get(ctx.guild.id)

        if leaderboard is None:
            return await ctx.send("`No games have been played on this server`")

        game = game.lower()
        stat = stat.lower()

        if game in ["won", "wins", "win"]:
            stat = "won"
            game = "total"
        elif game in ["lose", "lost"]:
            game = "total"
            stat = "lost"
        elif game in ["skill", "rank"]:
            game = "total"
            stat = "skill"
        else:
            if game in self.game_names:
                game = game
            elif game in ["connect", "connectfour"]:
                game = "connect4"
            elif game == "all":
                game = "total"
            else:
                return await ctx.send(
                    "`Invalid Leaderboard Game Field` (`all`, `filler`, `chess`, `connect`, `trivia`)"
                )
            if stat in ["won", "wins", "win"]:
                stat = "won"
            elif stat in ["lose", "lost"]:
                stat = "lost"
            elif stat in ["skill", "rank"]:
                stat = "skill"
            else:
                return await ctx.send(
                    "`Invalid Leaderboard Stat Field` (`won`, `lost`, `skill`)"
                )

        server_leaderboard = []
        if stat != "skill":
            for member_id in leaderboard:
                try:
                    if member_id != "_id" and leaderboard[member_id][game][stat] != 0:
                        server_leaderboard.append(
                            [
                                leaderboard[member_id][game][stat],
                                str(self.bot.get_user(int(member_id))),
                            ]
                        )
                except KeyError:
                    pass
        else:
            for member_id in leaderboard:
                try:
                    if member_id != "_id" and leaderboard[member_id][game]["won"] != 0:
                        server_leaderboard.append(
                            [
                                round(
                                    (
                                        leaderboard[member_id][game]["won"]
                                        / (
                                            leaderboard[member_id][game]["lost"]
                                            if leaderboard[member_id][game]["lost"] != 0
                                            else leaderboard[member_id][game]["lost"]
                                            + 1
                                        )
                                    )
                                    * (
                                        500
                                        * (
                                            1
                                            - 1
                                            / (
                                                leaderboard[member_id][game]["won"]
                                                + leaderboard[member_id][game]["lost"]
                                            )
                                        )
                                    )
                                ),
                                str(self.bot.get_user(int(member_id))),
                            ]
                        )
                except KeyError:
                    pass

        players = len(server_leaderboard)
        if players > 10:
            players = 10
        elif players == 0:
            return await ctx.send("`not enough games have been played`")

        server_leaderboard = sorted(server_leaderboard)
        if stat == "lost":
            server_leaderboard = server_leaderboard[:players]
        else:
            server_leaderboard = server_leaderboard[::-1][:players]

        for i in range(len(server_leaderboard)):
            server_leaderboard[
                i
            ] = f"{self.leaderboard_emojis[i]} {server_leaderboard[i][0]}{' SR' if stat=='skill' else ''} - {server_leaderboard[i][1]}"

        desc = "\n".join(server_leaderboard)

        embed = discord.Embed(
            title=f"Top {players} in this server ranked by {stat} - {game.capitalize()} Games",
            description=f"{desc}",
            color=discord.Color.gold(),
            timestamp=ctx.message.created_at,
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Games(bot))
