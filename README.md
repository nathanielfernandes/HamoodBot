# Hamood

Hamood is a Discord bot written with [discord.py](https://github.com/Rapptz/discord.py) that has a variety of helpful and fun [functions](#Commands).

### Background
Hamood's name and profile picture is an inside joke based off the [Yotube](https://knowyourmeme.com/memes/yotube) kid meme.

## Highlighted Features
### Games ``New``
You can play games such as 2048, Chess, Connect Four, Filler, and Sokoban.
### Image Manipulation ``BETA``
You can now deepfry and edit images, more functionality comming soon!
### Quick Channels ``New``
Using the ``quickchannel`` command, you can add a quick channel system into your server that allows users to instantly create a temporary channel to talk to someone.
### Custom Text Generated Memes
You can generate custom memes with your own text with the meme templates Hamood has.
### Reddit Posts
Hamood can find and send posts from your favourite subreddits.
### Complex Math ``New``
Hamood has new and improved math functions that can help you with your homework.
### Chemistry ``NEW``
Hamood can now balance chemical equations as well has give info on compounds and elements.
### Python
Hamood can now run short python programs and send the output all within the chat.


## Usage
### Public host
You can add Hamood to your discord server with this link [here](https://discord.com/api/oauth2/authorize?client_id=699510311018823680&permissions=8&scope=bot).

<!--
### Self-hosting
Grab the latest [files](https://github.com/nathanielfernandes/HamoodBot) and pip install Hamood's [dependancies](https://github.com/nathanielfernandes/HamoodBot/blob/master/requirements.txt) Then, create a Discord Bot Application [here](https://discord.com/developers/applications/) and create a [.env](https://pypi.org/project/python-dotenv/) file containing your Bot's Token. The discord.py [documentation](https://discordpy.readthedocs.io/en/latest/index.html) can help with any issues. 
-->

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Feel free to create a fork and use the code for any noncommercial purposes.

## Commands
These commands are organized from thier corresponding [Cog](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html)
### Hamood's Prefix for the following commands is "``.``"
### Games
- ``2048`` starts a new 2048 game.
- ``connect [@opponent]`` starts a new connect 4 game
- ``filler [@oponent]`` lets you play filler with a tagged user
- ``sokoban`` play the clasic sokoban game using the emoji reactions. Inspired by [PolyMars](https://www.youtube.com/channel/UCl7dSJloxuCa9IBFml7sakw).
- ``chess [@opponent]`` starts a new chess game. Use .move to play `BETA`
- ``move [coordinate of peice] [coordinate to move peice to]`` can only be used if you are in a chess match!.

### Text Memes
- ``bonk [text1], [text2]`` adds your own text to the 'bonk' meme format
- ``lick [text1], [text2]`` adds your own text to the 'lick' meme format
- ``slap [text1], [text2]`` adds your own text to the 'slap' meme format
- ``lookback [text1], [text2], [text3]`` adds your own text to the 'lookback' meme format
- ``our [text1], [text2]`` adds your own text to the 'our' meme format
- ``pour [text1], [text2]`` adds your own text to the 'pour' meme format
- ``shoot [text1], [text2]`` shoot someone, among us style

### Avatarmemes
- ``stonks [@user]`` adds a tagged discord avatar to the 'stonks' meme
- ``worthless [@user]`` adds a tagged discord avatar to the 'this is worthless' meme
- ``neat [@user]`` adds a tagged discord avatar to the 'this is pretty neat' meme
- ``grab [@user]`` adds a tagged discord avatar to the 'grab' meme
- ``compare [@user1] [@user2]`` compares two users avatars

### Reddit
- ``reddit [subreddit]`` finds a post from your specified subreddit
- ``meme`` quickly sends a meme from r/meme
- ``cat`` quickly sends a cat from r/cats
- ``dog`` quickly sends a dog from r/dogs
- ``spam [subreddit] [amount]`` sends a number of posts from a specified subreddit (max=5)

### Pokemon
- ``pokedex [name or id]`` gets a pokemons info
- ``pokevibe [@user]`` finds the pokemon your vibing with
- ``pokepic [name or id]`` gets a pic of the pokemon

### Math
- ``base [number)base], [next base]`` base conversion from base 2-36, assumes 2's compliment for negative numbers in binary
- ``calc [equation]`` calculates the answer to a given equation
- ``derivative [nth derivative] [equation]`` solves for the nth dervative of an equation
- ``solve [equation]`` solves for variables in most math equations 
- ``graph [equation], [next equation]... optional([last equation]: (start -x to x))`` graphs most equations
- ``py [code]`` runs `python-3.7.2` code and outputs to the chat. Execution cannot exceed 1 second! Included Libraries: ``math, numpy, time, random``

### Chemistry
- ``balance [equation] ex. FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl`` balances chemical equations
- ``stoich [equation] ex. FeCl3 + NH4OH -> Fe(OH)3 + NH4Cl`` balances chemical equations and returns extra info
- ``molar [compound]`` returns the molar mass of the compound
- ``table [element symbol or number]`` returns a list of periodic information

### Mod
- ``kick [@user]`` kicks a tagged member
- ``ban [@user]`` bans a tagged member
- ``purge`` deletes chat messages
- ``clean [@user] [amount, max=50]`` deletes chat messages from a user
- ``prunes [days]`` returns how many roleless members have not been active on the server
- ``deprune [days]`` kicks all pruned members within given date
- ``nickname [@user] [newname]`` changes the nickname of a member
- ``quickcategory [category]`` Creates a '+' channel which instantly creates a quick voice channel for the user that joins it
- ``quickchannel [name]`` Creates a '+' voice channel that creates quick voice channel for the user that joins it
- ``fullcategory [category]`` Creates a text channel and a '+' voice channel under a category which instantly creates a quick voice channel for the user that joins it

### Chance
- ``eightball`` Hamood shakes his magic 8ball
- ``flip`` flips a coin
- ``roll [NdN]`` Rolls a dice in NdN format.
- ``choose [choice1], [choice2], [choice3]`` Chooses between multiple choices.

### Fonts
- ``text [msg]`` send a message in a random font
- ``font [font] [colour] [msg]`` send a message in a selected font and colour

### Fun
- ``pp`` returns your pp size
- ``sortinghat`` sorts you to one of the Hogwarts houses
- ``vibecheck`` vibechecks you
- ``vibe`` vibechecks you but better
- ``roast`` roasts/insults you
- ``bubblewrap [height] [width]`` makes bubblewrap
- ``zodiac [mmm] [dd] [mmm] [dd]`` lets you test your zodiac's compatibilty with another
- ``match [person1] [person2]`` randomly gives a match percentage between two people

### General
- ``greet`` greets the user
- ``hamood`` calls hamood
- ``clap [msg]`` adds clap emojis to your sentence
- ``repeat [msg]`` repeats your message multiple times 
- ``echo [msg]`` echos your message a random amount of times
- ``no u`` sends an uno reverse card
- ``shrek`` sends the entire shrek movie as a 90 min long gif
- ``poll [option1], [option2]..., [option6]`` create a poll with 2-6 options
- ``clown [msg]`` clown someones text
- ``lengthen [sentence]`` makes words long
- ``nnn`` dont nut
### User
- ``joined [@user]`` says when a member joined the server
- ``avatar [@user]`` sends the profile picture of a tagged user
- ``roles [@user]`` lists the roles of a tagged user
- ``userinfo [@user]`` sends allot of server info on a user
- ``listening [@user]`` returns a users spotify listening activity

### Web
- ``covid [country]`` gets the latest covid 19 statistics

### About
- ``info`` get some background information on Hamood
- ``invite`` get the invite link for this bot
- ``version`` sends Hamood's current version
- ``ping`` returns hamood's ping

<!-- ## Screenshots
![level1](https://cdn.discordapp.com/attachments/699770186227646465/741028512609206282/unknown.png)
![level2](https://cdn.discordapp.com/attachments/699770186227646465/741038530767093821/unknown.png)
![level3](https://cdn.discordapp.com/attachments/699770186227646465/741028185029738627/unknown.png)
![level4](https://cdn.discordapp.com/attachments/699770186227646465/741038792810430545/unknown.png) -->
