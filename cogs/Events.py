import os
import sys
import discord
from discord.ext import commands

path = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/modules'
sys.path.insert(1, path)

import message_functions
import image_functions

class Events(commands.Cog):
    """Handles Any Discord Events"""
    def __init__(self, bot):
        self.bot = bot
        self.responses = {
            'bye':'goodbye {0.author.mention}',
            'goodnight':'goodnight {0.author.mention}',
            'gn':'gn',
            'im hamood':"No you're not, im hamood {0.author.mention}",
            'marco':'polo {0.author.mention}',
            'im hamood':'No your not, im hamood!',
        }

        self.profanity_action = 1

        file = os.path.split(os.getcwd())[0] + '/' + os.path.split(os.getcwd())[1] + '/textFiles/errors.txt'
        self.error_solutions = message_functions.convert_to_dict(file)

    @commands.Cog.listener()
    async def on_message(self, message): 
        #checks again to make sure the bot does not reply to itself
        if message.author.id == self.bot.user.id:
            return

        try:
            nsfw = message.channel.is_nsfw()
        except Exception:
            nsfw = False

        profane, badword = message_functions.profCheck(message.content)
        
        if (profane):
            if ("hamood" in message.content):
                uno = image_functions.unoCard()
                await message.channel.send(file=discord.File(uno))
                await message.channel.send(f'{message.author.mention} No U!')
                return
            else:
                if not nsfw:
                    if len(badword) == 1:
                        punc = 'is a bad word'
                    else:
                        punc = 'are bad words'

                    badword = ', '.join(badword)

                    if (self.profanity_action == 2):
                        await message.channel.purge(limit=1)
                        await message.channel.send(f'**{message.author.mention} said: ||"{message.content}"||, ||"{badword}"|| {punc}, watch your profanity!**')
                    else:
                        await message.add_reaction('❌')
                        await message.channel.send(f'**{message.author.mention}, ||{badword}|| {punc}, watch your profanity!**')
                    return
    
        elif message.content.startswith("im"):
            await message.channel.send(f"hi {message.content[2:]}, im hamood")

        if message.content in self.responses:
            await message.channel.send(self.responses[message.content].format(message))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}!')


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have the permission to do that")
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                await ctx.send(self.error_solutions[str(ctx.command)])
            except Exception:
                print('error')
        #raise error

   

def setup(bot):
    bot.add_cog(Events(bot))  

