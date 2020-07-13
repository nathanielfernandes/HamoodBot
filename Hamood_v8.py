#This program is discord bot named "Hamood"
#date 2020/05/2
#@author Nathaniel Fernandes

#you need to pip install a few of these 
import os
import json
import urllib.request
import platform
import webbrowser
import datetime
import random
import math
import praw
import asyncio
import functools
import itertools
import discord
from discord.ext import commands
from async_timeout import timeout
from discord.utils import get
from functools import partial
from itertools import cycle
from random import shuffle
from PyDictionary import PyDictionary


#Hamood's modules
import getFile
import noU
import imageSearch
import zodiacCheck
import formatMsg
import roastHandle
import redditHandle
import profanityCheck
import editPics

description = '''Hamood is ur freind'''

bot = commands.Bot(command_prefix='')


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.VERSION = "Hamood v9" 
        self.currentDT = str(datetime.datetime.now())

        if (platform.system() == 'Darwin'):
            self.running = 'macOS Catalina'
        elif (platform.system() == 'Linux'):
            self.running = 'Heroku Linux'

    @commands.Cog.listener()
    async def on_ready(self):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with your feelings"))
        print('-------------------')
        print(('|Logged in as {0} ({0.id})|'.format(bot.user)))
        print("|" + self.currentDT + '|')
        print('-------------------')
        print(self.VERSION)
        print('-------------------')

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     err = getattr(error, "original", error)
    #     if isinstance(err, commands.CommandNotFound):
    #         return

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send("**goodbye**")
        await bot.logout()

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, aType: str, *aName: str):
        """changes hamoods status"""
        aName = formatMsg.convertList(aName, False) 

        if (aType== 'playing'):
            await bot.change_presence(activity=discord.Game(name=aName))
        elif (aType == 'listening'):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=aName))
        elif (aType == 'watching'):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=aName))
        #elif (aType == 'streaming'):
        #   await bot.change_presence(activity=discord.Streaming(name=aName, url=my_twitch_url))

    @commands.command(aliases=['inv'])
    async def invite(self, ctx):
        """get the invite link for this bot"""
        await ctx.send('https://discord.com/api/oauth2/authorize?client_id=699510311018823680&permissions=8&scope=bot')

    @commands.command()
    async def version(self, ctx):
        """sends Hamood's current version"""
        await ctx.send(('```md\n[' + self.VERSION + ' | ' + self.currentDT + '](RUNNING ON: '+self.running+')```'))

    @commands.command(aliases=['newwordadd', 'newswear','newprof'])
    @commands.is_owner()
    async def newprofanity(self, ctx, *newWord:str):
        """lets you add a profane word to hamood's profanity list"""
        newWord = profanityCheck.profAdd(newWord)
        await ctx.send(("{0.author.mention} '||" + (newWord) + "||' was added to my profanity list").format(ctx))

    @commands.command()
    async def ping(self, ctx):
        """returns hamood's ping"""
        await ctx.send("```xl\n'"+ ('pong! {0}'.format(bot.latency) + "'```"))

    @commands.command(aliases=['addroast', 'roastadd', 'roastnew'])
    @commands.is_owner()
    async def newroast(self, ctx, *roast:str):
        """lets you add a roast to hamood's list"""

        newRoast = roastHandle.addRoast(roast)
        await ctx.send(("{0.author.mention} '" + (newRoast) + "' was added to my list of roasts").format(ctx))

    @commands.command(aliases=['roastlist'])
    @commands.is_owner()
    async def listroast(self, ctx):
        """lists the subreddits in its list"""
        list = open(r"C:\Users\natha\Desktop\Hamood Bot\roasts.txt","r",encoding='utf-8')
        list = list.readlines()
        await ctx.send(("roasts in list:").format(ctx))
        for line in list:
            await ctx.send((line).format(ctx))




class Messaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

        self.member = None
        self.name = None
        self.user = None

        # 1 = warning message
        # 2 = automatically deletes the message and shows warning message
        self.profanity_action = 1
        self.dictionary = PyDictionary()

    @commands.command()
    @commands.is_owner()
    async def proflevel(self, ctx, lvl:int):
        self.profanity_action = lvl

    @commands.Cog.listener()
    async def on_message(self, message): 
        channel = message.channel.id
        channel = str(channel)
        user = message.author.id
        name = bot.get_user(user)

        #lowercases all messages received by the bot, unless it is a dm
        if ('dm' not in message.content):
            message.content = message.content.lower().replace(' ', ' ')
        # we do not want the bot to reply to itself
        if message.author.id == bot.user.id:
            return
        #nsfw = message.channel.is_nsfw()
        profane, badword = profanityCheck.profCheck(message.content)
        
        if (profane):
            if ("hamood" in message.content):
                uno = noU.unoCard()
                #await message.channel.purge(limit=1)
                await message.channel.send(file=discord.File(uno))
                await message.channel.send('{0.author.mention} No U!'.format(message))
                return
            else:
                #if not nsfw:
                if len(badword) == 1:
                    punc = 'is a bad word'
                else:
                    punc = 'are bad words'
                words = ''
                for word in badword:
                    words += word + ', '

                if (self.profanity_action == 2):
                    await message.channel.purge(limit=1)
                    await message.channel.send(('**{0.author.mention} said: ||"'+message.content+'"||, ||"'+words+'"|| ' + punc +', watch your profanity!**').format(message))
                else:
                    await message.add_reaction('❌')
                    await message.channel.send(('**{0.author.mention}, ||'+words+'|| '+punc+', watch your profanity!**').format(message))
                return

        elif message.content.startswith('bye'):
            await message.channel.send('goodbye {0.author.mention}'.format(message))

        elif message.content.startswith('gn'): 
            await message.channel.send('goodnight {0.author.mention}'.format(message))

        elif message.content.startswith('goodnight'): 
            await message.channel.send('goodnight {0.author.mention}'.format(message))

        elif (message.content == ('dang')):
            await message.channel.send('{0.author.mention} you called?'.format(message))
        
        elif message.content.startswith("im hamood"):
            await message.channel.send("No you're not, im hamood")
        
        elif message.content.startswith("im"):
            name = message.content[2:]
            await message.channel.send("hi" + name + ", im hamood")
            
        elif message.content.startswith("marco"):
            await message.channel.send("polo")
        
        await bot.process_commands(message)

    @commands.command(aliases=['def'])
    async def define(self, ctx, word):
        """finds the definition of a word"""
        definition = self.dictionary.meaning(word)
        definition = formatMsg.remove(definition, "{", "}", "[", "]")
        await ctx.send(str(word) + ": " + str(definition))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}!'.format(member))

    # @commands.command()
    # @commands.is_owner()
    # async def dm(self, ctx, member: discord.Member, *, content: str):
    #     self.member = member
    #     await member.send(content)

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     self.user = message.author.id
    #     self.name = bot.get_user(self.user)

    #     if message.author.id == bot.user.id:
    #         return
    #     elif (str(self.name) == str(self.member)):
    #         await ctx.send(('{0.author.mention}: ' + str(message.content)).format(message))
    #     await bot.process_commands(message)

    @commands.command(aliases=['clear'])
    async def clean(self, ctx, amount=3):
        """deletes chat messages"""
        amount = int(amount) + 1
        if amount > 20:
            amount = 20
        await ctx.channel.purge(limit=amount)

    @commands.command(aliases=['hello','hi','hey', 'yo'])
    async def greet(self, ctx):
        """greets the user"""
        possible_responses = ['hello', 'hi', 'hey', "what's up"]
        await ctx.send((random.choice(possible_responses) + ' {0.author.mention}').format(ctx))

    @commands.command()
    async def hamood(self, ctx):
        """calls hamood"""    
        possible_responses = [
            'what do you want {0.author.mention}?',
            'what {0.author.mention}?',
            'huh?',
            'yeah {0.author.mention}?',
            "what's up"]
        possible_replies = ["go away", "stop calling me"]
        #member = member or ctx.author
        #if self.last_member is None or self.last_member.id != member.id:
        await ctx.send(random.choice(possible_responses).format(ctx))
        #else:
            #await ctx.send(random.choice(possible_replies).format(ctx))
        #self.last_member = member

    @commands.command()
    async def clap(self, ctx, *content:str):
        """claps ur sentence"""
        msg = ''
        for word in content:
            msg += '**' + word + '**' + ':clap:'
        await ctx.send(msg)

    @commands.command()
    async def repeat(self, ctx, times: int, *content: str):
        """Repeats a message multiple times."""
        msg = ''
        content = formatMsg.convertList(content, False) 
        for i in range(times):
            msg += content + '\n'
        await ctx.send(msg)

    @commands.command()
    async def echo(self, ctx, *content: str):
        """echos a message."""
        content = formatMsg.convertList(content, False) 
        times = random.randint(1,5)
        for i in range(times):
            await ctx.send(content)

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        retStr = str("```css\nThis is some colored Text```")
        await ctx.send(retStr)




