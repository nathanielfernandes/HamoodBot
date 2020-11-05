import discord
from discord.ext import commands

from modules.chem_functions import (
    balance_equation,
    format_equation,
    get_molar_mass,
    get_elements,
    get_element_period,
    elements,
)


class Chemistry(commands.Cog):
    """Quick Chem"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def balance(self, ctx, *, content: commands.clean_content):
        """``balance [equation] ex. FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl`` balances chemical equations"""
        eq = balance_equation(content)
        if isinstance(eq, tuple):
            reac, prod = eq
            eq = format_equation(reac, prod)

        embed = discord.Embed(
            title=f"Balance chemical equation:",
            description=f"**{content}**:\n```ini\n{eq}```",
            color=discord.Color.purple(),
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def stoich(self, ctx, *, content: commands.clean_content):
        """``stoich [equation] ex. FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl`` balances chemical equations and returns extra info"""

        eq = balance_equation(content)
        if isinstance(eq, tuple):
            reac, prod = eq
            eq = format_equation(reac, prod)

        masses = "\n".join(
            [
                f"{i}-[{get_molar_mass(i)}]"
                for i in list(reac.keys()) + list(prod.keys())
            ]
        )
        elements = get_elements(list(reac.keys()) + list(prod.keys()))
        values = sum(elements.values())
        elements = "\n".join(
            [
                f"{i}-[{elements[i]}]-{(elements[i]/values)*100:0.2f}%"
                for i in elements.keys()
            ]
        )

        embed = discord.Embed(
            title=f"Stoichiometry Info:",
            description=f"**{content}**",
            color=discord.Color.purple(),
        )
        embed.add_field(
            name="**Balanced Equation:**", value=f"```ini\n{eq}```", inline=False
        )
        embed.add_field(
            name="**Elements:**", value=f"```ini\n{elements}```",
        )
        embed.add_field(
            name="**Molar Masses:**", value=f"```ini\n{masses}```",
        )

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def molar(self, ctx, *, content: commands.clean_content):
        """``molar [compound]`` returns the molar mass of the compound"""
        elements = get_elements([content])
        if elements is not None:
            values = sum(elements.values())
            percents = "\n".join(
                [f"{i}-[{(elements[i]/values)*100:0.2f}%]" for i in elements.keys()]
            )
            embed = discord.Embed(
                title=f"Molar Mass of {content}:",
                description=f"```ini\n{get_molar_mass(content)}\n{percents}```",
                color=discord.Color.purple(),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid Input")

    @commands.command()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def table(self, ctx, element):
        """``table [element symbol or number]`` returns a list of periodic information"""
        table = get_element_period(element)

        if table is not None:
            embed = discord.Embed(
                title=f"Periodic Table {table[0]} | {element} | {table[2]}",
                color=discord.Color.purple(),
            )
            embed.add_field(
                name="**Atomic Mass**", value=f"```\n{table[3]} u```",
            )
            embed.add_field(
                name="**Density**", value=f"```\n{table[14]} g/cm^3```",
            )
            embed.add_field(
                name="**Group**", value=f"```\n{table[15]}```",
            )
            embed.add_field(
                name="**Standard State**", value=f"```\n{table[11]}```",
            )
            embed.add_field(
                name="**Meliting Point**", value=f"```\n{table[12]} K```",
            )
            embed.add_field(
                name="**Boiling Point**", value=f"```\n{table[13]} K```",
            )
            embed.add_field(
                name="**Electronegativity**", value=f"```\n{table[6]}```",
            )
            embed.add_field(
                name="**Ionization Energy**", value=f"```\n{table[8]} eV```",
            )
            embed.add_field(
                name="**Electron Configuration**", value=f"```\n{table[5]}```",
            )
            embed.add_field(
                name="**Oxidation States**", value=f"```\n{table[10]}```",
            )
            embed.add_field(
                name="**Atomic Radius**", value=f"```\n{table[7]} ppm```",
            )
            embed.add_field(
                name="**Year Discovered**", value=f"```\n{table[16]}```",
            )

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{element} is not a valid element!")


#     answer = ChemEq(content).balance()
#     await ctx.send(f"**Balanced Equation:** {answer}")

# @commands.command()
# @commands.cooldown(4, 10, commands.BucketType.user)
# async def balance(self, ctx, *, content: commands.clean_content):
#     """``balance [equation] ex. FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl`` balances chemical equations"""
#     answer = ChemEq(content).balance()
#     await ctx.send(f"**Balanced Equation:** {answer}")


def setup(bot):
    bot.add_cog(Chemistry(bot))
