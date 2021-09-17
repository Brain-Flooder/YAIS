import discord
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from discord.utils import get
import time
import random

class FunCommands(commands.Cog, name='FunCommands'):
    '''These are the developer commands'''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
		The default check for this cog whenever a command is used. Returns True if the command is allowed.
		'''
        return ctx.author.id == self.bot.author_id
    
    @commands.command(name='coinflip',aliases=['cf'])
    async def coinfilp(self,ctx):
        await ctx.send(f'{ctx.author.mention} flipped the coin!')
        h = random.randint(0,1)
        time.sleep(random.random()+random.random())
        if h == 1:
          await ctx.send('The coin is head. GG!')
        else:
          await ctx.send('The coin is tail. GG!')

    @commands.command(name='dice')
    async def dice(self,ctx):
        await ctx.send(f'{ctx.author.mention} rolled the dice.')
        time.sleep(random.random()+random.random())
        h = random.randint(1,6)
        if h == 1:
          await ctx.send('The dice rolled 1. GG!')
        if h == 2:
          await ctx.send('The dice rolled 2. GG!')
        if h == 3:
          await ctx.send('The dice rolled 3. GG!')
        if h == 4:
          await ctx.send('The dice rolled 4. GG!')
        if h == 5:
          await ctx.send('The dice rolled 5. GG!')
        if h == 6:
          await ctx.send('The dice rolled 6. GG!')

def setup(bot):
    bot.add_cog(FunCommands(bot))