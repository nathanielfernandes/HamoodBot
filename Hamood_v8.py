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
#from random_word import RandomWords
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
#import scrapeImage
#import aiChat

from boto.s3.connection import S3Connection
s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])

TOKEN = os.environ['TOKEN']


if (platform.system() == 'Darwin'):
    running = 'macOS Catalina'
elif (platform.system() == 'Linux'):
    running = 'Raspberry pi 3B+'

path = os.path.dirname(os.path.realpath(__file__))


VR = "Hamood v8" 

#inv link
#https://discord.com/api/oauth2/authorize?client_id=699510311018823680&permissions=8&scope=bot

# Default Bot Stuff #
description = '''Hamood is ur freind'''

#i have no bot prefix which creates allot of errors in the console, however i clean it up. use a prefix if you want avoid these errors when not using the cleaner
bot = commands.Bot(command_prefix='')

#used for the vibecheck command
#r = RandomWords()

#used for dictionary purposes
dictionary = PyDictionary()

#gets current date and time
currentDT = datetime.datetime.now()

# 1 = warning message
# 2 = automatically deletes the message and shows warning message
profanity_action = 1

#runs on startup
@bot.event
async def on_ready():
# Setting 'Watching' status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with your feelings"))
    print('-------------------')
    print(('|Logged in as {0} ({0.id})|'.format(bot.user)))
    print("|" + str(currentDT) + '|')
    print('-------------------')
    print(VR)
    print('-------------------')


@bot.command(pass_context = True)
async def version(ctx):
    await ctx.send(('```md\n[' + VR + ' | ' + str(currentDT) + '](RUNNING ON: '+running+')```'))

#owner commands
#allows the owner to logout out the bot within discords
@bot.command(pass_context = True)
@commands.is_owner()
async def logout(ctx):
    await ctx.send("***goodbye***")
    await bot.logout()

#allows the owner of the bot to dm other users using the bot
#allows the owner of the bot to dm users that are in the same server as the bot, the format is "dm <discordtag> <message>"
@bot.command(pass_context = True)
@commands.is_owner()
async def dm(ctx, member: discord.Member, *, content: str):

    await member.send(content)
    print('Hamood#3840: ', end='')
    print(content)

    @bot.event
    async def on_message(message):
        user = message.author.id
        name = bot.get_user(user)

        if message.author.id == bot.user.id:
            return
        elif (str(name) == str(member)):
            print(str(name) + ": ", end='')
            print((message.content))
            
            await ctx.send(('{0.author.mention}: ' + str(message.content)).format(message))

        await bot.process_commands(message)


#removes errors from console
#ive setup the console to print out all sent and recieved messages to and from the bot, it removes errors to make the console less cluttered
# @bot.event
# async def on_command_error(ctx, error):
#     err = getattr(error, "original", error)

#     if isinstance(err, commands.CommandNotFound):
#         return


image_url = ''
image_channel = ''
#runs whenever a message is recieved by the bot
@bot.event
async def on_message(message): 

    currentDT = datetime.datetime.now()
    channel = message.channel.id
    channel = str(channel)

    user = message.author.id
    name = bot.get_user(user)

    print('|' + str(name) + ": ", end='')
    print((message.content), end='')
    print(' [' + str(currentDT) + '] |')

    #lowercases all messages received by the bot, unless it is a dm
    if ('dm' not  in message.content) and ('link' not  in message.content):
        message.content = message.content.lower().replace(' ', ' ')

    # we do not want the bot to reply to itself
    if message.author.id == bot.user.id:
        return

        #print(message.attachments)


    global image_url
    global image_channel

    attach = str(message.attachments)
    if ('.jpg' in attach) or ('.png' in attach) or ('.jpeg' in attach):
        start = attach.find('url=')
        image_url = (attach[start+5:-3])
        image_channel = channel
        


        #print(image_url)

        #aiChat
   # elif (channel == '706335537853628436'):
       # response = aiChat.chat(message.content)
       # await message.channel.send(response)
        #return
    #nsfw = message.channel.is_nsfw()
    profane, badword = profanityCheck.profCheck(message.content)
    
    if (profane):
        if ("hamood" in message.content):
            uno = noU.unoCard()
            await message.channel.purge(limit=1)
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

            if (profanity_action == 2):
                await message.channel.purge(limit=1)
                await message.channel.send(('***{0.author.mention} said: ||"'+message.content+'"||, ||"'+words+'"|| ' + punc +', watch your profanity!***').format(message))

            else:
                await message.add_reaction('❌')
                await message.channel.send(('***{0.author.mention}, ||'+words+'|| '+punc+', watch your profanity!***').format(message))
            return
        
    # if (str(message.author.id) == '558518137390235708'):
    #     await message.channel.purge(limit=1)
    #     #await message.channel.send('f u {0.author.mention}'.format(message))
    #     return

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

