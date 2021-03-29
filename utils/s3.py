import os
import asyncio
import aiobotocore
import discord
import random


try:
    AWS_ACCESS_KEY_ID = os.environ.get("AWSACCESSKEYID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWSSECRETKEY")

except KeyError:
    from dotenv import load_dotenv

    load_dotenv()
    AWS_ACCESS_KEY_ID = os.environ.get("AWSACCESSKEYID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWSSECRETKEY")


class S3:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.session = aiobotocore.get_session()

    async def discordUpload(
        self,
        ctx,
        filename: str,
        description=None,
        title=None,
        requested=True,
        rainbow=True,
        color=None,
    ):
        link = await self.upload(filename)
        r = lambda: random.randint(0, 255)

        if color is None:
            color = (
                ctx.author.color
                if not rainbow
                else discord.Color.from_rgb(r(), r(), r())
            )
        else:
            color = discord.Color.from_rgb(color[0], color[1], color[2])

        embed = discord.Embed(title=title, description=description, color=color,)
        embed.set_image(url=link)
        if requested:
            embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

    async def upload(self, filename: str):
        key = os.path.basename(filename)

        async with self.session.create_client(
            "s3",
            region_name="us-east-2",
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
        ) as client:
            await client.put_object(
                Bucket=self.bucket_name, Key=key, Body=open(filename, "rb")
            )
        return "https://hamoodbucket.s3.us-east-2.amazonaws.com/" + key

    async def delete(self, filename: str):
        key = filename
        async with self.session.create_client(
            "s3",
            region_name="us-east-2",
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
        ) as client:
            await client.delete_object(Bucket=self.bucket_name, Key=key)
