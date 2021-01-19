import os
import discord
from discord.ext import commands

from modules.math_functions import *

import modules.checks as checks


class Math(commands.Cog):
    """Quick Mafs"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.isAllowedCommand()
    async def base(self, ctx, *, content: commands.clean_content):
        """``base [number)base], [next base]`` converts numbers between bases"""
        try:
            number, base2 = content.split(", ")
            number, base1 = number.split(")")
        except ValueError:
            await ctx.send("Invalid Input!")
            return
        answer = await base_conversion(number, int(base1), int(base2))
        embed = discord.Embed(
            title=f"Base {base1} to Base {base2}:",
            description=f"**Base {base1}:** `{number}`\n**Base {base2}:** `{answer}`\n",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    # await ctx.send(f"**Base {base1}:** `{number}`\n**Base {base2}:** `{answer}`\n")

    @commands.command(aliases=["calculate"])
    @checks.isAllowedCommand()
    async def calc(self, ctx, *, content: commands.clean_content):
        """``calc [equation]`` calculates the answer to the given equation (assumes natural log unless specified [log(base, number)]"""
        content = "".join([x for x in content])

        out = str(await calc_eq(content))
        if len(out) > 2000:
            out = out[:1950] + " Exceded Character Limit! "

        embed = discord.Embed(
            title="Calculate:",
            description=f"{content} **=**\n```{out}```",
            color=discord.Color.blue(),
        )

        await ctx.send(embed=embed)

    #  await ctx.send(f"**Answer: **`{out}`")

    @commands.command(aliases=["aliases"])
    @checks.isAllowedCommand()
    @commands.cooldown(4, 10, commands.BucketType.user)
    async def derivative(self, ctx, number, *, content: commands.clean_content):
        """``derivative [nth derivative] [equation]`` solves for the nth dervative of an equation"""
        ext = ["th", "st", "nd", "rd"]
        number = int(number)
        answer = await get_derivative(content, number)
        embed = discord.Embed(
            title=f"{number}{ext[number] if number <= 3 else 'th'} Derivative of :",
            description=f"{content} **=**\n```{answer}```",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(4, 10, commands.BucketType.user)
    async def solve(self, ctx, *, content: commands.clean_content):
        """``solve [equation]`` solves for variables in most math equations"""
        embed = discord.Embed(
            title="Solve:",
            description=f"**{content}**:\n```{await solve_eq(content)}```",
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

    #     await ctx.send(f"`{solve_eq(content)}`")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(2, 10, commands.BucketType.channel)
    async def graph(self, ctx, *, content: commands.clean_content):
        """``graph [equation], [next equation]`` graphs given equation"""
        content = content.split(", ") if ", " in content else [content]
        for i in range(len(content)):
            if ": " in content[i]:
                content[i] = content[i].split(": ")
            elif ": " not in content[i]:
                content[i] = [content[i]]

        done, graph = await graph_eq(content, f"{ctx.author}'s Graph")
        if done:
            await ctx.send(file=discord.File(graph))
            os.remove(graph)
        else:
            await ctx.send("`Could not graph equation`")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def py(self, ctx, *, content: commands.clean_content):
        """``py [code]`` runs `python-3.7.2` code and outputs to the chat. 
            Execution cannot exceed 1 second!
            Included Libraries: `math, numpy, time, random`"""

        content = content.replace("```py", "").replace("```", "")

        out, time = await run_code(content)
        if len(str(out)) > 2000:
            out = out[:1900] + " Exceded Character Limit! "

        msg = f"**Output:** {f'Completed in **{time}** seconds!' if time else ' '}```\n{out}```"
        embed = discord.Embed(
            title=f"{ctx.author}'s Code",
            description=msg,
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_author(
            name="Python",
            icon_url="https://cdn.discordapp.com/attachments/749779300181606411/800982444823937024/768px-Python-logo-notext.png",
        )
        # embed.set_thumbnail(
        #     url=carbon_code(content.replace("\n", "%0D%0A"), True)[: 2000 - len(msg)]
        # )

        await ctx.send(embed=embed)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def java(self, ctx, *, content: commands.clean_content):
        """``java [code]`` Compiles and runs your java code."""
        content = content.replace("```java", "").replace("```", "")
        out = await java_code(content)
        if len(str(out)) > 2000:
            out = out[:1900] + " Exceded Character Limit! "

        msg = f"**Output:** ```\n{out}```"
        embed = discord.Embed(
            title=f"{ctx.author}'s Code",
            description=msg,
            color=ctx.author.color,
            timestamp=ctx.message.created_at,
        )
        embed.set_author(
            name="Java",
            icon_url="https://cdn.discordapp.com/attachments/749779300181606411/800983689348513822/java-logo-transparent-png-5-Transparent-Images.png",
        )

        await ctx.send(embed=embed)

    # @commands.command()
    # @checks.isAllowedCommand()
    # @commands.cooldown(1, 30, commands.BucketType.guild)
    # async def code(self, ctx, *, content: commands.clean_content):
    #     """``code [code]`` converts code from text to a prettier image. `(uses carbon)`"""

    #     try:
    #         c = await carbon_code(content.replace("```py", "").replace("```", ""))
    #         await ctx.send(file=discord.File(c))
    #     except Exception:
    #         await ctx.send("`could not convert code`")
    #     os.remove(c)
    # content = (
    #     content.replace("```py", "").replace("```", "").replace("\n", "%0D%0A")
    # )
    # embed = discord.Embed(
    #     color=discord.Color.from_rgb(240, 240, 240),
    #     timestamp=ctx.message.created_at,
    # )
    # embed.set_footer(
    #     text=f"{ctx.author}'s code", icon_url=ctx.author.avatar_url,
    # )
    # embed.set_image(url=carbon_code(content[:1800], True))
    # await ctx.send(embed=embed)

    @commands.command(aliases=["ltx", "fool"])
    @checks.isAllowedCommand()
    @commands.cooldown(2, 10, commands.BucketType.channel)
    async def latex(self, ctx, *, content: commands.clean_content):
        """``latex [latex formula]`` converts latex to regular text"""

        text, e = await latex_to_text(content)
        if e is None:
            try:
                await ctx.send(file=discord.File(text))
            except Exception:
                await ctx.send("`Could Not Convert Formula`")

            os.remove(text)
        else:
            await ctx.send(f"```{e}```")

        # try:
        #     c = await carbon_code(content.replace("```py", "").replace("```", ""))
        #     await ctx.send(file=discord.File(c))
        #     await ctx.message.delete()
        # except Exception:
        #     await ctx.send("`could not convert code")
        # os.remove(c)


def setup(bot):
    bot.add_cog(Math(bot))

