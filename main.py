import os
import discord
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('ys '),  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents,
    help_command = None
)
bot.author_id = 832264231617167381  # Change to your discord id!!!

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"October go brrr"))

@bot.command(name='prefix')
async def pf(ctx):
  await ctx.reply(f'My prefix is {bot.command_prefix}')

@bot.command(name='sd')
async def sd(ctx):
  if ctx.author.id == bot.author_id:
    await bot.close()

@bot.command(name='nick')
async def nick(ctx,*,nick):
  await ctx.author.edit(nick=nick)
  await ctx.send('Changed! BTW did you know Discord has a / command  for this?')

@bot.command(name='invite',description='My invite link')
async def a(ctx):
    emb = discord.Embed(title='My invite link', description='Click [me](https://discord.com/api/oauth2/authorize?client_id=894953153160691722&permissions=8&scope=bot%20applications.commands)')
    await ctx.send(embed=emb)

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