@bot.command(aliases=['inv'])
async def invite(ctx):
    """get the invite link for this bot"""
    await ctx.send('https://discord.com/api/oauth2/authorize?client_id=699510311018823680&permissions=8&scope=bot')


#below are bot commands that run when called
@bot.command(aliases=['newwordadd', 'newswear','newprof'])
@commands.is_owner()
async def newprofanity(ctx, *newWord:str):
    """lets you add a profane word to hamood's profanity list"""

    newWord = profanityCheck.profAdd(newWord)

    await ctx.send(("{0.author.mention} '||" + (newWord) + "||' was added to my profanity list").format(ctx))


@bot.command(aliases=['sign'])
async def zodiac(ctx, month1: str, day1: int, month2:str, day2: int, quick="slow"):

    sign1 = zodiacCheck.getZodiac(month1, day1)
    sign2 = zodiacCheck.getZodiac(month2, day2)
    
    if sign1 or sign2:
        await ctx.send("enter two dates in the format <mmm dd mmm dd>")
        return


    compatibility = zodiacCheck.getCompatibility(sign1, sign2)


    if (quick == "slow"):
        await ctx.send(("person 1 is a ***" + sign1 + "***, person 2 is a ***" + sign2 + "***, and they are about ***" + compatibility + "*** compatible").format(ctx))
    else:
        await ctx.send(('***' + sign1 + "*** and ***" + sign2 + "*** are about ***" + compatibility + "*** compatible").format(ctx))


@bot.command(aliases=['clear'], pass_context=True)
#@commands.has_role("Admin")
async def clean(ctx, amount=5):
    """deletes chat messages"""
    amount = int(amount)
    amount += 1
    
    await ctx.channel.purge(limit=amount)

#this tag command only works if there is a "IT" role
@bot.command(pass_context=True)
@commands.has_role("IT")
async def tag(ctx, member: discord.Member):
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

    

@bot.command()
@commands.is_owner()
async def status(ctx, aType: str, *aName: str):
    """changes hamoods status"""

    #aName = formatMsg.remove(aName, '(', ')', "'", ",")
    aName = formatMsg.convertList(aName, False) 

    if (aType== 'playing'):
        await bot.change_presence(activity=discord.Game(name=aName))
    #elif (aType == 'streaming'):
    #   await bot.change_presence(activity=discord.Streaming(name=aName, url=my_twitch_url))
    elif (aType == 'listening'):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=aName))
    elif (aType == 'watching'):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=aName))


@bot.command(aliases=['hello','hi','hey', 'yo'])
async def greet(ctx):
    """greets the user"""
    possible_responses = ['hello', 'hi', 'hey', "what's up"]

    await ctx.send((random.choice(possible_responses) + ' {0.author.mention}').format(ctx))


@bot.command()
async def hamood(ctx):
    """calls hamood"""    
    possible_responses = [
        'what do you want {0.author.mention}?',
        'what {0.author.mention}?',
        'huh?',
        'yeah {0.author.mention}?',
        'go away',
        'stop calling me',
        "what's up"
    ]

    await ctx.send(random.choice(possible_responses).format(ctx))


