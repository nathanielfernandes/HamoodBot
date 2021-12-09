import os, io
import discord
from discord.ext import commands

from modules.math_functions import *
from utils.Premium import PremiumCooldown


class Math(commands.Cog):
    """Quick Mafs"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def base(self, ctx, *, content: commands.clean_content):
        """<number>)<base>, <new base>|||Converts numbers between bases. Max Base = 36."""
        try:
            number, base2 = content.split(", ")
            number, base1 = number.split(")")
            answer = base_conversion(number, min(int(base1), 36), min(int(base2), 36))
        except:
            await self.Hamood.quick_embed(
                ctx,
                title="Could not convert number between bases.",
                description="Follow the format: `<number>)<base>`, `<base>`",
            )
        else:
            await self.Hamood.quick_embed(
                ctx,
                author={"name": "Base Conversion"},
                description=f"**Base {base1}:** `{number}`\n**Base {base2}:** `{answer}`\n",
                footer={"text": f"Base {base1} to Base {base2}"},
            )

    @commands.command(aliases=["calculate"])
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(2, 3, "user"), reg=(2, 5, "user")))
    async def calc(self, ctx, *, content: commands.clean_content):
        """<equation>|||Calculates the answer to the given equation (assumes natural log unless specified: log(base, number)."""
        try:
            out = str(calc_eq(content))
        except:
            await self.Hamood.quick_embed(ctx, title="Could not calculate the answer.")
        else:
            if len(out) > 1950:
                out = out[:1900] + " Exceded Character Limit! "

            await self.Hamood.quick_embed(
                ctx,
                author={"name": "Calculate"},
                description=f"`{content}` =\n```{out}```",
            )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "user")))
    async def derivative(self, ctx, *, content: commands.clean_content):
        """<equation>|||Calculates the derivative of an equation."""
        try:
            answer = get_derivative(content, 1)
        except:
            await self.Hamood.quick_embed(
                ctx, title="Could not calculate the derivative."
            )
        else:
            await self.Hamood.quick_embed(
                ctx,
                author={"name": "Derivative"},
                description=f"`{content}`:\n```{answer.replace('**', '^')}```",
            )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "user")))
    async def solve(self, ctx, *, content: commands.clean_content):
        """<equation>|||Solves for variables in most math equations. Works best with quadratics."""
        try:
            answer = solve_eq(content)
        except:
            await self.Hamood.quick_embed(ctx, title="Could not solve the equation.")
        else:
            await self.Hamood.quick_embed(
                ctx,
                author={"name": "Solve"},
                description=f'`{content}`:\n```{", ".join(answer)}```',
            )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(1, 5, "user"), reg=(1, 10, "user")))
    async def graph(self, ctx, *, content: commands.clean_content):
        """<equation>, [equation], [equations]...|||Graphs given equations. Only 'x' can be used as a variable."""
        content = content.lower()
        content = content.split(", ") if ", " in content else [content]

        done = graph_eq(content)
        if isinstance(done, io.BytesIO):
            await self.Hamood.quick_embed(
                ctx,
                author={
                    "name": f"{ctx.author}'s Graph",
                    "icon_url": ctx.author.avatar.url,
                },
                bimage=done,
            )
        else:
            await self.Hamood.quick_embed(
                ctx, author={"name": "Could not graph"}, description=f"```{done}```"
            )

    @commands.command(aliases=["ltx", "fool"])
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(2, 5, "user"), reg=(2, 10, "user")))
    async def latex(self, ctx, *, content: commands.clean_content):
        """<latex formula>|||Converts latex to regular text image."""
        e = latex_to_text(content)
        if isinstance(e, io.BytesIO):
            await self.Hamood.quick_embed(
                ctx, author={"name": f"{ctx.author}'s Latex"}, bimage=e
            )
        else:
            await self.Hamood.quick_embed(
                ctx,
                author={"name": "Could not convert formula"},
                description=f"```{e}```",
            )


def setup(bot):
    bot.add_cog(Math(bot))
