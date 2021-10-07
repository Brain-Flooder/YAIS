import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions, CheckFailure, CommandNotFound, NotOwner, MissingRequiredArgument
import time


class OnCommandErrorCog(commands.Cog, name="on command error"):
  def __init__(self, bot:commands.Bot):
    self.bot = bot
        
  @commands.Cog.listener()
  async def on_command_error(self, ctx:commands.Context, error:commands.CommandError):
    if isinstance(error, commands.CommandOnCooldown):
      day = round(error.retry_after/86400)
      hour = round(error.retry_after/3600)
      minute = round(error.retry_after/60)
      if day > 0:
        await ctx.send('This command has a cooldown, for '+str(day)+ "day(s)")
      elif hour > 0:
        await ctx.send('This command has a cooldown, for '+str(hour)+ " hour(s)")
      elif minute > 0:
        await ctx.send('This command has a cooldown, for '+ str(minute)+" minute(s)")
      else:
        await ctx.send(f'This command has a cooldown, for {error.retry_after:.2f} second(s)')
    elif isinstance(error, CommandNotFound):
      await ctx.send("No command found",delete_after=3)
    elif isinstance(error, MissingPermissions):
      await ctx.send("❌ You don't have permission to do that.")
    elif isinstance(error, CheckFailure):
      await ctx.send(error)
    elif isinstance(error, NotOwner):
      await ctx.send(error)
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("A parameter is missing") 
    else:
      print(error)
      await ctx.reply('An unknown error occured.\nFor more help, join this server (https://discord.gg/t9eH5yuMR4) and send us a photo of the error.')

def setup(bot):
	bot.add_cog(OnCommandErrorCog(bot))
