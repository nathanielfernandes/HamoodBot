#Hamood Bot#
#date 2020/05/2
#@author Nathaniel Fernandes

#dependancies
import os
import json
import urllib.request
import platform
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
import textwrap

#modules that i have made for some of hamood's functions
import imageSearch
import zodiacCheck
import redditSearch
import messageFeatures
import imageFeatures
import webScraping

#bot description
description = '''Hamood is ur freind'''

#the prefix the bot looks for before processing a message
bot = commands.Bot(command_prefix='', case_insensitive=True)

    
#Messaging cog that checks for profantiy and also provide some simple chat commands
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

    #allows the owner of hamood to temporarily change what actions hamood takes when someone uses profanity
    @commands.command()
    @commands.is_owner()
    async def proflevel(self, ctx, lvl:int):
        self.profanity_action = lvl
    
    #runs on any chat message
    @commands.Cog.listener()
    async def on_message(self, message): 
        #checks again to make sure the bot does not reply to itself
        if message.author.id == bot.user.id:
            return

        #gets the the channel and user that said the message
        channel = str(message.channel.id)
        user = message.author.id
        name = bot.get_user(user)

        #
        try:
            nsfw = message.channel.is_nsfw()
        except Exception:
            nsfw = False

        profane, badword = messageFeatures.profCheck(message.content)
        
        if (profane):
            if ("hamood" in message.content):
                uno = imageFeatures.unoCard()
                #await message.channel.purge(limit=1)
                await message.channel.send(file=discord.File(uno))
                await message.channel.send('{0.author.mention} No U!'.format(message))
                return
            else:
                if not nsfw:
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
        
    # @commands.command(aliases=['def'])
    # async def define(self, ctx, word):
    #     """finds the definition of a word"""
    #     definition = self.dictionary.meaning(word)
    #     definition = messageFeatures.remove(definition, "{", "}", "[", "]")
    #     await ctx.send(str(word) + ": " + str(definition))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}!'.format(member))

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
        member = ctx.author
        if self.last_member is None or self.last_member.id != member.id:
            await ctx.send(random.choice(possible_responses).format(ctx))
        else:
            await ctx.send(random.choice(possible_replies))
        self.last_member = member

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
        content = messageFeatures.convertList(content, False) 
        for i in range(times):
            msg += content + '\n'
        await ctx.send(msg)

    @commands.command()
    async def echo(self, ctx, *content: str):
        """echos a message."""
        content = messageFeatures.convertList(content, False) 
        times = random.randint(1,5)
        for i in range(times):
            await ctx.send(content)

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx):
        retStr = str("```css\nThis is some colored Text```")
        await ctx.send(retStr)


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.VERSION = "Hamood v11" 
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

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send("**goodbye**")
        await bot.logout()

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, aType: str, *aName: str):
        """changes hamoods status"""
        aName = messageFeatures.convertList(aName, False) 

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
        self.currentDT = datetime.datetime.now()
        await ctx.send(('```md\n[{} | {}](RUNNING ON: {})```').format(self.VERSION, self.currentDT, self.running))

    @commands.command()
    async def ping(self, ctx):
        """returns hamood's ping"""
        await ctx.send("```xl\n'"+ ('pong! {0}'.format(bot.latency) + "'```"))



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
        """sends the profile picture of a tagged user"""
        for a in avamember:
            userAvatarUrl = a.avatar_url
            await ctx.send(userAvatarUrl)




