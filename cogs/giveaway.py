import discord
from discord.ext import commands
import time
import random
import asyncio

class GiveawayCommands(commands.Cog, name='FunCommands'):
    '''These are the giveaway commands'''
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='createGW')
    @commands.has_permissions(manage_guild=True)
    async def cgw(self,ctx,times:int,winners,*,prize):
      eh = time.time()
      for x in range(0,times):
        eh+=60
      eh=int(eh)
      embed=discord.Embed()
      embed.add_field(name=prize,value=f'React with 🎉 to enter!\nTime: <t:{eh}:R>\nHosted by: {ctx.author.mention}')
      embed.set_footer(text = f'{winners} winner(s)')
      gwlink = await ctx.send(embed=embed)
      await gwlink.add_reaction('🎉')
      await asyncio.sleep(eh)
      await ctx.send(f"{gwlink.reactions}")

def setup(bot):
    bot.add_cog(GiveawayCommands(bot))