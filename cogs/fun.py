import discord
from discord.ext import commands
import time
import random
import asyncio

class FunCommands(commands.Cog, name='FunCommands'):
    '''These are the fun commands'''
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='coinflip',aliases=['cf'])
    async def coinfilp(self,ctx):
        await ctx.send(f'{ctx.author.mention} flipped the coin!')
        h = random.randint(0,1)
        await asyncio.sleep(random.random()+random.random()+random.random())
        if h == 1:
          await ctx.send('The coin is head. GG!')
        else:
          await ctx.send('The coin is tail. GG!')

    @commands.command(name='dice')
    async def dice(self,ctx):
        await ctx.send(f'{ctx.author.mention} rolled the dice.')
        await asyncio.sleep(random.random()+random.random()+random.random())
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