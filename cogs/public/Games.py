import os
import discord
from discord.ext import commands

from games.Chess import Chess
from games.Trivia import Trivia
from games.Filler import Filler
from games.ConnectFour import ConnectFour
from utils.Premium import PremiumCooldown


class Games(commands.Cog):
    """Fun Games you can play with your friends"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.game_names = ("total", "filler", "connect4", "chess", "trivia")
        self.leaderboard_emojis = (
            ":first_place:",
            ":second_place:",
            ":third_place:",
            ":medal:",
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            _id = str(payload.guild_id) + str(payload.user_id)
            if _id in self.Hamood.active_games:
                await self.Hamood.active_games[_id].on_reaction(payload)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(2, 30, "user"), reg=(4, 60, "channel")))
    async def connect4(self, ctx, member: discord.Member = None, wager: int = 0):
        """<@opponent> [wager]|||Starts a game of connect4."""
        wager = int(wager)
        game = ConnectFour(playerTwo=member, ctx=ctx, wager=wager)
        await game.setup_game()

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 30, "user"), reg=(4, 60, "channel")))
    @commands.bot_has_permissions(embed_links=True)
    async def filler(self, ctx, member: discord.Member = None, wager: int = 0):
        """<@opponent> [wager]|||Starts a game of filler."""
        wager = int(wager)
        game = Filler(playerTwo=member, ctx=ctx, wager=wager)
        await game.setup_game()

    @commands.command()
    @commands.check(PremiumCooldown(prem=(1, 30, "user"), reg=(2, 60, "channel")))
    @commands.bot_has_permissions(embed_links=True)
    async def trivia(
        self,
        ctx,
        member: discord.Member = None,
        category="any",
        wager: int = 0,
    ):
        """<@opponent> [category] [wager]|||Play a game of trivia with someone!\n \n**Categories include:** `any`, `general`, `books`, `film`, `music`, `musicals`, `theatres`, `tv`, `video games`, `board games`, `nature`, `computers`, `mathematics`, `mythology`, `sports`, `geography`, `history`, `politics`, `art`, `celebrities`, `animals`, `vehicles`, `comics`, `gadgets`, `anime`, `manga`, `cartoon`, `animation`"""
        game = Trivia(
            playerTwo=member,
            ctx=ctx,
            category=category,
            wager=wager,
        )
        await game.setup_game()

    @commands.command()
    @commands.check(PremiumCooldown(prem=(2, 30, "user"), reg=(4, 60, "channel")))
    @commands.bot_has_permissions(embed_links=True)
    async def chess(self, ctx, member: discord.Member = None, wager=0):
        """<@opponent> [wager]|||Starts a game of Chess. Use .move to play."""
        wager = int(wager)
        game = Chess(playerTwo=member, ctx=ctx, wager=wager)
        await game.setup_game()

    @commands.command()
    @commands.cooldown(4, 10, commands.BucketType.user)
    @commands.bot_has_permissions(embed_links=True)
    async def move(self, ctx, *, content: commands.clean_content = None):
        """<coord> <coord>|||Used to move your chess peices, ex. 'e2 e4'. Can only be used if you are in a chess match!."""
        _id = str(ctx.guild.id) + str(ctx.author.id)
        if _id not in self.Hamood.active_games:
            return await ctx.send("`You are not currently in a game!`")

        msg = await self.Hamood.active_games[_id].game_update(
            member=ctx.author, move=content.lower().replace(" ", "").replace(",", "")
        )
        if msg is not None:
            await ctx.send(f"`{msg}`")

    @commands.command()
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def leavegame(self, ctx):
        """|||Leaves any game you are currently in."""
        _id = str(ctx.guild.id) + str(ctx.author.id)
        if _id not in self.Hamood.active_games:
            return await ctx.send("`You are not currently in a game!`")

        await self.Hamood.active_games[_id].delete_game(member=ctx.author)
        await ctx.send(f"{ctx.author.mention}, you have left your game!")

    async def grabLeaderboard(self, ctx):
        leaderboard = await self.Hamood.Leaderboards.get(ctx.guild.id)
        if leaderboard is None:
            await self.Hamood.quick_embed(
                ctx, title="No games have been played on this server :("
            )
            return
        else:
            return leaderboard

    async def grabMemberStat(self, ctx, member, game):
        leaderboard = await self.grabLeaderboard(ctx)
        if leaderboard:
            if str(member.id) not in leaderboard:
                await self.Hamood.quick_embed(
                    ctx, title=f"{member} has not played any games on this server."
                )
                return
            else:
                if game not in leaderboard[str(member.id)]:
                    await ctx.send(f"{member} has no stats for that game")
                    return
                else:
                    return leaderboard[str(member.id)][game]

        return

    async def verify_game_name(self, ctx, game):
        if game in self.game_names:
            return True
        else:
            await self.Hamood.quick_embed(
                ctx,
                title="Invalid Game",
                description="Try: "
                + ", ".join(f"`{game}`" for game in self.game_names),
            )
            return False

    async def verify_stat_name(self, ctx, stat):
        valid = ("won", "lost", "skill")
        if stat in valid:
            return True
        else:
            await self.Hamood.quick_embed(
                ctx,
                title="Invalid Stat",
                description="Try: " + ", ".join(f"`{s}`" for s in valid),
            )
            return False

    def calc_sr(self, stats):
        return round(
            (
                stats["won"]
                / (stats["lost"] if stats["lost"] != 0 else stats["lost"] + 1)
            )
            * (500 * (1 - 1 / (stats["won"] + (stats["lost"]))))
        )

    def get_stat(self, stats, stat):
        if stat == "skill":
            return self.calc_sr(stats)

        return stats[stat]

    @commands.command(aliases=["stat"])
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(4, 5, "user"), reg=(4, 10, "channel")))
    async def stats(self, ctx, member: discord.Member = None, game="total"):
        """[@member] [game]|||See your game stats!"""
        member = ctx.author if member is None else member
        game = game.lower()

        gn = await self.verify_game_name(ctx, game)
        if gn:
            stat = await self.grabMemberStat(ctx, member, game)
            await self.Hamood.quick_embed(
                ctx,
                author={"name": f"{member}'s {game.capitalize()} Stats"},
                description=f"**Wins:** {stat['won']}\n**Losses:** {stat['lost']}\n**SR:** {self.calc_sr(stat)}",
                timestamp=ctx.message.created_at,
                thumbnail=member.avatar.url,
            )

    @commands.command(aliases=["leaderboards"])
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(3, 10, commands.BucketType.channel)
    async def leaderboard(self, ctx, game="total", stat="won"):
        """[game] [stat]|||View the server games leaderboard."""
        game, stat = game.lower(), stat.lower()

        gn = await self.verify_game_name(ctx, game)
        if not gn:
            return

        sn = await self.verify_stat_name(ctx, stat)
        if not sn:
            return

        leaderboard = await self.grabLeaderboard(ctx)
        if not leaderboard:
            return

        del leaderboard["_id"]

        server_leaderboard = {}
        for m_id, stats in leaderboard.items():
            try:
                server_leaderboard[
                    str(self.bot.get_user(int(m_id)).mention)
                ] = self.get_stat(stats[game], stat)
            except Exception as e:
                print(e)
                pass

        order = sorted(
            server_leaderboard.keys(), key=lambda m_id: server_leaderboard[m_id]
        )[:25]

        if len(order) == 0:
            await self.Hamood.quick_embed(
                ctx, title=f"Not enough games have been played :("
            )
            return

        if stat != "lost":
            order = order[::-1]

        desc = "\n".join(
            f"{self.leaderboard_emojis[min(i, 3)]} **{server_leaderboard[order[i]]}{' SR' if stat=='skill' else ''}** • {order[i]}"
            for i in range(len(order))
        )

        await self.Hamood.quick_embed(
            ctx,
            title=f"Top {len(order)} in {ctx.guild.name}",
            url=f"{self.Hamood.URL}/games/{ctx.guild.id}?game={game}&sort={stat}",
            description=desc,
            footer={
                "text": f"Ranking by: {stat.capitalize()}\nGame: {game.capitalize()}"
            },
        )


def setup(bot):
    bot.add_cog(Games(bot))
