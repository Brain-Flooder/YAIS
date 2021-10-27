import discord
from discord.ext import commands
import time
import random
import asyncio

class GiveawayCommands(commands.Cog, name='Giveaway Commands'):
    '''These are the giveaway commands'''
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='createGW')
    @commands.has_permissions(manage_guild=True)
    async def cgw(self,ctx,times:int,winners,*,prize):
      eh = time.time()
      x=0
      for x in range(0,times):
        eh+=1
        x+=1
      eh=int(eh)
      print(x)
      embed=discord.Embed()
      embed.add_field(name=prize,value=f'React with 🎉 to enter!\nTime: <t:{eh}:R>\nHosted by: {ctx.author.mention}')
      embed.set_footer(text = f'{winners} winner(s)')
      gwlink = await ctx.send(embed=embed)
      await gwlink.add_reaction('🎉')
      await asyncio.sleep(x)
      for s in gwlink.reactions:
        if s.emoji.name == "tada":
          users = await s.users().flatten()
          winner = random.choice(users)
          await gwlink.channel.send(f'{winner.mention} has won the raffle.')
          
          
def setup(bot):
  bot.add_cog(GiveawayCommands(bot))