import discord
from discord.ext import commands
import re
import json

class AutoMod(commands.Cog, name='Moderation'):
    '''Moderation command'''
    def __init__(self, bot):
    	  self.bot = bot
    @commands()

    @commands.Cog.listener()
    async def on_message(self,message):
        with open('cogs/autodisabled.txt') as fi:
          a  = fi.readline()
          dg = a.split(', ')
        if str(message.guild.id) in dg:
          return
        else:
          with open('cogs/badwords.txt')as f:
            hmm = f.readline()
            yae = hmm.split(', ')
            search=[]
            if message.author == self.bot.user:
                  return
            if 'abw' or 'sbw' in message.content:
              return
            else:
              for x in yae:
                search+=re.findall(f'{x}',message.content.lower())
                if len(search)>0:
                  await message.delete()
                  await message.channel.send(f"{message.author.mention} Don't say that >:(", delete_after = 3)
                  with open('warn.json','r+') as w:
                    data = json.load(w)
                    
        if message.author == self.bot.user:
                return


def setup(bot):
    bot.add_cog(AutoMod(bot))