@bot.command(aliases=['coin'])
async def flip(ctx): 
    """flips a coin"""
    possible_responses = ['heads', 'tails']

    await ctx.send('***' + (random.choice(possible_responses) + '***, ' + '{0.author.mention}').format(ctx))



@bot.command()
async def pp(ctx):
    """returns your pp size"""
    size = '8'
    length =  ''
    randomSize = random.randint(0,50)
    for i in range(randomSize):
        length += '='
    size = size + length + 'D'

    await ctx.send(('{0.author.mention} :eggplant: size is ***' + size +'***').format(ctx))

         

@bot.command()
async def ping(ctx):
    """returns hamood's ping"""
 
    await ctx.send("```xl\n'"+ ('pong! {0}'.format(round(bot.latency, 1)) + "'```"))
        

@bot.command()
async def match(ctx, left: str, right: str):
    """match makes"""
    match = str(random.randint(0,100))
    
    await ctx.send('***' + left + '*** and ***' + right + '*** are ***' + match + '%*** compatible')
    
    

@bot.command(aliases=['+'])
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""

    await ctx.send(left + right)
         

@bot.command(aliases=['*'])
async def multiply(ctx, left: int, right: int):
    """multiplies two numbers together."""
    
    await ctx.send(left * right)
         

@bot.command(aliases=['-'])
async def subtract(ctx, left: int, right: int):
    """subtracts two numbers together."""

    await ctx.send(left - right)
         

@bot.command(aliases=['/'])
async def divide(ctx, left: int, right: int):
    """divides two numbers together."""

    await ctx.send(left / right)
         

@bot.command(aliases=['dice'])
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))

    await ctx.send(result)

         

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""

    await ctx.send(random.choice(choices))
         

@bot.command(aliases=["pop", "bubble"])
async def bubblewrap(ctx, w=3, h=3):
    """creates some bubble wrap"""
    if w > 14:
        w = 14
    if h > 14:
        h = 14
    wrap = ''
    w = "||***pop***||"*int(w)
    for i in range(h):
        wrap += w + "\n"

    await ctx.send(wrap)



@bot.command()
async def repeat(ctx, times: int, *content: str):
    """Repeats a message multiple times."""

    msg = ''
    #content = formatMsg.remove(content, '(', ')', "'", ",")
    content = formatMsg.convertList(content, False) 

    for i in range(times):
        msg += content + '\n'

    await ctx.send(msg)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""

    await ctx.send('```md\n# ' + ('{0.name} joined in {0.joined_at}'.format(member)) + ' #```')
         
        
@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:

        await ctx.send('no, {0.subcommand_passed} is not cool'.format(ctx))
             

@cool.command(name='nathan')
async def _bot(ctx):
    """Is the bot cool?"""

    await ctx.send('yes, nathan is cool.')
         

@bot.command(aliases= ['does','would','should','could','can','do','will','is','am i'])
async def answer(ctx):
    """answers your yes or no question"""

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
         




@bot.command()
async def vibecheck(ctx):
    """vibechecks you"""
    url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
    words = json.loads(url.read())
    random_word = random.choice(words)
    #possible_response = r.get_random_word()

    await ctx.send((('{0.author.mention}')+' your vibe checked out to be ' + "***'"+ (random_word)+ "'***").format(ctx))
    await ctx.message.add_reaction('✔️')
 
@bot.command(aliases=['def'])
async def define(ctx, word):
    """finds the definition of a word"""
    definition = dictionary.meaning(word)
    definition = formatMsg.remove(definition, "{", "}", "[", "]")

    await ctx.send(str(word) + ": " + str(definition))


#roast system
@bot.command(aliases=['roast me', 'roastme'])
async def roast(ctx):
    """roasts you"""

    roast = roastHandle.getRoast()

    await ctx.send(('{0.author.mention}  ' + roast).format(ctx))

         

