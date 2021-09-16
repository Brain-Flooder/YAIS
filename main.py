import os
import discord
from keep_alive import keep_alive
from discord.ext import commands
#print(discord.__version__)

bot = commands.Bot(
    command_prefix="y!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive

)

bot.author_id = 832264231617167381  # Change to your discord id!!!

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"))

extensions = [
    'cogs.commands',  # Same name as it would be if you were importing it
    #'cogs.help',
    #'cogs.ModerationCmd'
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ['token']

bot.run(token)  # Starts the bot
