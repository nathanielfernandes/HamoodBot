from __future__ import annotations
import random
import discord, os
from typing import List, Union, Any
from types import CoroutineType, FunctionType
from discord.ext import commands


def get_interaction_value(interaction: discord.Interaction):
    return interaction.data["values"][0]


class SelectOption(discord.components.SelectOption):
    """An option to be used in a select menu"""

    def __init__(self, label: str = None, emoji: str = None, item: Any = None):
        """
        The item arugment can be anything that you want. When the option is selected by a user your
        given callback for the menu will be passed the item contained in the option.

        Args:
            label (str, optional): The label of the option. Defaults to None.
            emoji (str, optional): The Emoji of the option. Defaults to None.
            item (Any, optional): An Optional item that the option will hold onto. Defaults to None.
        """
        super().__init__(label=label, emoji=emoji, value=os.urandom(16).hex())
        self.item = item


class SelectMenu(discord.ui.Select):
    """A Wrapper for the select menu that can be used in a view."""

    def __init__(
        self,
        options: List[SelectOption],
        placeholder: str = None,
        callback: CoroutineType = None,
        check: FunctionType = None,
        check_fail: CoroutineType = None,
        min_values: int = 1,
        max_values: int = 1,
    ):
        """
        The callback, check, and check_fail functions will be passed the:
            interaction object, the item held by the option, the menu object

        Args:
            options (List[SelectOption]): list of options (in order)
            placeholder (str, optional): Placeholder value for the menu. Defaults to None.
            callback (CoroutineType, optional): function to call when an option is selected by a user. Defaults to None.
            check (FunctionType, optional): a function to filter out unwanted uses of the menu. Defaults to None.
            check_fail (CoroutineType, optional): a function that will run when you check fails. Defaults to None.
        """
        super().__init__(
            placeholder=placeholder,
            options=options,
            min_values=min_values,
            max_values=max_values,
        )
        self._mapping = {option.value: option.item for option in options}
        self.check = check or (lambda interaction, item, menu: True)
        self._callback = callback
        self.check_fail = check_fail or (
            lambda interaction, item, menu: interaction.response.send(
                content="**This message does not belong to you**", ephemeral=True
            )
        )

    async def callback(self, interaction: discord.Interaction):
        items = (
            self._mapping[interaction.data["values"][0]]
            if len(interaction.data["values"]) == 1
            else [self._mapping[n] for n in interaction.data["values"]]
        )

        if self.check(interaction, items, self):
            await self._callback(interaction, items, self)
        else:
            await self.check_fail(interaction, items, self)


class Button(discord.ui.Button):
    """A button to be used in a view"""

    BLURPLE = discord.ButtonStyle.blurple
    GREEN = discord.ButtonStyle.green
    GRAY = discord.ButtonStyle.gray
    RED = discord.ButtonStyle.red
    LINK = discord.ButtonStyle.link

    def __init__(
        self,
        label: str = None,
        emoji: str = None,
        url: str = None,
        style: Union[
            Button.BLURPLE, Button.GREEN, Button.GRAY, Button.RED, Button.LINK
        ] = discord.ButtonStyle.blurple,
        disabled: bool = False,
        item: Any = None,
        callback: CoroutineType = None,
        check: FunctionType = None,
        check_fail: CoroutineType = None,
        row: int = None,
    ):
        """
        The callback, check, and check_fail functions will be passed the:
            interaction object, the item held by the button, the button object

        Args:
            label (str, optional): The label of the button. Defaults to None.
            emoji (str, optional): The emoji of the button. Defaults to None.
            url (str, optional): [description]. Defaults to None.
            style (Union[ Button.BLURPLE, Button.GREEN, Button.GRAY, Button.RED, Button.LINK ], optional): the sytle/color of the button. Defaults to discord.ButtonStyle.blurple.
            disabled (bool, optional): [description]. Defaults to False.
            item (Any, optional): [description]. Defaults to None.
            callback (CoroutineType, optional): [description]. Defaults to None.
            check (FunctionType, optional): [description]. Defaults to None.
            check_fail (CoroutineType, optional): [description]. Defaults to None.
        """
        super().__init__(label=label, emoji=emoji, style=style, url=url, row=row)
        self.disabled = disabled
        self.item = item
        self.check = check or (lambda interaction, item, btn: True)
        self._callback = callback
        self.check_fail = check_fail or (
            lambda interaction, item, btn: interaction.response.send(
                content="**This message does not belong to you**", ephemeral=True
            )
        )

    async def callback(self, interaction: discord.Interaction):
        if self.check(interaction, self.item, self):
            await self._callback(interaction, self.item, self)
        else:
            await self.check_fail(interaction, self.item, self)