@bot.command(aliases=['addroast', 'roastadd', 'roastnew'])
async def newroast(ctx, *roast:str):
    """lets you add a roast to hamood's list"""

    newRoast = roastHandle.addRoast(roast)

    await ctx.send(("{0.author.mention} '" + (newRoast) + "' was added to my list of roasts").format(ctx))


@bot.command(aliases=['roastlist'])
async def listroast(ctx):
    """lists the subreddits in its list"""
    list = open(r"C:\Users\natha\Desktop\Hamood Bot\roasts.txt","r",encoding='utf-8')
    list = list.readlines()
    await ctx.send(("roasts in list:").format(ctx))
    for line in list:
        await ctx.send((line).format(ctx))



#Reddit Stuff
#uses a reddit bot to find reddit posts
@bot.command(aliases=['reddit'])
async def red(ctx, redditSub='abc123'):
    """finds posts from reddit"""

    if (redditSub == "abc123"):
        redditSub = redditHandle.getSubReddit()
        
    post = redditHandle.findPost(redditSub)

    await ctx.send(("here's your post from the '" + redditSub + "' subreddit {0.author.mention}").format(ctx))
    await ctx.send(post.url)


@bot.command(aliases=['addreddit', 'redditadd', 'redditnew'])
async def newreddit(ctx, sub:str):
    """lets you add a subreddit to the list"""
    sub = redditHandle.addSubReddit(sub)

    await ctx.send(("{0.author.mention} '" + (sub) + "' was added to the subReddit list").format(ctx))

@bot.command(aliases=['redditlist'])
async def listreddit(ctx):
    """lists the subreddits in its list"""
    list = open(r"C:\Users\natha\Desktop\Hamood Bot\subreddits.txt","r",encoding='utf-8')
    list = list.readlines()
    await ctx.send(("subReddits in list:").format(ctx))
    for line in list:
        await ctx.send((line).format(ctx))


@bot.command(aliases=['memes'])
async def meme(ctx):
    """sends a meme"""
    post = redditHandle.findPost('memes')

    await ctx.send(("here's your meme {0.author.mention}").format(ctx))
    await ctx.send(post.url)


@bot.command(aliases=['cats', 'noura'])
async def cat(ctx):
    """sends a cat pic"""
    post = redditHandle.findPost('cats')

    await ctx.send(("here's your cat, {0.author.mention}").format(ctx))
    await ctx.send(post.url)
         

@bot.command(aliases=['curse'])
async def cursed(ctx):
    """finds posts from r/cursedimages"""
    post = redditHandle.findPost('cursedimages')

    await ctx.send(("here's your cursed image, {0.author.mention}").format(ctx))
    await ctx.send(post.url)


@bot.command(aliases=['blur'])
async def blursed(ctx):
    """finds posts from r/blursedimages"""
    post = redditHandle.findPost('blursedimages')

    await ctx.send(("here's your blursed image, {0.author.mention}").format(ctx))
    await ctx.send(post.url)


@bot.command(aliases=['bless'])
async def blessed(ctx):
    """finds posts from r/Blessed_Images"""
    post = redditHandle.findPost('Blessed_Images')

    await ctx.send(("here's your blessed image, {0.author.mention}").format(ctx))
    await ctx.send(post.url)      


@bot.command(aliases=['dark'])
async def darkhumor(ctx):
    """finds posts from r/DarkHumorAndMemes"""
    post = redditHandle.findPost('DarkHumorAndMemes')

    await ctx.send(("here's your dark meme, {0.author.mention}").format(ctx))
    await ctx.send(post.url)


@bot.command(aliases=['pizza', 'time', 'pizza time', 'ayan'])
async def pizzatime(ctx):
    """its pizza time!"""
    post = redditHandle.findPost('raimimemes')
   
    await ctx.send(("its pizza time, {0.author.mention}").format(ctx))
    await ctx.send(post.url)  


# @bot.command(aliases=['noura'])
# async def kitten(ctx):
#     """kitty"""
#     post = redditHandle.findPost('kittengifs')

#     await ctx.send(("heres a kitten").format(ctx))
#     await ctx.send(post.url)


