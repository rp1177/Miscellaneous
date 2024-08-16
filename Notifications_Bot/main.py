#import necessary libraries to communicate with discord client
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext import tasks
from cogs.general_commands import setup
from cogs.gmail_cog import setup_gmail


# Create a connection to Discord by creating an instance of a bot
load_dotenv()
TOKEN = os.getenv('INSERT_DISCORD_TOKEN')
GUILD = os.getenv('INSERT_DISCORD_GUILD')


#Set up permissions for bot (i.e. sending message contents and process commands from the cogs)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


#Turn the bot online and call the cog setups
@bot.event
async def on_ready():

    #Find guild information and id and print them
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)

    #Call bot ccogs for general and gmail related commands
    await setup(bot)
    await setup_gmail(bot)
    

    print(
        f'Bot successfully connected to Discord!\n'
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

# Happy birthday message (little test to understand basic message content stuff)
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

    #make sure bot commands are still processed.
    await bot.process_commands(message)

bot.run(TOKEN)
