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


def quick_embed(
    member, title=None, desc=None, image=None, color=None, rainbow=True, requested=True,
):
    embed = discord.Embed()
    r = lambda: random.randint(0, 255)

    if color is None:
        color = member.color if not rainbow else discord.Color.from_rgb(r(), r(), r())
    else:
        color = discord.Color.from_rgb(color[0], color[1], color[2])

    embed = discord.Embed(title=title, description=desc, color=color,)
    embed.set_image(url=image)
    if requested:
        embed.set_footer(text=f"Requested by {member}")

    return embed.to_dict()
