import os
import discord
from keep_alive import keep_alive
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

bot = commands.Bot(
    command_prefix="y!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    help_command=None
)
bot.author_id = 832264231617167381  # Change to your discord id!!!

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"{bot.command_prefix}help"))
menu = DefaultMenu('◀️', '▶️', '❌') # You can copy-paste any icons you want.
bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.green()) 

@bot.command(name='howmuchcmd')
async def b(ctx):
    await ctx.send(f'I have {len(bot.commands)}')

if __name__ == '__main__':
	for filename in os.listdir("cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"cogs.{filename[:-3]}")

keep_alive()  # Starts a webserver to be pinged.
token = os.environ['token']

bot.run(token)  # Starts the bot
