from discord.ext import commands
from discord import Embed

class HelpCommands(commands.Cog, name='Help Commands'):
    '''These are the fun commands'''
    def __init__(self, bot):
      self.bot = bot
    
    @commands.command(name='help')
    async def help(self,ctx):
      embed = Embed(title='My commands')
      cogs = self.bot.cogs
      for x in cogs:
        e = self.bot.get_cog(x)
        wit = e.get_commands()
        w = ''
        for y in wit:
          w += f'`{y.name}` {y.description}\n'
          print(w)
        embed.add_field(name=x,value=f'{w} \n', inline=False)
      await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(HelpCommands(bot))