import discord
from discord.ext import commands
from modules.chem_functions import *

from utils.Premium import PremiumCooldown


class Chemistry(commands.Cog):
    """Get Chemistry Help"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(5, 5, "user"), reg=(5, 10, "user")))
    async def balanceeq(self, ctx, *, content: commands.clean_content):
        """<chemical equation>|||Balances chemical equations `ex. FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl`."""
        try:
            eq = balance_equation(content)
            if isinstance(eq, tuple):
                reac, prod = eq
                eq = format_equation(reac, prod)
        except:
            return await self.Hamood.quick_embed(
                ctx,
                title=f"Could not balance `{content}`",
                description=f"Follow this format:\n```FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl```",
            )
        else:
            await self.Hamood.quick_embed(
                ctx,
                author={"name": "Balanced chemical equation"},
                description=f"**{content}**:```ini\n{eq}```",
            )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(5, 5, "user"), reg=(5, 10, "user")))
    async def stoich(self, ctx, *, content: commands.clean_content):
        """<chemical equation>|||Balances chemical equations with extra info `ex. FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl`."""
        try:
            eq = balance_equation(content)
            if isinstance(eq, tuple):
                reac, prod = eq
                eq = format_equation(reac, prod)

            masses = "\n".join(
                f"{i}: {get_molar_mass(i)}"
                for i in list(reac.keys()) + list(prod.keys())
            )
            elements = get_elements(list(reac.keys()) + list(prod.keys()))
            values = sum(elements.values())
            elements = "\n".join(
                f"{i}: {(elements[i]/values)*100:0.2f}%" for i in elements.keys()
            )
        except:
            return await self.Hamood.quick_embed(
                ctx,
                title=f"Could not Balance`{content}`",
                description=f"Follow this format:\n```FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl```",
            )
        else:
            await self.Hamood.quick_embed(
                ctx,
                author={"name": "Balanced chemical equation"},
                description=f"**{content}**:```ini\n{eq}```",
                fields=[
                    {
                        "name": "Elements",
                        "value": f"```yaml\n{elements}```",
                        "inline": False,
                    },
                    {
                        "name": "Molar Masses",
                        "value": f"```yaml\n{masses}```",
                        "inline": False,
                    },
                ],
            )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    @commands.check(PremiumCooldown(prem=(5, 5, "user"), reg=(5, 10, "user")))
    async def molar(self, ctx, *, content: commands.clean_content):
        """<chemical compound>|||Returns the molar mass of the compound."""
        elements = get_elements([content])
        if elements is not None:
            values = sum(elements.values())
            percents = "\n".join(
                f"{i}: {(elements[i]/values)*100:0.2f}%" for i in elements.keys()
            )
            await self.Hamood.quick_embed(
                ctx,
                author={"name": f"Molar Mass of {content}"},
                description=f"```yaml\n{get_molar_mass(content)}``````yaml\n{percents}```",
            )
        else:
            await self.Hamood.quick_embed(
                ctx, title=f"`{content}` is not a valid compound"
            )

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def table(self, ctx, element):
        """<element symbol|atomic number>|||Returns a list of periodic information on a given element."""
        table = get_element_period(element)

        if table is not None:
            await self.Hamood.quick_embed(
                ctx,
                author={
                    "name": f"Periodic Table • {table[0]} | {table[1]} | {table[2]}"
                },
                fields=[
                    {"name": "**Atomic Mass**", "value": f"```\n{table[3]} u```",},
                    {"name": "**Density**", "value": f"```\n{table[14]} g/cm^3```",},
                    {"name": "**Group**", "value": f"```\n{table[15]}```",},
                    {"name": "**Standard State**", "value": f"```\n{table[11]}```",},
                    {"name": "**Melting Point**", "value": f"```\n{table[12]} K```",},
                    {"name": "**Boiling Point**", "value": f"```\n{table[13]} K```",},
                    {"name": "**Electronegativity**", "value": f"```\n{table[6]}```",},
                    {
                        "name": "**Ionization Energy**",
                        "value": f"```\n{table[8]} eV```",
                    },
                    {
                        "name": "**Electron Configuration**",
                        "value": f"```\n{table[5]}```",
                    },
                    {"name": "**Oxidation States**", "value": f"```\n{table[10]}```",},
                    {"name": "**Atomic Radius**", "value": f"```\n{table[7]} ppm```",},
                    {"name": "**Year Discovered**", "value": f"```\n{table[16]}```",},
                ],
            )
        else:
            await self.Hamood.quick_embed(
                ctx, title=f"`{element}` is not a valid element"
            )


def setup(bot):
    bot.add_cog(Chemistry(bot))
