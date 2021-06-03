import discord
from discord.ext import commands


class ErrorHandling(commands.Cog):
    """Handles Command Errors"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.ignored_errors = (commands.CommandNotFound,)

    async def error_embed(self, ctx, title, msg):
        embed = discord.Embed(
            title=f"`{ctx.command.name.title()}` | {title}",
            description=msg,  # f"**{ctx.command.name}** is used like this: ```ini\n{p}{s[start:end]}```",
            colour=discord.Color.red(),
        )
        embed.set_author(
            name="Command Failed",
            icon_url="https://cdn.discordapp.com/attachments/749779629643923548/773072024922095636/images.png",
        )
        embed.set_footer(text=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/749779300181606411/799902760837316628/tumblr_01a3fd42036dbeac4d74baff3a2497ff_ecd049b3_500.gif"
        )
        try:
            await ctx.send(embed=embed)
        except Exception:
            print("Could not send error!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "orignal", error)

        if isinstance(error, self.ignored_errors):
            return

        if isinstance(error, commands.CommandOnCooldown):
            await self.error_embed(
                ctx,
                "Command on Cooldown",
                f"Please retry after: ```{self.Hamood.pretty_time_delta(error.retry_after)}```",
            )

        elif isinstance(error, commands.CheckFailure):
            if isinstance(error, commands.MissingPermissions):
                perms = "\n".join(
                    f"• {str(p).replace('_', ' ').title()}" for p in error.missing_perms
                )
                await self.error_embed(
                    ctx,
                    "Lack of Permissions",
                    f"You are missing the following permissions:```{perms}```",
                )

            elif isinstance(error, commands.BotMissingPermissions):
                perms = "\n".join(
                    f"• {str(p).replace('_', ' ').title()}" for p in error.missing_perms
                )
                await self.error_embed(
                    ctx,
                    "I don't have the permission to do that",
                    f"I am missing the following permissions:```{perms}```",
                )

            else:
                await self.error_embed(
                    ctx, "Restricted", f"You do not have access to this command.",
                )

        elif isinstance(error, commands.UserInputError):
            if isinstance(error, commands.MemberNotFound):
                await self.error_embed(
                    ctx,
                    "Member Not Found",
                    f"I could not find the member: `{error.argument}`",
                )

            elif isinstance(error, commands.PartialEmojiConversionFailure):
                await self.error_embed(
                    ctx,
                    "Could Not Convert Emoji",
                    f"I could not convert the emoji: {error.argument}",
                )

            elif isinstance(error, commands.EmojiNotFound):
                await self.error_embed(
                    ctx,
                    "Emoji not Found",
                    f"I could not find the emoji: `{error.argument}`",
                )

            else:
                p = self.Hamood.find_prefix(ctx.guild.id)
                s = ctx.command.help
                start = s.find("``") + 2
                end = s.find("``", start)
                await self.error_embed(
                    ctx,
                    "Input Error",
                    f"The command should be used like this:```ini\n{p}{s[start:end]}```",
                )

        else:
            await self.error_embed(
                ctx,
                "Whoops!",
                f"Something went wrong with this command, try it again later.",
            )

            print(ctx.command.name)
            print(error)


def setup(bot):
    bot.add_cog(ErrorHandling(bot))