class View(discord.ui.View):
    async def start(
        self,
        ctx: commands.Context,
        content: str = None,
        embed: discord.Embed = None,
        mention_author: bool = False,
        clear_after: bool = True,
        timeout: float = 180.0,
    ):
        self.timeout = timeout
        self.msg = await ctx.reply(
            content=content,
            embed=embed,
            view=self,
            mention_author=mention_author,
        )
        if clear_after:
            await self.wait()
            await self.msg.edit(view=None)

    def add_component(self, component: Union[SelectMenu, Button]):
        self.add_item(component)

    def add_components(self, components: List[Union[SelectMenu, Button]]):
        for component in components:
            self.add_item(component)

    async def clear(self):
        await self.msg.edit(view=None)


def chunk_options(
    l: List[SelectOption],
    n: int = 25,
    placeholder: str = "Page",
    callback: CoroutineType = None,
    check: FunctionType = None,
    check_fail: CoroutineType = None,
    min_values: int = 1,
    max_values: int = 1,
) -> List[SelectMenu]:
    chunks = []
    chunk = []
    for i in range(len(l)):
        if i != 0 and i % n == 0:
            chunks.append(chunk)
            chunk = []
        else:
            chunk.append(l[i])

    if len(chunk) > 0:
        chunks.append(chunk)

    return [
        SelectMenu(
            options=chunks[i],
            callback=callback,
            check=check,
            check_fail=check_fail,
            placeholder=f"{placeholder} {i+1}",
            min_values=min_values,
            max_values=max_values,
        )
        for i in range(len(chunks))
    ]


class EasyPaginator(discord.ui.View):
    def __init__(self, ctx: commands.Context, pages: list[discord.Embed]):
        super().__init__()
        self.pages = pages
        self.page_number = 0
        self.ctx = ctx
        self.msg = None

    async def start(self):
        self.update_buttons()
        self.msg = await self.ctx.reply(
            embed=self.pages[0], view=self, mention_author=False
        )
        await self.wait()
        await self.msg.edit(view=None)

    def update_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if (
                    (len(self.pages) == 0)
                    or (
                        (child.label == "❮❮" or child.label == "❮")
                        and 0 == self.page_number
                    )
                    or (
                        (child.label == "❯❯" or child.label == "❯")
                        and len(self.pages) - 1 == self.page_number
                    )
                ):
                    child.disabled = True
                else:
                    child.disabled = False

    async def update_message(self, interaction: discord.Interaction):
        self.update_buttons()
        await interaction.response.edit_message(
            embed=self.pages[self.page_number], view=self
        )

    async def user_check(self, interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                content="**This message does not belong to you!**", ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="❮❮", style=discord.ButtonStyle.grey)
    async def firstpage(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        if await self.user_check(interaction):
            self.page_number = 0
            await self.update_message(interaction)

    @discord.ui.button(label="❮", style=discord.ButtonStyle.primary)
    async def prevpage(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        if await self.user_check(interaction):
            self.page_number = self.page_number = max(
                0, min(self.page_number - 1, len(self.pages) - 1)
            )
            await self.update_message(interaction)

    @discord.ui.button(label="❯", style=discord.ButtonStyle.primary)
    async def nextpage(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        if await self.user_check(interaction):
            self.page_number = max(0, min(self.page_number + 1, len(self.pages) - 1))
            await self.update_message(interaction)

    @discord.ui.button(label="❯❯", style=discord.ButtonStyle.grey)
    async def lastpage(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        if await self.user_check(interaction):
            self.page_number = len(self.pages) - 1
            await self.update_message(interaction)

    @discord.ui.button(
        emoji="<a:dice:791541710995980308>", style=discord.ButtonStyle.green
    )
    async def rng(self, _button: discord.ui.Button, interaction: discord.Interaction):
        if await self.user_check(interaction):
            self.page_number = random.randint(0, len(self.pages) - 1)
            await self.update_message(interaction)

    # @discord.ui.button(label="✕", style=discord.ButtonStyle.red)
    # async def close(self, _button: discord.ui.Button, interaction: discord.Interaction):
    #     if await self.user_check(interaction):
    #         await self.msg.edit(view=None)
