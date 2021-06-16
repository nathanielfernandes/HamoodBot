import os, re, pprint

import discord
import random


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


async def quick_embed(ctx, reply=True, delete_image=True, **kwargs):
    title = kwargs.get("title", "")
    description = kwargs.get("description", "")
    timestamp = kwargs.get("timestamp")
    color = kwargs.get("color", discord.Color.from_rgb(*pastel_color()))
    image = kwargs.get("image")
    thumbnail = kwargs.get("thumbnail")
    author = kwargs.get("author")
    footer = kwargs.get("footer")
    fields = kwargs.get("fields")
    image_url = kwargs.get("image_url", "")
    url = kwargs.get("url", "")

    embed = discord.Embed(title=title, description=description, color=color, url=url)
    if timestamp:
        embed.timestamp = timestamp

    file = None
    if not image_url:
        if image:
            filename = os.path.basename(image)
            embed.set_image(url=f"attachment://{filename}")
            file = discord.File(fp=image, filename=filename)
    else:
        embed.set_image(url=image_url)

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if author:
        embed.set_author(
            name=author.get("name", ""),
            url=author.get("url", ""),
            icon_url=author.get("icon_url", ""),
        )

    if footer:
        embed.set_footer(
            text=footer.get("text", ""), icon_url=footer.get("icon_url", "")
        )

    if fields:
        for f in fields:
            embed.add_field(name=f.get("name", "-"), value=f.get("value", "-"))

    if reply:
        msg = await ctx.reply(file=file, embed=embed, mention_author=False)
    else:
        msg = await ctx.send(file=file, embed=embed)

    if delete_image and image:
        os.remove(image)

    return msg


# def quick_embed(
#     member, title=None, desc=None, image=None, color=None, rainbow=True, requested=True,
# ):
#     embed = discord.Embed()
#     r = lambda: random.randint(0, 255)

#     if color is None:
#         color = member.color if not rainbow else discord.Color.from_rgb(r(), r(), r())
#     else:
#         color = discord.Color.from_rgb(color[0], color[1], color[2])

#     embed = discord.Embed(title=title, description=desc, color=color,)
#     embed.set_image(url=image)
#     if requested:
#         embed.set_footer(text=f"Requested by {member}")

#     return embed.to_dict()