class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
        self.words = json.loads(self.url.read())

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
        """get your self sorted out"""
        houses = ['Gryffindor', 'Hufflepuff', 'Slytherin', 'Ravenclaw']
        house = random.choice(houses)
        await ctx.send(('{0.author.mention}, you belong to the **' + house + '** house!').format(ctx))

    @commands.command()
    async def vibecheck(self, ctx):
        """vibechecks you"""
        random_word = random.choice(self.words)
        await ctx.send((('{0.author.mention}')+' your vibe checked out to be ' + "**'"+ (random_word)+ "'**").format(ctx))
        await ctx.message.add_reaction('✔️')

    @commands.command()
    async def vibe(self, ctx):
        """vibechecks you but better"""
        random_word = random.choice(self.words)
        await ctx.send((('{0.author.mention}')+' your vibe checked out to be:').format(ctx))
        await textPrep(ctx, (random_word, ' '), 'random', 500, 'random', 100)
        await ctx.message.add_reaction('✔️')

    @commands.command(aliases=['roast me', 'roastme'])
    async def roast(self, ctx):
        """roasts you"""
        roast = messageFeatures.getRoast()
        await ctx.send(('{0.author.mention}  ' + roast).format(ctx))

    @commands.command(aliases=["pop", "bubble"])
    async def bubblewrap(self, ctx, w=3, h=3):
        """creates some bubble wrap"""
        if w > 12:
            w = 12
        if h > 12:
            h = 12
        wrap = ''
        w = "||pop||"*int(w)
        for i in range(h):
            wrap += w + "\n"
        await ctx.send(wrap)

    @commands.command(aliases=['sign'])
    async def zodiac(self, ctx, month1: str, day1: int, month2:str, day2: int, quick="slow"):
        """test your zodiac's compatibilty with another"""
        sign1 = zodiacCheck.getZodiac(month1, day1)
        sign2 = zodiacCheck.getZodiac(month2, day2)

        compatibility = zodiacCheck.getCompatibility(sign1, sign2)

        if (quick == "slow"):
            await ctx.send(("person 1 is a **{}**, person 2 is a **{}**, and they are about **{}** compatible").format(sign1, sign2, compatibility))
        else:
            await ctx.send(('**{}** and **{}** are about **{}** compatible').format(sign1, sign2, compatibility))

    @commands.command()
    async def match(self, ctx, *content: str):
        """match makes"""
        match = str(random.randint(0,100))
        content = messageFeatures.convertList(content, True) 
        left, right = content
        await ctx.send(('**{}** and **{}** are **{}%** compatible').format(left, right, match))




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
        rolls, limit = map(int, dice.split('d'))
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *content: str):
        """Chooses between multiple choices."""
        content = messageFeatures.convertList(content, True) 
        await ctx.send(random.choice(content))




class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        path = os.path.dirname(os.path.realpath(__file__))
        imageFeatures.deleteImage((path + '/' + 'tempImages' + '/' + "placeholder.txt"))

    @commands.command()
    async def google(self, ctx, *query:str):
        """googles an image"""
        query = messageFeatures.convertList(query, False)
        image = imageSearch.ImgSearch(query)
        await ctx.send("This is the first result for '" + query + "':")
        await ctx.send(file=discord.File(image))
        imageFeatures.deleteImage(image)

    @commands.command()
    async def no(self, ctx, content:str):
        """no you"""
        if (content == 'u' or content == 'you'):
            #await ctx.channel.purge(limit=1)
            uno = imageFeatures.unoCard()
            await ctx.send(file=discord.File(uno))

    @commands.command(aliases=["movie time"])
    async def shrek(self, ctx):
        """the entire shrek movie as a 90 min long gif"""
        await ctx.send("https://imgur.com/gallery/IsWDJWa")




async def redditPrep(ctx, subRedd):
    async with ctx.typing():
        post = redditSearch.findPost(subRedd)
    await ctx.send(post.url)

class RedditStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['reddit'])
    async def red(self, ctx, redditSub='abc123'):
        """finds posts from reddit"""
        if (redditSub == "abc123"):
            redditSub = redditSearch.getSubReddit()
        await ctx.send(("here's your post from the '" + redditSub + "' subreddit {0.author.mention}").format(ctx))
        await redditPrep(ctx, redditSub)

    @commands.command(aliases=['memes'])
    async def meme(self, ctx):
        """sends a meme"""
        await redditPrep(ctx, 'memes')

    @commands.command(aliases=['cats', 'noura'])
    async def cat(self, ctx):
        """sends a cat pic"""
        await redditPrep(ctx, 'cats')

    @commands.command(aliases=['curse'])
    async def cursed(self, ctx):
        """finds posts from r/cursedimages"""
        await redditPrep(ctx, 'cursedimages')

    @commands.command(aliases=['blur'])
    async def blursed(self, ctx):
        """finds posts from r/blursedimages"""
        await redditPrep(ctx, 'blursedimages')

    @commands.command(aliases=['bless'])
    async def blessed(self, ctx):
        """finds posts from r/Blessed_Images"""
        await redditPrep(ctx, 'Blessed_Images')

    @commands.command(aliases=['pizza', 'time', 'pizza time', 'ayan'])
    async def pizzatime(self, ctx):
        """its pizza time!"""
        await redditPrep(ctx, 'raimimemes')

    @commands.command(aliases=["dogs", "doggy", "doge"])
    async def dog(self, ctx):
        """sends a dog post"""
        await redditPrep(ctx, 'dog')

    @commands.command()
    async def spam(self, ctx, redditSub='random', amount='2'):
        """finds posts from reddit"""
        amount = int(amount)
        if amount > 10:
            amount = 10
        amount = int(amount)
        for i in range(amount):
            if (redditSub == "random"):
                redditSub = redditSearch.getSubReddit()
            await redditPrep(ctx, redditSub)



