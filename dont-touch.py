'''import discord
from discord.ext import commands
import re
import json
from replit import db

class AutoMod(commands.Cog, name='AutoModeration'):
    #Moderation command
    def __init__(self, bot):
    	  self.bot = bot
    @commands.Cog.listener()
    async def on_message(self,message):
      with open('cogs/autodisabled.txt','r') as fi:
        a  = fi.readline()
        dg = a.split(', ')
      if str(message.guild.id) not in dg:
        with open('cogs/badwords.txt','r')as f:
          hmm = f.readline()
          yae = hmm.split(', ')
          for i in yae:
            if i == '':
              yae.remove(i)
          if message.author == self.bot.user:
            return
          else:
            for x in yae:
              if len(re.findall(f'{x}',message.content.lower()))>0:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Don't say that >:(", delete_after = 3)
                db[f"{message.author.id}, {message.author.guild}"] += 1
      if message.author == self.bot.user:
        return
                    
def setup(bot):
    bot.add_cog(AutoMod(bot))'''