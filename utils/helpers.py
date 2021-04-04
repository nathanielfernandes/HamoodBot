import os
import discord
import random


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


async def quick_embed(ctx, reply=False, delete_image=True, **kwargs):
    r = lambda: random.randint(0, 255)
    title = kwargs.get("title")
    description = kwargs.get("description")
    timestamp = kwargs.get("timestamp")
    color = kwargs.get("color", discord.Color.from_rgb(r(), r(), r()))
    image = kwargs.get("image")
    thumbnail = kwargs.get("thumbnail")
    author = kwargs.get("author")
    footer = kwargs.get("footer")
    fields = kwargs.get("fields")

    embed = discord.Embed(title=title, description=description, color=color)
    if timestamp:
        embed.timestamp = timestamp

    if image:
        filename = os.path.basename(image)
        embed.set_image(url=f"attachment://{filename}")
        file = discord.File(fp=image, filename=filename)
    else:
        file = None

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