async def textMemePrep(ctx, text, coords, font, colour, source, wrap=12):
    async with ctx.typing():
        text = list(text)
        text.append(', ')
        text = messageFeatures.convertList(text, True)

        for i in range(len(text)):
            text[i] = textwrap.wrap(text[i], width=wrap)
            for a in range(len(text[i])):
                text[i][a] += '\n'
            text[i] = messageFeatures.convertList(text[i], False)

        for i in range(len(coords)):
            coords[i].append(text[i])
        
        name = imageFeatures.randomNumber()
        name = str(name) + '.jpg'

        meme = imageFeatures.addText(source, font, colour, coords, name)
        #await ctx.message.delete()
        await ctx.send(file=discord.File(meme))
        imageFeatures.deleteImage(meme)


class TextMemes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def bonk(self, ctx, *content:str):
        """give someone a good bonk"""
        await textMemePrep(ctx, content, [[(250,450)],[(1050,600)]], 75, 'BLACK', 'bonkImage.jpg')

    @commands.command()
    async def lick(self, ctx, *content:str):
        """lick someone tasty"""
        await textMemePrep(ctx, content, [[(320,220)],[(75,200)]], 35, 'BLACK', 'lickImage.jpg')

    @commands.command()
    async def slap(self, ctx, *content:str):
        """slap someone annoying"""
        await textMemePrep(ctx, content, [[(580, 30)],[(220, 250)]], 60, 'WHITE', 'slapImage.jpg')

    @commands.command()
    async def lookback(self, ctx, *content:str):
        """look back at it"""
        await textMemePrep(ctx, content, [[(120, 285)],[(360, 180)],[(525, 250)]], 30, 'BLACK', 'lookBackImage.jpg', 14)

    @commands.command()
    async def our(self, ctx, *content:str):
        """soviet bugs bunny"""
        content = list(content)
        content[0] = 'our ' + content[0]
        await textMemePrep(ctx, content, [[(325,320)], [(310,110)]], 45, 'BLACK', 'sovietImage.jpg')

    @commands.command()
    async def pour(self, ctx, *content:str):
        """pour yourself a nice drink"""
        await textMemePrep(ctx, content, [[(50,110)], [(430,60)]], 45, 'BLACK', 'coffeeImage.jpg', 8)





async def imagePrep(ctx, member, stuff, memeImage, size):
    path = os.path.dirname(os.path.realpath(__file__))

    async with ctx.typing():
        member = list(member)
        member.append(ctx.author)
        
        Urls = []
        for a in member:
            userAvatarUrl = str(a.avatar_url)
            userAvatarUrl = userAvatarUrl.replace('.webp', '.png')
            Urls.append(userAvatarUrl)

        for i in range(len(stuff)):
            stuff[i].append(Urls[i])
        
        for item in stuff:
            name = imageFeatures.randomNumber()
            name = str(name) + '.png'
            save = path + '/' + "tempImages" '/' + name
            webScraping.scrape(item[2], save)
            
            pos = stuff.index(item)
            stuff[pos][2] = save

        finalName = imageFeatures.randomNumber()
        finalName = str(finalName) + '.jpg'

        meme = imageFeatures.addImage(memeImage, stuff, size, finalName)
        
        for item in stuff:
            imageFeatures.deleteImage(item[2])
        
        #await ctx.message.delete()

        try:
            await ctx.send(file=discord.File(meme))
        except discord.Forbidden:
            print('could not send!')

        imageFeatures.deleteImage(meme)

class PfpMemes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def stonks(self, ctx, *avamember : discord.Member):
        """Stonks!"""
        await imagePrep(ctx, avamember, [[(65, 20), 0]], "stonksImage.jpg", (200,200))

    @commands.command()
    async def worthless(self, ctx, *avamember : discord.Member):
        """your worthless"""
        await imagePrep(ctx, avamember, [[(490, 235), -10]], "worthlessImage.jpg", (450,450))
            
    @commands.command()
    async def neat(self, ctx, *avamember : discord.Member):
        """your pretty neat ;)"""
        await imagePrep(ctx, avamember, [[(16, 210), 0]], "neatImage.jpg", (270,270))

    @commands.command()
    async def grab(self, ctx, *avamember : discord.Member):
        """GRAB"""
        await imagePrep(ctx, avamember, [[(25, 265), 0]], "grabImage.jpg", (150,150))



