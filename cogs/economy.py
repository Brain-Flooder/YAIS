import discord
from replit import db
from discord.ext import commands
import random
import asyncio

cashE = '<:YeetCoin:899166414546559056>'

class EconomyCommands(commands.Cog, name='EconomyCommands'):
    '''These are the fun commands'''
    def __init__(self, bot):
        self.bot = bot
        
    global cashE

    @commands.command(name='cash')
    async def cash(self,ctx,user:discord.Member=None):
      if user is None:
        try:
          value = db[f'{ctx.author.id}']
          await ctx.send(f'You currently have {value} {cashE}')
        except KeyError:
          value = db[ctx.author.id]='0'
          await ctx.send(f'You currently have {value} {cashE}')
      else:
        try:
          value = db[f'{user.id}']
          await ctx.send(f'{user.mention} currently have {value} {cashE}')
        except KeyError:
          value = db[f'{user.id}']='0'
          await ctx.send(f'{user.mention} currently have {value} {cashE}')

      
    @commands.command(name='work')
    @commands.cooldown(rate=1, per=600)
    async def work(self,ctx):
      e = random.randint(-250,250)
      try:
        value = int(db[f'{ctx.author.id}'])
        value += e
        db[f'{ctx.author.id}'] = f'{value}'
        if e<0:
          await ctx.send(f'You messed things up! You spend {-e}{cashE} to make things back.')
        else:
          await ctx.send(f'You did a great job. You get {e}{cashE} for that.')
      except KeyError:
        db[ctx.author.id]=f'{e}'
        if e<0:
          await ctx.send(f'You messed things up! You spend {-e}{cashE} to make things back.')
        else:
          await ctx.send(f'You did a great job. You get {e}{cashE} for that.')

      
    @commands.command(name='transfer',aliases=['give','move'])
    async def give(self,ctx,user:discord.User,cash:int):
      try:
        value1 = int(db[f'{ctx.author.id}'])
        value2 = int(db[f'{user.id}'])
        if value1 > cash:
          e=cash/100*80
          value1 -= cash
          db[f'{ctx.author.id}'] = f'{value1}'
          value2 += e
          db[f'{user.id}'] = f'{value2}'
          await ctx.send(f'You gave {e} to  {user.mention} after 20% tax. Now, you have {value1} and they got {value2}.')
        else:
          await ctx.send("You don't have enough cash to do it.")
      except KeyError:
        db[f'{user.id}'] = '0'
        value1 = int(db[f'{ctx.author.id}'])
        value2 = int(db[f'{user.id}'])
        if value1 > cash:
          e=cash/100*80
          value1 -= cash
          db[f'{ctx.author.id}'] = f'{value1}'
          value2 += e
          db[f'{user.id}'] = f'{value2}'
          await ctx.send(f'You gave {e} to  {user.mention} after 20% tax. Now, you have {value1} and they got {value2}.')

        else:
          await ctx.send("You don't have enough cash to do it.")

      
    @commands.command(name='test')
    async def test(self,ctx):
      if ctx.author.id == 832264231617167381 or ctx.author.id == 543656290468102174:
        E = db[f'{ctx.author.id}']
        e = int(E)
        e += 50000
        db[f'{ctx.author.id}'] = f'{e}'
        await ctx.send('Dev powah >:)')

    
    @commands.command(name='clear')
    async def clear(self,ctx,user:discord.User):
      if ctx.author.id == 832264231617167381 or ctx.author.id == 543656290468102174:
        db[f'{ctx.author.id}'] = '0'
        await ctx.send('Dev powah >>:)')


    @commands.command(name='leaderboard',aliases=['lb'])
    async def ld(self,ctx):
      e=' The Leaderboard'
      for x in ctx.guild.members:
        try:
          e += f"\n{x.name}: {db[str(x.id)]}"
        except KeyError:
          db[f"{x.id}"]='0'
          e += f"\n{x.name}: {db[str(x.id)]}"
      await ctx.send(e)

    
def setup(bot):
    bot.add_cog(EconomyCommands(bot))