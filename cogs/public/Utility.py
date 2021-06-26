import discord, re
from discord.ext import commands
from typing import Union


class Utility(commands.Cog):
    """Server Utility"""

    def __init__(self, bot):
        self.bot = bot
        self.Hamood = bot.Hamood

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(embed_links=True)
    @commands.cooldown(3, 60, commands.BucketType.guild)
    async def prefix(
        self,
        ctx,
        action: str = None,
        *,
        content: commands.clean_content(remove_markdown=True) = None,
    ):
        """[set|reset] [new prefix]|||Changes Hamood's prefix for this server."""
        if action is None and content is None:
            return await self.Hamood.quick_embed(
                ctx, description=f"My Prefix Currently is: `{ctx.prefix}`"
            )

        if action is not None:
            if action == "reset":
                self.Hamood.prefixes_list[ctx.guild.id] = "."
                await self.Hamood.Prefixdb.change_prefix(str(ctx.guild.id), ".")
                return await self.Hamood.quick_embed(
                    ctx, description=f"Set Prefix Back to: `.`"
                )
            elif action == "set":
                if content is None:
                    return await self.Hamood.quick_embed(
                        ctx, description="Please Specify A Prefix!"
                    )
                ms = self.Hamood.re_member.findall(content)
                rs = self.Hamood.re_role.findall(content)
                es = self.Hamood.re_emoji.findall(content)
                cs = self.Hamood.re_channel.findall(content)
                og_c = str(content)
                content = content or "@"
                content = (
                    content.replace("@", "").replace("/", "").replace("\\", "")[:10]
                )
                if content is None or content == "" or ms or rs or es or cs:
                    return await self.Hamood.quick_embed(
                        ctx, description=f"Cannot Change Prefix to: `{og_c}`"
                    )
                else:
                    self.Hamood.prefixes_list[ctx.guild.id] = content
                    await self.Hamood.Prefixdb.change_prefix(str(ctx.guild.id), content)
                    return await self.Hamood.quick_embed(
                        ctx, description=f"Set Prefix to: `{content}`"
                    )
            else:
                await self.Hamood.quick_embed(
                    ctx, description="Action can only be `set` or `reset`!"
                )

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(embed_links=True, manage_channels=True)
    async def pinboard(self, ctx):
        """|||Sets up a pin-board-📌 channel in the server which allows members to 'pin' messages there without needing extra permisions. Add messages to the pin-board by reacting to them with 📌."""
        channel = discord.utils.get(ctx.guild.channels, name="pin-board-📌")
        if channel is None:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await ctx.guild.create_text_channel(
                "pin-board-📌",
                topic="React to a message with a 📌 and it will pop up here.",
                overwrites=overwrites,
            )
            await self.Hamood.quick_embed(
                ctx,
                description=f"{ctx.author.mention} has setup the `pin-board-📌`. Add messages to it by reacting to it with 📌.",
                color=discord.Color.from_rgb(219, 24, 50),
            )

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True, embed_links=True)
    @commands.cooldown(5, 20, commands.BucketType.guild)
    async def emojisteal(
        self,
        ctx,
        emoji: Union[discord.PartialEmoji, str],
        *,
        name: commands.clean_content = None,
    ):
        """<:emoji:|emoji url> [name]|||Steals the sent emoji or image and adds it to the server."""
        eurl = None
        if isinstance(emoji, discord.PartialEmoji):
            eurl = emoji.url
            name = emoji.name or name
        else:
            ls = self.Hamood.re_ValidImageUrl.findall(emoji)
            if len(ls) > 0:
                eurl = ls[0]
            name = name or "changeme"

        if not eurl:
            return await self.Hamood.quick_embed(
                ctx, description=f"Could not find the emoji/image: `{emoji}`"
            )

        emoji_bytes = await self.Hamood.ahttp.bytes_download(url=str(eurl), no_io=True)

        if not emoji_bytes:
            return await self.Hamood.quick_embed(
                ctx, description=f"Could not download the emoji/image :("
            )
        try:
            added_emoji = await ctx.guild.create_custom_emoji(
                name=name[:32], image=emoji_bytes
            )
        except:
            await self.Hamood.quick_embed(
                ctx,
                description="Could not add the emoji to the server. Emoji cap may be reached or file size/type is not supported.",
            )
        else:
            await self.Hamood.quick_embed(
                ctx,
                title=f"{added_emoji} has been added to the server",
                description=f"```yaml\nName: {name[:32]}\nTag: {added_emoji}```",
                thumbnail=str(added_emoji.url),
                footer={"text": f"Added by {ctx.author}"},
            )

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(embed_links=True, manage_channels=True)
    async def quickchannel(self, ctx, *, name: commands.clean_content = " "):
        """<channel name>|||Creates a \u2795 voice channel that creates temporary voice channels for members that joins it. Make sure this emoji: \u2795, remains in the channel name."""
        await ctx.author.guild.create_voice_channel(f"\u2795 {name}")
        await self.Hamood.quick_embed(
            ctx,
            description=f"{ctx.author.mention} has setup a `quickchannel` named `\u2795 {name}`",
            color=discord.Color.from_rgb(250, 250, 250),
        )

    @commands.command(name="subscribe (comming soon)")
    async def subscribe(self, ctx):
        """<youtube channel url>|||Subscribes the current channel to a youtube channel. Any uploads from the channel will be sent here."""
        pass

    @commands.command(name="unsubscribe (comming soon)")
    async def unsubscribe(self, ctx):
        """<youtube channel url>|||Unsubscribes the current channel from a youtube channel."""
        pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            if before.channel is not None:
                if str(member.id) in before.channel.name:
                    try:
                        await before.channel.delete()
                    except:
                        print("Could not delete channel!")

            if after.channel is not None:
                if "\u2795" in str(after.channel.name):
                    try:
                        channel = await after.channel.clone(
                            name=f"{member.name}'s quick channel ☁️ {member.id}"
                        )
                        await member.move_to(channel, reason="Quick Channel Move")
                    except:
                        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            if str(payload.emoji) == "📌":
                channel = discord.utils.get(
                    payload.member.guild.channels, name="pin-board-📌"
                )
                if channel is not None and payload.channel_id != channel.id:
                    try:
                        c = await self.bot.fetch_channel(payload.channel_id)
                        msg = await c.fetch_message(payload.message_id)
                    except discord.errors.NotFound:
                        return

                    messages = await channel.history(limit=100).flatten()

                    for m in messages:
                        if len(m.embeds) >= 1:
                            if str(msg.id) in str(m.embeds[0].footer.text):
                                return

                    embed = discord.Embed(
                        title="",
                        description="",
                        color=discord.Color.from_rgb(219, 24, 50),
                    )
                    embed.set_author(
                        name=f"{msg.author.display_name} 📌",
                        icon_url=msg.author.avatar_url,
                    )
                    embed.set_footer(
                        text=f"{payload.member} pinned this • {msg.id}",
                    )

                    if len(msg.embeds) >= 1 and "tenor" not in msg.content:
                        embed_dict = msg.embeds[0].to_dict()

                        embed.title = embed_dict.get("title", "")
                        desc = (
                            msg.content
                            + ("\n\n" if len(msg.content) >= 1 else "")
                            + embed_dict.get("description", "")
                        )
                        url = embed_dict.get("url", "")
                        img = embed_dict.get("image")
                        embed.description = desc
                        embed.url = str(url)

                        for f in embed_dict.get("fields", []):
                            embed.add_field(
                                name=f["name"],
                                value=f["value"],
                                inline=f["inline"],
                            )

                        if img is not None:
                            embed.set_image(url=img["url"])
                        else:
                            image_urls = self.Hamood.re_ValidImageUrl.findall(
                                f"{msg.content} {url} {embed.description}"
                            )
                            if len(image_urls) > 0:
                                embed.set_image(url=image_urls[0])

                        t_url = embed_dict.get("thumbnail", {}).get("url", "")
                        if embed.to_dict().get("image", {}).get("url", "") != t_url:
                            embed.set_thumbnail(url=t_url)
                    else:
                        embed.description = msg.content

                        urls = ""
                        attachments = []
                        if len(msg.attachments) > 0:
                            for atch in msg.attachments:
                                urls += f" {atch.url}"
                                attachments.append(atch)
                        urls += f" {msg.content}"

                        image_urls = self.Hamood.re_ValidImageUrl.findall(urls)
                        if len(image_urls) > 0:
                            embed.set_image(url=image_urls[0])

                        embed.add_field(
                            name="Attachments",
                            value="\n".join(
                                f"[{a.filename}]({a.url})" for a in attachments
                            ),
                        )

                    embed.add_field(
                        name="\u200b",
                        value=f"{msg.channel.mention} • [jump to message]({msg.jump_url})",
                        inline=False,
                    )

                    try:
                        await channel.send(embed=embed)
                    except:
                        pass


def setup(bot):
    bot.add_cog(Utility(bot))