class Fonts(commands.Cog):

    @commands.command()
    async def arial(self, ctx, *content:str):
        """send a message in arial text"""
        await textPrep(ctx, content, 'arial', 500, 'black', 100)

    @commands.command(aliases=['craft'])
    async def minecraft(self, ctx, *content:str):
        """send a message in minecraft text"""
        await textPrep(ctx, content, 'minecraft', 500, 'yellow2', 100)

    @commands.command(aliases=['tale'])
    async def undertale(self, ctx, *content:str):
        """send a message in undertale text"""
        await textPrep(ctx, content, 'undertale', 500, 'white', 100)

    @commands.command(aliases=['rick'])
    async def morty(self, ctx, *content:str):
        """send a message in morty text"""
        await textPrep(ctx, content, 'morty', 500, 'green1', 100)

    @commands.command()
    async def gta(self, ctx, *content:str):
        """send a message in starwars text"""
        await textPrep(ctx, content, 'gta', 500, 'white', 100)

    @commands.command()
    async def enchant(self, ctx, *content:str):
        """send a message in enchant text"""
        await textPrep(ctx, content, 'enchant', 500, 'minecraft-enchantment.ttf', 100)

    @commands.command(aliases=['?'])
    async def unknown(self, ctx, *content:str):
        """send a message in unknown text"""
        await textPrep(ctx, content, 'unown.ttf', 500, 'black', 100)

    @commands.command(aliases=['poke'])
    async def pokemon(self, ctx, *content:str):
        """send a message in pokemon text"""
        await textPrep(ctx, content, 'pokemon', 500, 'steelblue2', 100)

    @commands.command(aliases=['sonic'])
    async def sega(self, ctx, *content:str):
        """send a message in sega text"""
        await textPrep(ctx, content, 'sega', 500, 'navy', 100)

    @commands.command(aliases=['sponge'])
    async def spongebob(self, ctx, *content:str):
        """send a message in spongebob text"""
        await textPrep(ctx, content, 'spongebob', 500, 'lightblue', 100)

    @commands.command()
    async def avenger(self, ctx, *content:str):
        """sends a message in avengers text"""
        await textPrep(ctx, content, 'avenger', 500, 'red4', 100)

    @commands.command()
    async def sketch(self, ctx, *content:str):
        """sends a message in avengers text"""
        await textPrep(ctx, content, 'sketch', 500, 'random', 100)

    @commands.command()
    async def batman(self, ctx, *content:str):
        """sends a message in avengers text"""
        await textPrep(ctx, content, 'batman', 500, 'black', 100)

    @commands.command()
    async def text(self, ctx, *content:str):
        """send a message in a random font"""
        await textPrep(ctx, content, 'random', 500, 'random', 100)

    @commands.command()
    async def font(self, ctx, font, colour, *content:str):
        """send a message in a selected font and colour"""
        await textPrep(ctx, content, font, 500, colour, 100)

async def textPrep(ctx, text, font, font_size, colour, wrap=80):
    async with ctx.typing():
        if text == ():
            return

        font = imageFeatures.getFont(font)
        
        colour = imageFeatures.getColour(colour)

        text = messageFeatures.convertList(text, False)
        text = [text]
        for i in range(len(text)):
            text[i] = textwrap.wrap(text[i], width=wrap)
            for a in range(1,len(text[i])):
                text[i][a] = '\n' + text[i][a]
            text[i] = messageFeatures.convertList(text[i], False)
        text = text[0]

        name = imageFeatures.randomNumber()
        name = str(name) + '.png'

        textImg = imageFeatures.makeText(text, font, font_size, colour, name)
        #await ctx.message.delete()
        await ctx.send(file=discord.File(textImg))
        imageFeatures.deleteImage(textImg)


class Statistics(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def covid(self, ctx, country=None):
        """gets the latest covid 19 statistics"""

        info = webScraping.covid_info(country)
        date = str(datetime.datetime.now())
        msg = ''
        for i, j in info.items():
            msg += i + ' : **' + j + '**' + '\n'
        
        if country == None:
            await ctx.send("As of **" + date[:10] + "**: \n" + msg)
        else:  
            await ctx.send("As of **" + date[:10] + "** in **" + str(country) + "**: \n" + msg)



class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        path = os.path.dirname(os.path.realpath(__file__))
        file = path + '/' + 'textFiles' + '/' + "errors.txt"

        self.error_solutions = messageFeatures.convert_to_dict(file)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        err = getattr(error, "original", error)
        if isinstance(err, commands.CommandNotFound):
            return
        
        try:
            await ctx.send(self.error_solutions[str(ctx.command)])
        except Exception:
            print('error')




bot.add_cog(Errors(bot))
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
bot.add_cog(Fonts(bot))
bot.add_cog(Statistics(bot))


TOKEN = os.environ['TOKEN']
bot.run(TOKEN)