@bot.command(aliases=["dogs", "doggy", "doge"])
async def dog(ctx):
    """dog"""
    post = redditHandle.findPost('dog')

    await ctx.send(("heres a dog").format(ctx))
    await ctx.send(post.url)

@bot.command()
async def spam(ctx, redditSub='random', amount='2'):
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


@bot.command()
async def google(ctx, *query:str):
    """googles an image"""
    #query = formatMsg.remove(query, '(', ')', "'", ",")
    query = formatMsg.convertList(query, False)
    image = imageSearch.ImgSearch(query)
    await ctx.send(file=discord.File(image))
    imageSearch.deleteImage(image)

@bot.command()
async def no(ctx, content:str):
    """no you"""
    if (content == 'u' or content == 'you'):
        await ctx.channel.purge(limit=1)
        uno = noU.unoCard()
        await ctx.send(file=discord.File(uno))

@bot.command(pass_context = True)
# #@commands.is_owner()
@commands.has_role("hackerman")
async def link(ctx, website, amount=1):
    await ctx.channel.purge(limit=1)
    for i in range(amount):
        webbrowser.open_new(website)

@bot.command()
async def send(ctx, mix=1):
    await ctx.channel.purge(limit=1)
    if mix <= 0:
        mix = 1
    content = getFile.getMedia(mix)
    await ctx.send(file=discord.File(content))

@bot.command(aliases=["movie time"])
async def shrek(ctx):
    await ctx.send("https://imgur.com/gallery/IsWDJWa")



pollOne = -1
pollTwo = -1

async def pollResults(time, channel, firstPoll, secondPoll):
    delete = True
    
    global pollOne
    global pollTwo

    await asyncio.sleep(time)
    await bot.wait_until_ready()

    #print('woo')
    #print(pollOne, pollTwo)
    totalPolls = pollOne + pollTwo

    percentOne = round((pollOne / totalPolls) * 100)
    percentTwo = round((pollTwo / totalPolls) * 100)

    difference = abs(percentOne - percentTwo)

    singleTick = "|||||"

    barOne = (singleTick*percentOne) + " " + str(percentOne) + "% | " + firstPoll + " | " 
    barTwo = (singleTick*percentTwo) + " " + str(percentTwo) + "% | " + secondPoll + " | " 

    if percentOne > percentTwo:
        result = '"' + firstPoll + '" won by ' + str(difference) + "% !"
    elif percentOne < percentTwo:
        result = '"' + secondPoll + '" won by ' + str(difference) + "% !"
    elif percentOne == percentTwo:
        result = "it's a tie!"

    await channel.send("the poll results are in:" + '\n' + barOne + '\n' + barTwo + '\n' + result)
    #await channel.send(barOne)
  #  await channel.send(barTwo)
    #await channel.send(result)

    pollOne = -1
    pollTwo = -1

    return delete


@bot.command(pass_context = True)
async def poll(ctx, time:int, *content:str):
    global pollOne
    global pollTwo

    pollOne = -1
    pollTwo = -1

    done = False
    channel = ctx.message.channel
    time *= 60

    # content = formatMsg.remove(content, '(', ')', "'", ",")

    # if 'vs.' not in content:
    #     return

    # split1 = (content.find('vs.')) - 1
    # split2 = split1 + 5

    # firstPoll = content[:split1]
    # secondPoll = content[split2:]

    content = formatMsg.convertList(content, True)
    firstPoll, secondPoll = content
    
    await ctx.send("Option 1: "+firstPoll + '\n' + "Option 2: "+secondPoll + '\n' + "@everyone VOTE!")
    #await ctx.send("Option 2: "+secondPoll)
    await ctx.message.add_reaction(":one:713819687036780544")
    await ctx.message.add_reaction(":two:713819703985963028")
    #await ctx.send("@everyone VOTE!")

    done = await pollResults(time, channel, firstPoll, secondPoll)
    if done:
        await ctx.message.delete()


