# Hamood

Hamood is a Discord bot written with [discord.py](https://github.com/Rapptz/discord.py) that has a variety of helpful and fun [functions](#Commands).

### Background
I decided to create Hamood as a fun qurantine project to learn new skills.
Hamood's name and profile picture is an inside joke based off the [Yotube](https://knowyourmeme.com/memes/yotube) kid meme.

## Highlight Features
### Covid-19 Statistics ``New!``
Hamood can send the latest Covid-19 statistics of any country from [worldometer](https://www.worldometers.info/coronavirus/).
### Automatic Profanity Dectection
Hamood calls out anyone that uses profane words
### Custom Text Generated Memes
You can generate custom memes with your own text with the meme templates Hamood has.
### Reddit Posts
Hamood can find and send posts from your favourite subreddits.

## Usage
### Public host
You can add Hamood to your discord server with this link [here](https://discord.com/api/oauth2/authorize?client_id=699510311018823680&permissions=8&scope=bot).
### Self-hosting
Grab the latest [files](https://github.com/nathanielfernandes/HamoodBot) and pip install Hamood's [dependancies](https://github.com/nathanielfernandes/HamoodBot/blob/master/requirements.txt) Then, create a Discord Bot Application [here](https://discord.com/developers/applications/) and create a [.env](https://pypi.org/project/python-dotenv/) file containing your Bot's Token. The discord.py [documentation](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html) can help with any issues.
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Feel free to create a fork and use the code for any noncommercial purposes.

## Commands
These commands are organized alphabetically from thier corresponding [Cog](https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html)
### About
- ``invite`` get the invite link for this bot
- ``github`` sends the link to Hamood's github repository
- ``version`` sends Hamood's current version
- ``ping`` returns hamood's ping
### Avatar Memes
- ``stonks [@user]`` adds a tagged discord avatar to the 'stonks' meme
- ``worthless [@user]`` adds a tagged discord avatar to the 'this is worthless' meme
- ``neat [@user]`` adds a tagged discord avatar to the 'this is pretty neat' meme
- ``grab [@user]`` adds a tagged discord avatar to the 'grab' meme
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
### Math
- ``add [number1] [number2]`` adds two numbers together
- ``multiply [number1] [number2]`` multiplies two numbers together
- ``subtract [number1] [number2]`` subtracts two numbers together
- ``divide [number1] [number2]`` divides two numbers together
### Mod
- ``kick [@user]`` kicks a tagged member
- ``ban [@user]`` bans a tagged member
- ``clean`` deletes chat messages
### Reddit
- ``red [subreddit]`` finds a post from your specified subreddit
- ``meme`` quickly sends a meme from r/meme
- ``cat`` quickly sends a cat from r/cats
- ``dog`` quickly sends a dog from r/dogs
- ``spam [subreddit] [amount]`` sends a number of posts from a specified subreddit (max=10)
### Text Memes
- ``bonk [text1], [text2]`` adds your own text to the 'bonk' meme format
- ``lick [text1], [text2]`` adds your own text to the 'lick' meme format
- ``slap [text1], [text2]`` adds your own text to the 'slap' meme format
- ``lookback[text1], [text2], [text3]`` adds your own text to the 'lookback' meme format
- ``our [text1], [text2]`` adds your own text to the 'our' meme format
- ``pour [text1], [text2]``adds your own text to the 'pour' meme format
### User
- ``joined [@user]`` says when a member joined the server
- ``avatar [@user]`` sends the profile picture of a tagged user
- ``roles [@user]`` lists the roles of a tagged user
- ``userinfo [@user]`` sends allot of server info on a user
### Web
- ``covid [country]`` gets the latest covid 19 statistics
- ``google [image]`` googles an image



