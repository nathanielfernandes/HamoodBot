import discord
from discord.ext import commands
from discord.ext.commands import Command, CooldownMapping, Cooldown, BucketType


class PremiumCooldown:
    def __init__(self, prem: tuple, reg: tuple):
        self.types = {
            "user": BucketType.user,
            "channel": BucketType.channel,
            "guild": BucketType.guild,
        }

        self.premium_mapping = CooldownMapping.from_cooldown(*self.clean(prem))
        self.regular_mapping = CooldownMapping.from_cooldown(*self.clean(reg))

    async def __call__(self, ctx: commands.Context):
        isPremium = await ctx.bot.Hamood.user_is_premium(ctx.author.id)
        mapping = self.premium_mapping if isPremium else self.regular_mapping
        bucket = mapping.get_bucket(ctx.message)

        retry_after = bucket.update_rate_limit()
        if retry_after:
            raise commands.CommandOnCooldown(bucket, retry_after)

        return True

    def clean(self, pack: tuple):
        rate, per, _type = pack
        return (rate, per, self.types[_type])
