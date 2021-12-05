import disnake
from replit import db
from disnake.ext import commands
import random

cashE = '<:YeetCoin:899166414546559056>'

class EconomyCommands(commands.Cog, name='Economy Commands'):
    '''These are the fun commands'''
    def __init__(self, bot):
        self.bot = bot
        
    global cashE

    @commands.command(name='cash',description='Your cash')
    async def cash(self,ctx,user:disnake.Member=None):
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

      
    @commands.command(name='work',description='Work to get more coins')
    @commands.cooldown(rate=1, per=600)
    async def work(self,ctx):
      e = random.randint(-250,250)
      try:
        value = int(db[f'{ctx.author.id}'])
        value += e
        db[f'{ctx.author.id}'] = f'{value}'
        if e<0:
          await ctx.send(f'You messed things up! You spend {-e}{cashE} to make things back.')
        elif e>=0 and e<=50:
          await ctx.send(f"What a lazy guy. You didn't work enough. That is why you only get {e}{cashE}.")
        else:
          await ctx.send(f'You did a great job. You get {e}{cashE} for that.')
      except KeyError:
        db[ctx.author.id]=f'{e}'
        if e<0:
          await ctx.send(f'You messed things up! You spend {-e}{cashE} to make things back.')
        elif e<=0 and e<50:
          await ctx.send(f"What a lazy guy. You didn't work enough. That is why you only get {e}{cashE}.")
        else:
          await ctx.send(f'You did a great job. You get {e}{cashE} for that.')

      
    @commands.command(name='transfer',aliases=['give','move'],description='Give someone your coins with a little tax')
    async def give(self,ctx,user:disnake.User,cash:int):
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
    async def clear(self,ctx,user:disnake.User):
      if ctx.author.id == 832264231617167381 or ctx.author.id == 543656290468102174:
        db[f'{ctx.author.id}'] = '0'
        await ctx.send('Dev powah >>:)')


    @commands.command(name='leaderboard',aliases=['lb'],description='Show the top 20 richest users')
    async def lb(self,ctx):
      e = {}
      high = {}
      for x in ctx.guild.members:
        try:
          e.update({x.name: int(db[str(x.id)])})
        except KeyError:
          db[f"{x.id}"]='0'
          e.update({x.name: 0})
      high=dict(sorted(e.items(),key= lambda x:x[1], reverse = True))
      text = ''
      e = 0
      for x in high:
        if e == 20:
          return
        else:
          text += f'{x}: {high[x]}\n'
        e+=1
      embed = disnake.Embed(title=f'Top highest in {ctx.guild.name}',description=text,color=0x6ba4ff)
      await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(EconomyCommands(bot))