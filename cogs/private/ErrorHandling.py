import discord, os
from discord.ext import commands

from utils.CONSTANTS import ANSI


class ErrorHandling(commands.Cog):
    """Handles Command Errors"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood
        self.ignored_errors = (commands.CommandNotFound,)
        self.bTypes = {
            commands.BucketType.user: "per `user`",
            commands.BucketType.channel: "in a `channel`",
            commands.BucketType.guild: "in a `server`",
            commands.BucketType.default: "`globaly`",
        }

    async def error_embed(self, ctx, title, msg, c=False):
        embed = discord.Embed(
            title=f"`{ctx.command.name.title()}` | {title}",
            description=msg,
            colour=discord.Color.red(),
        )
        # embed.set_author(name=f"{ctx.command.name.title()} | {title}")
        # embed.set_footer(
        #     text=f"{ctx.author}",
        #     icon_url=ctx.author.avatar.url,
        # )
        if c:
            embed.set_footer(text="supporters get reduced cooldowns ;)")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/749779300181606411/799902760837316628/tumblr_01a3fd42036dbeac4d74baff3a2497ff_ecd049b3_500.gif"
        )
        try:
            await ctx.reply(embed=embed, mention_author=False)
        except Exception:
            print("Could not send error!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "orignal", error)

        if isinstance(error, self.ignored_errors):
            return

        if isinstance(error, commands.CommandOnCooldown):
            # await self.Hamood.quick_embed(
            #     ctx,
            #     author={"name": "Command on Cooldown"},
            #     description=f"Please retry after: ```{self.Hamood.pretty_dt(error.retry_after)}```",
            #     # footer={"text": f"{ctx.author}", "icon_url": ctx.author.avatar.url},
            # )
            await self.error_embed(
                ctx,
                "Command on Cooldown",
                f"Limit: `{error.cooldown.rate} times` every `{self.Hamood.pretty_dt(error.cooldown.per)}` {self.bTypes[error.cooldown.type]}\nPlease retry after: ```{self.Hamood.pretty_dt(error.retry_after)}```",
                True,
            )

        elif isinstance(error, commands.MaxConcurrencyReached):
            await self.error_embed(
                ctx,
                "Maximum Concurrency Reached",
                f"Limit: `{error.number}` concurrent uses {self.bTypes[error.per]}",
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
                if "Send Messages" in perms:
                    return
                elif "Embed Links" in perms:
                    return await ctx.reply(
                        f"**I am missing the** `Embed Links` **permission!**",
                        mention_author=False,
                    )

                await self.error_embed(
                    ctx,
                    "I don't have the permission to do that",
                    f"I am missing the following permissions:```{perms}```",
                )
            elif isinstance(error, commands.NotOwner):
                await self.error_embed(
                    ctx, "Owner Only", "This command is resereved for owners of Hamood."
                )
            # else:
            #     await self.error_embed(
            #         ctx,
            #         "Restricted",
            #         f"You do not have access to this command.",
            #     )

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
                p = ctx.prefix

                await self.error_embed(
                    ctx,
                    "Input Error",
                    f"The command should be used like this:\n`{p}{ctx.command.name} {ctx.command.help.split('|||')[0]}`",
                )

        elif isinstance(error, commands.CommandInvokeError):

            if isinstance(error.__cause__, discord.Forbidden):
                await self.error_embed(
                    ctx,
                    "I don't have the permission to do that",
                    "",
                )
            else:
                await self.error_embed(
                    ctx,
                    "Whoops!",
                    f"Something went wrong with this command, try it again later.\n\nThe error has been reported:\n> `{error}`",
                )
                errorMsg = f"{self.Hamood.cstr('Uncaught Error:', ANSI.FAIL)}\nCommand: {ctx.command.name}\nError: {type(error).__name__}:\n\t{error}"
                print(
                    f'{self.Hamood.cstr("-" * 40, ANSI.WARNING)}\n{errorMsg}\n{self.Hamood.cstr("-" * 40, ANSI.WARNING)}'
                )
            # await error_channel.send(f"```py\n{errorMsg}```")


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