class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['+'])
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.send('**' + str(left + right) + '**')
            
    @commands.command(aliases=['*'])
    async def multiply(self, ctx, left: int, right: int):
        """multiplies two numbers together."""
        await ctx.send('**' + str(left * right) + '**')

    @commands.command(aliases=['-'])
    async def subtract(self, ctx, left: int, right: int):
        """subtracts two numbers together."""
        await ctx.send('**' + str(left - right) + '**')

    @commands.command(aliases=['/'])
    async def divide(self, ctx, left: int, right: int):
        """divides two numbers together."""
        await ctx.send('**' + (left / right) + '**')




class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined the server"""
        await ctx.send('```md\n# ' + ('{0.name} joined in {0.joined_at}'.format(member)) + ' #```')

    @commands.command()
    async def avatar(self, ctx, *avamember : discord.Member):
        for a in avamember:
            userAvatarUrl = a.avatar_url
            await ctx.send(userAvatarUrl)




class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("IT")
    async def tag(self, ctx, member: discord.Member):
        """tags a user"""
        victim = member
        user = ctx.message.author

        if str(victim) == 'Hamood#3840':
            await ctx.send(("{0.author.mention}, im on time out").format(ctx))
        elif (str(victim) == str(user)):
            await ctx.send(("{0.author.mention}, you can't tag yourself").format(ctx))
        else:
            await user.remove_roles(discord.utils.get(user.guild.roles, name='IT'))
            await victim.add_roles(discord.utils.get(victim.guild.roles, name='IT'))
            await ctx.send((f"{member} is now it!").format(ctx))

    @commands.command()
    async def pp(self, ctx):
        """returns your pp size"""
        size = '8'
        length =  ''
        randomSize = random.randint(0,50)
        for i in range(randomSize):
            length += '='
        size = size + length + 'D'
        await ctx.send(('{0.author.mention} :eggplant: size is **' + size +'**').format(ctx))

    @commands.command()
    async def sortinghat(self, ctx):
        houses = ['Gryffindor', 'Hufflepuff', 'Slytherin', 'Ravenclaw']
        house = random.choice(houses)
        await ctx.send(('{0.author.mention}, you belong to the **' + house + '** house!').format(ctx))

    @commands.command()
    async def vibecheck(self, ctx):
        """vibechecks you"""
        url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
        words = json.loads(url.read())
        random_word = random.choice(words)
        await ctx.send((('{0.author.mention}')+' your vibe checked out to be ' + "**'"+ (random_word)+ "'**").format(ctx))
        await ctx.message.add_reaction('✔️')

    @commands.command(aliases=['roast me', 'roastme'])
    async def roast(self, ctx):
        """roasts you"""
        roast = roastHandle.getRoast()
        await ctx.send(('{0.author.mention}  ' + roast).format(ctx))

    @commands.command(aliases=["pop", "bubble"])
    async def bubblewrap(self, ctx, w=3, h=3):
        """creates some bubble wrap"""
        if w > 14:
            w = 14
        if h > 14:
            h = 14
        wrap = ''
        w = "||**pop**||"*int(w)
        for i in range(h):
            wrap += w + "\n"
        await ctx.send(wrap)

    @commands.command(aliases=['sign'])
    async def zodiac(self, ctx, month1: str, day1: int, month2:str, day2: int, quick="slow"):
        sign1 = zodiacCheck.getZodiac(month1, day1)
        sign2 = zodiacCheck.getZodiac(month2, day2)
        
        if (sign1 == True) or (sign2 == True):
            await ctx.send("enter two dates in the format <mmm dd mmm dd>")
            return

        compatibility = zodiacCheck.getCompatibility(sign1, sign2)

        if (quick == "slow"):
            await ctx.send(("person 1 is a **" + sign1 + "**, person 2 is a **" + sign2 + "**, and they are about **" + compatibility + "** compatible").format(ctx))
        else:
            await ctx.send(('**' + sign1 + "** and **" + sign2 + "** are about **" + compatibility + "** compatible").format(ctx))

    @commands.command()
    async def match(self, ctx, *content: str):
        """match makes"""
        match = str(random.randint(0,100))
        content = formatMsg.convertList(content, True) 
        left, right = content
        await ctx.send('**' + left + '** and **' + right + '** are **' + match + '%** compatible')




class Chance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases= ['8ball','does','would','should','could','can','do','will','is','am i'])
    async def eightball(self, ctx):
        """Hamood shakes his magic 8ball"""
        possible_responses = [
            "hell naw",
            "i highley doubt it",
            "how am i supposed to know",
            "i guess its possible",
            "fo sho",
            "maybe",
            "stop asking",
            "yeah",
            "nah",
            "i dont care",
            "ofcourse",
            "not really"
            ]
        await ctx.send((random.choice(possible_responses) + ', ' + '{0.author.mention}'.format(ctx)))

    @commands.command(aliases=['coin'])
    async def flip(self, ctx): 
        """flips a coin"""
        possible_responses = ['heads', 'tails']
        await ctx.send('**' + (random.choice(possible_responses) + '**, ' + '{0.author.mention}').format(ctx))

    @commands.command(aliases=['dice'])
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *content: str):
        """Chooses between multiple choices."""
        content = formatMsg.convertList(content, True) 
        await ctx.send(random.choice(content))




class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def google(self, ctx, *query:str):
        """googles an image"""
        query = formatMsg.convertList(query, False)
        image = imageSearch.ImgSearch(query)
        await ctx.send("This is the first result for '" + query + "':")
        await ctx.send(file=discord.File(image))
        imageSearch.deleteImage(image)

    @commands.command()
    async def no(self, ctx, content:str):
        """no you"""
        if (content == 'u' or content == 'you'):
            #await ctx.channel.purge(limit=1)
            uno = noU.unoCard()
            await ctx.send(file=discord.File(uno))

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx, mix=1):
        """sends something special ;)"""
        await ctx.channel.purge(limit=1)
        if mix <= 0:
            mix = 1
        content = getFile.getMedia(mix)
        await ctx.send(file=discord.File(content))

    @commands.command(aliases=["movie time"])
    async def shrek(self, ctx):
        await ctx.send("https://imgur.com/gallery/IsWDJWa")




class RedditStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['reddit'])
    async def red(self, ctx, redditSub='abc123'):
        """finds posts from reddit"""
        if (redditSub == "abc123"):
            redditSub = redditHandle.getSubReddit()
        post = redditHandle.findPost(redditSub)
        await ctx.send(("here's your post from the '" + redditSub + "' subreddit {0.author.mention}").format(ctx))
        await ctx.send(post.url)


    @commands.command(aliases=['addreddit', 'redditadd', 'redditnew'])
    @commands.is_owner()
    async def newreddit(self, ctx, sub:str):
        """lets you add a subreddit to the list"""
        sub = redditHandle.addSubReddit(sub)
        await ctx.send(("{0.author.mention} '" + (sub) + "' was added to the subReddit list").format(ctx))

    @commands.command(aliases=['redditlist'])
    @commands.is_owner()
    async def listreddit(self, ctx):
        """lists the subreddits in its list"""
        list = open(r"C:\Users\natha\Desktop\Hamood Bot\subreddits.txt","r",encoding='utf-8')
        list = list.readlines()
        await ctx.send(("subReddits in list:").format(ctx))
        for line in list:
            await ctx.send((line).format(ctx))

    @commands.command(aliases=['memes'])
    async def meme(self, ctx):
        """sends a meme"""
        post = redditHandle.findPost('memes')
        await ctx.send(("here's your meme {0.author.mention}").format(ctx))
        await ctx.send(post.url)

    @commands.command(aliases=['cats', 'noura'])
    async def cat(self, ctx):
        """sends a cat pic"""
        post = redditHandle.findPost('cats')
        await ctx.send(("here's your cat, {0.author.mention}").format(ctx))
        await ctx.send(post.url)   

    @commands.command(aliases=['curse'])
    async def cursed(self, ctx):
        """finds posts from r/cursedimages"""
        post = redditHandle.findPost('cursedimages')
        await ctx.send(("here's your cursed image, {0.author.mention}").format(ctx))
        await ctx.send(post.url)

    @commands.command(aliases=['blur'])
    async def blursed(self, ctx):
        """finds posts from r/blursedimages"""
        post = redditHandle.findPost('blursedimages')
        await ctx.send(("here's your blursed image, {0.author.mention}").format(ctx))
        await ctx.send(post.url)

    @commands.command(aliases=['bless'])
    async def blessed(self, ctx):
        """finds posts from r/Blessed_Images"""
        post = redditHandle.findPost('Blessed_Images')
        await ctx.send(("here's your blessed image, {0.author.mention}").format(ctx))
        await ctx.send(post.url)      

    @commands.command(aliases=['dark'])
    async def darkhumor(self, ctx):
        """finds posts from r/DarkHumorAndMemes"""
        post = redditHandle.findPost('DarkHumorAndMemes')
        await ctx.send(("here's your dark meme, {0.author.mention}").format(ctx))
        await ctx.send(post.url)

    @commands.command(aliases=['pizza', 'time', 'pizza time', 'ayan'])
    async def pizzatime(self, ctx):
        """its pizza time!"""
        post = redditHandle.findPost('raimimemes')
        await ctx.send(("its pizza time, {0.author.mention}").format(ctx))
        await ctx.send(post.url)  

    @commands.command(aliases=["dogs", "doggy", "doge"])
    async def dog(self, ctx):
        """dog"""
        post = redditHandle.findPost('dog')
        await ctx.send(("heres a dog").format(ctx))
        await ctx.send(post.url)

    @commands.command()
    async def spam(self, ctx, redditSub='random', amount='2'):
        """finds posts from reddit"""
        amount = int(amount)
        if amount > 10:
            amount = 10
        amount = int(amount)
        for i in range(amount):
            if (redditSub == "random"):
                redditSub = redditHandle.getSubReddit()

            post = redditHandle.findPost(redditSub)
            
            await ctx.send(("here's your post from the '" + redditSub + "' subreddit {0.author.mention}").format(ctx))
            await ctx.send(post.url)



class TextMemes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def bonk(self, ctx, *content:str):
        content = formatMsg.convertList(content, True)
        nameOne, nameTwo = content
        content = [[nameOne, (250, 450)], [nameTwo, (1050, 600)]]
        
        meme = editPics.addText('bonkImage.jpg', 75, (0,0,0), content, 'BONK.jpg')
        await ctx.send(file=discord.File(meme))
        editPics.deleteImage(meme)

    @commands.command()
    async def lick(self, ctx, *content:str):
        content = formatMsg.convertList(content, True)
        nameOne, nameTwo = content
        content = [[nameOne, (320,220)], [nameTwo, (75,200)]]

        meme = editPics.addText('lickImage.jpg', 35, (0,0,0), content, 'LICK.jpg')
        await ctx.send(file=discord.File(meme))
        editPics.deleteImage(meme)

    @commands.command()
    async def slap(self, ctx, *content:str):
        content = formatMsg.convertList(content, True)
        nameOne, nameTwo = content
        content = [[nameOne, (580, 30)], [nameTwo, (220, 250)]]

        meme = editPics.addText('slapImage.jpg', 60, (255,255, 255), content, 'SLAP.jpg')
        await ctx.send(file=discord.File(meme))
        editPics.deleteImage(meme)

    @commands.command()
    async def lookback(self, ctx, *content:str):
        content = formatMsg.convertList(content, True)
        nameOne, nameTwo, nameThree = content
        content = [[nameOne, (120, 285)], [nameTwo, (360, 180)], [nameThree, (525, 250)]]
        
        meme = editPics.addText('lookBackImage.jpg', 45, (0,0,0), content, 'LOOKBACK.jpg')
        await ctx.send(file=discord.File(meme))
        editPics.deleteImage(meme)

    @commands.command()
    async def worthless(self, ctx, *content:str):
        content = formatMsg.convertList(content, False)
        nameOne = content
        content = [[nameOne, (300, 320)]]

        meme = editPics.addText('worthlessImage.jpg', 180, (0,0,0), content, 'WORTHLESS.jpg')
        await ctx.send(file=discord.File(meme))
        editPics.deleteImage(meme)




class PfpMemes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = os.path.dirname(os.path.realpath(__file__))

    def imagePrep(stuff, memeImage, size, finalName):
        for item in stuff:
            name = editPics.randomNumber()
            name = str(name) + '.png'
            save = self.path + '/' + "memePics" '/' + name
            item[0]
            editPics.scrape(item[0], save)
            
            pos = stuff.index(item)
            stuff[pos][0] = save

        meme = editPics.addImage(memeImage, stuff, size, finalName)
        
        for item in stuff:
            editPics.deleteImage(item[0])
        return meme

    @commands.command()
    async def stonks(self, ctx, *avamember : discord.Member):
        avatarUrls = []
        for a in avamember:
            userAvatarUrl = str(a.avatar_url)
            userAvatarUrl = userAvatarUrl.replace('.webp', '.png')
            avatarUrls.append(userAvatarUrl)
        
        first = avatarUrls[0]
        content = [[first, (65, 20)]]

        img = PfpMemes.imagePrep(content, "stonksImage.jpg", (200,200), "STONKS.jpg")

        await ctx.send(file=discord.File(img))
        editPics.deleteImage(img)
            

bot.add_cog(Config(bot))
bot.add_cog(Messaging(bot))
bot.add_cog(Math(bot))
bot.add_cog(Member(bot))
bot.add_cog(Fun(bot))
bot.add_cog(Chance(bot))
bot.add_cog(Images(bot))
bot.add_cog(RedditStuff(bot))
bot.add_cog(TextMemes(bot))
bot.add_cog(PfpMemes(bot))

TOKEN = os.environ['TOKEN']
#bot.loop.create_task(bg_task())
bot.run(TOKEN)