@bot.event
async def on_raw_reaction_add(payload):
    global pollOne
    global pollTwo

    if payload.emoji.name == "one":
        pollOne += 1
    if payload.emoji.name == "two":
        pollTwo += 1

    #print(pollOne, pollTwo)
@bot.event
async def on_raw_reaction_remove(payload):
    global pollOne
    global pollTwo
    
    if payload.emoji.name == "one":
        pollOne -= 1
    if payload.emoji.name == "two":
        pollTwo -= 1


@bot.command(pass_context=True)
async def bonk(ctx, *content:str):
    content = formatMsg.convertList(content, True)
    nameOne, nameTwo = content

    meme = editPics.addText('bonkImage.jpg', 75, (0,0,0), nameOne, nameTwo, ' ', [250, 450], [1050, 600], [0,0], 'BONK.jpg')
    await ctx.send(file=discord.File(meme))
    editPics.deleteImage(meme)

@bot.command(pass_context=True)
async def lick(ctx, *content:str):
    content = formatMsg.convertList(content, True)
    nameOne, nameTwo = content

    meme = editPics.addText('lickImage.jpg', 35, (0,0,0), nameOne, nameTwo, ' ', [320, 220], [75, 200], [0,0], 'LICK.jpg')
    await ctx.send(file=discord.File(meme))
    editPics.deleteImage(meme)

@bot.command(pass_context=True)
async def slap(ctx, *content:str):
    content = formatMsg.convertList(content, True)
    nameOne, nameTwo = content

    meme = editPics.addText('slapImage.jpg', 60, (255,255, 255), nameOne, nameTwo, ' ', [580, 30], [220, 250], [0,0], 'SLAP.jpg')
    await ctx.send(file=discord.File(meme))
    editPics.deleteImage(meme)

@bot.command(pass_context=True)
async def lookback(ctx, *content:str):
    content = formatMsg.convertList(content, True)
    nameOne, nameTwo, nameThree = content
    
    meme = editPics.addText('lookBackImage.jpg', 45, (0,0,0), nameOne, nameTwo, nameThree, [120, 285], [360, 180], [525, 250], 'LOOKBACK.jpg')
    await ctx.send(file=discord.File(meme))
    editPics.deleteImage(meme)

@bot.command(pass_context=True)
async def worthless(ctx, *content:str):
    content = formatMsg.convertList(content, False)
    nameOne = content

    meme = editPics.addText('worthlessImage.jpg', 180, (0,0,0), nameOne, ' ', ' ', [300, 300], [0, 0], [0, 0], 'WORTHLESS.jpg')
    await ctx.send(file=discord.File(meme))
    editPics.deleteImage(meme)
# @bot.command(pass_context=True)
# async def drake(ctx, nameOne:str, nameTwo:str, nameThree:str):
#     meme = editPics.addText('drakeImage.jpg', 80, (0,0,0), nameOne, nameTwo, nameThree, [150, 525], [610, 250], [610, 850], 'DRAKE.jpg')
#     await ctx.send(file=discord.File(meme))
#     editPics.deleteImage(meme)


photo = ''
save = ''

def editorSetup(imgName, classifier, rotation, channel):
    global image_url
    global image_channel
    global path
    global photo
    global save

    if (image_channel == channel):
        try:
            editPics.deleteImage(photo)
            editPics.deleteImage(save)
        except Exception:
            print("couldn't delete!")

        name = editPics.randomNumber()
        name = str(name) + '.png'#"temporaryImage1.png"
        save = (path + '/' + "memePics" '/' + name)
        
        editPics.scrape(image_url, save)

        photo = editPics.addFilter(save, imgName, classifier, rotation)
    else:
        print('channel does not match!')  

    editPics.deleteImage(save)

    return photo
        

@bot.command(pass_context=True)
async def googly(ctx):
    photo = editorSetup('googlyEye.png', 'eyes', True, str(ctx.message.channel.id))
    await ctx.send(("here's your googlified image, {0.author.mention}").format(ctx))
    await ctx.send(file=discord.File(photo))
    editPics.deleteImage(photo)

