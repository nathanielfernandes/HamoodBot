import os, re, pprint, sys
import discord, functools
import random, asyncio
from io import BytesIO

import requests


def flatten(l, condition=lambda e: True, switch=lambda e: e) -> list:
    return [switch(e) for t in l for e in t if condition(e)]


def named_flatten(l, names, condition=lambda e: True, switch=lambda e: e) -> dict:
    return dict(zip(names, [switch(e) for t in l for e in t if condition(e)]))


def pastel_color():
    rgb = [100, random.randint(100, 237), 237]
    random.shuffle(rgb)
    return tuple(rgb)


def pretty_time_delta(seconds):
    s = seconds
    seconds = round(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        p = "%d days, %d hours, %d minutes, %d seconds" % (
            days,
            hours,
            minutes,
            seconds,
        )
    elif hours > 0:
        p = "%d hours, %d minutes, %d seconds" % (hours, minutes, seconds)
    elif minutes > 0:
        p = "%d minutes, %d seconds" % (minutes, seconds)
    else:
        p = "%d seconds" % (seconds,)

    if s < 0:
        p = "-" + p
    return p


def pretty_dt(s: float) -> str:
    if s < 1:
        return f"{round(s * 1000)} miliseconds"
    elif s < 60:
        return f"{round(s)} second{'s' if round(s) != 1 else ''}"

    y, s = divmod(s, 3.154e7)
    mm, s = divmod(s, 2.628e6)
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)

    au = {"year": y, "month": mm, "day": d, "hour": h, "minute": m}
    ex = []
    for u in au:
        if au[u] > 0:
            return ", ".join(
                (
                    f"{round(au[i])} {i}{'s' if round(au[i]) != 1 else ''}"
                    if round(au[i]) != 0
                    else ""
                )
                for i in au
                if i not in ex
            ) + (
                f", {round(s)} second{'s' if round(s) != 1 else ''}"
                if round(s) != 0
                else ""
            )
        else:
            ex.append(u)


def random_name(ext: str = "png") -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(18)) + "." + ext


def pil_to_bytes(img, ext: str = "png"):
    buffer = BytesIO()
    img.save(buffer, ext)
    buffer.seek(0)
    img.close()
    return buffer


async def quick_embed(ctx, reply=True, delete_image=True, send=True, **kwargs):
    title = kwargs.get("title", "")
    description = kwargs.get("description", "")
    timestamp = kwargs.get("timestamp")
    color = kwargs.get("color", discord.Color.from_rgb(*pastel_color()))
    thumbnail = kwargs.get("thumbnail")
    author = kwargs.get("author")
    footer = kwargs.get("footer", {})
    fields = kwargs.get("fields")
    image = kwargs.get("image")
    bimage = kwargs.get("bimage")
    image_url = kwargs.get("image_url", "")
    pil_img = kwargs.get("pil_image")
    pil_ext = kwargs.get("pil_ext", "png")
    url = kwargs.get("url", "")
    stats = kwargs.get("stats")

    embed = discord.Embed(title=title, description=description, color=color, url=url)
    if timestamp:
        embed.timestamp = timestamp

    file = None
    if not image_url:
        if pil_img:
            bimage = await ctx.bot.Hamood.run_async(
                pil_to_bytes, img=pil_img, ext=pil_ext
            )
            name = random_name(pil_ext)
            embed.set_image(url=f"attachment://{name}")
            file = discord.File(fp=bimage, filename=name)
        elif bimage:
            embed.set_image(url=f"attachment://bytesimage.jpg")
            file = discord.File(fp=bimage, filename="bytesimage.jpg")
        elif image:
            filename = os.path.basename(image)
            embed.set_image(url=f"attachment://{filename}")
            file = discord.File(fp=image, filename=filename)
    else:
        embed.set_image(url=image_url)

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if author:
        embed.set_author(
            name=author.get("name", "\u200b"),
            url=author.get("url", ""),
            icon_url=author.get("icon_url", ""),
        )

    if footer or stats:
        text = footer.get("text", "")
        if text and stats:
            text += " • "
        embed.set_footer(
            text=text + (f"{ctx.prefix}{ctx.command.name} • {stats}" if stats else ""),
            icon_url=footer.get("icon_url", ""),
        )

    if fields:
        for f in fields:
            embed.add_field(
                name=f.get("name", "\u200b"),
                value=f.get("value", "\u200b"),
                inline=f.get("inline", True),
            )

    if send:
        if reply:
            msg = await ctx.reply(file=file, embed=embed, mention_author=False)
        else:
            msg = await ctx.send(file=file, embed=embed)

    if pil_img or bimage:
        try:
            ctx.bot.Hamood.total_gens += 1
            ctx.bot.Hamood.total_gen_bytes += sys.getsizeof(bimage)
        except:
            pass
        bimage.close()

    if delete_image and image:
        os.remove(image)

    if send:
        return msg
    else:
        return embed


class ReactionController:
    __slots__ = ("mapping", "buttons")

    def __init__(self):
        self.mapping = {}
        self.buttons = []
        methods = [
            func
            for func in dir(self)
            if callable(getattr(self, func)) and not func.startswith("__")
        ]

        buttonPositions = {}
        for name in methods:
            method = getattr(self, name)
            if hasattr(method, "__emoji__") and hasattr(method, "__position__"):
                self.mapping[method.__emoji__] = method
                buttonPositions[method.__emoji__] = method.__position__

        self.buttons = [None] * len(buttonPositions)
        for button, position in buttonPositions.items():
            if position == -1:
                self.buttons.append(button)
            else:
                self.buttons[position] = button

        self.buttons = [i for i in self.buttons if i is not None]

    def ismapped(self, emoji):
        return emoji in self.mapping

    async def reaction_event(self, emoji):
        await self.mapping[emoji]()

    @staticmethod
    def button(emoji, position=-1):
        def decorator(func):
            func.__emoji__ = emoji
            func.__position__ = position
            return func

        return decorator


def to_async(syncfunc):
    @functools.wraps(syncfunc)
    async def sync_wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        func = functools.partial(syncfunc, *args, **kwargs)
        return await loop.run_in_executor(None, func)

    return sync_wrapper