@bot.command(pass_context=True)
async def clown(ctx):
    photo = editorSetup('clownFace.png', 'faces', False, str(ctx.message.channel.id))
    await ctx.send(("here's your clowned image, {0.author.mention}").format(ctx))
    await ctx.send(file=discord.File(photo))
    editPics.deleteImage(photo)

@bot.command(pass_context=True)
async def sadcat(ctx):
    photo = editorSetup('cryingCat.png', 'cats', False, str(ctx.message.channel.id))
    await ctx.send(("here's your sadcat image, {0.author.mention}").format(ctx))
    await ctx.send(file=discord.File(photo))
    editPics.deleteImage(photo)

@bot.command(pass_context=True)
async def test(ctx):
    retStr = str("```css\nThis is some colored Text```")
    await ctx.send(retStr)


    # global image_url
    # global image_channel
    # global path

    # global photo
    # global save

    

    # if (image_channel == currentChannel:

    #     try:
    #         editPics.deleteImage(photo)
    #         editPics.deleteImage(save)
    #     except Exception:
    #         print("couldn't delete!")

    #     name = editPics.randomNumber()
    #     name = str(name) + '.png'#"temporaryImage1.png"
    #     save = (path + '/' + "memePics" '/' + name)
        
    #     editPics.scrape(image_url, save)

    #     photo = editPics.addFilter(save, 'googlyEye.png', 'eyes', True)
        
    #     editPics.deleteImage(photo)
    #     editPics.deleteImage(save)
    # else:
    #     print('channel does not match!')



# photo2 = ''
# save2 = ''
# @bot.command(pass_context=True)
# async def clown(ctx):
#     global image_url
#     global image_channel
#     global path

#     global photo2
#     global save2

#     if (image_channel == str(ctx.message.channel.id)):
#         try:
#             editPics.deleteImage(photo2)
#             editPics.deleteImage(save2)
#         except Exception:
#             print("couldn't delete!")

#         name = editPics.randomNumber()
#         name = str(name) + '.png'#"temporaryImage1.png"
#         save2 = (path + '/' + "memePics" '/' + name)
        
#         editPics.scrape(image_url, save2)

#         photo2 = editPics.addFilter(save2, 'googlyEye.png', 'eyes', True)
#         await ctx.send(file=discord.File(photo2))
#         editPics.deleteImage(photo2)
#         editPics.deleteImage(save2)
#     else:
#         print('channel does not match!')



# # photo2 = ''
# # save2 = ''
# # @bot.command(pass_context=True)
# # async def clown(ctx):
# #     global image_url
# #     global path
# #     global photo2
# #     global save2

# #     try:
# #         editPics.deleteImage(photo2)
# #         editPics.deleteImage(save2)
# #     except Exception:
# #         print("couldn't delete!")

# #     name = editPics.randomNumber()
# #     name = str(name) + '.png'#"temporaryImage2.png"
# #     save2 = path + '/' + "memePics" '/' + name

# #     editPics.scrape(image_url, save2)

# #     photo2 = editPics.clownFace(save2)
# #     await ctx.send(file=discord.File(photo2))
# #     editPics.deleteImage(photo2)
# #     editPics.deleteImage(save2)


# photo3 = ''
# save3 = ''
# @bot.command(pass_context=True)
# async def sadcat(ctx):
#     global image_url
#     global path
#     global photo3
#     global save3

#     try:
#         editPics.deleteImage(photo3)
#         editPics.deleteImage(save3)
#     except Exception:
#         print("couldn't delete!")

#     name = editPics.randomNumber()
#     name = str(name) + '.png'#"temporaryImage2.png"
#     save3 = path + '/' + "memePics" '/' + name

#     editPics.scrape(image_url, save3)

#     photo3 = editPics.catFace(save3)
#     await ctx.send(file=discord.File(photo3))
#     editPics.deleteImage(photo3)
#     editPics.deleteImage(save3)


#bot.loop.create_task(bg_task())
bot.run(TOKEN)
