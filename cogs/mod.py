import os
import discord
from discord.ext import commands

apikey = os.environ['perapi']

from PyPerspective.Perspective import Perspective #upm package(PyPerspective)
perspective = Perspective(apikey,ratelimit=True,default_not_store=True) # Default Do Not Store Option Is True.
# Default Not Store Option Is For Not Providing Do_Not_Store Kwarg In Get Score Function
# You Can Overwrite Default If You Gave Kwarg In Get Score Func

class Moderation(commands.Cog, name='Moderation'):
  '''Moderation command'''
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(name='ban')
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, user: discord.Member, *, reason=None):
    
      await ctx.send(f'{user.mention} was banned. Reason: {reason}')
      await ctx.guild.ban(user, reason=reason)
    
      
    
  @commands.command(name='kick')
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, user: discord.Member, *, reason=None):
    
      await ctx.guild.kick(user, reason=reason)
      await user.send(f'You got banned from {user.guild.name}. Reason:{reason} ')
      await ctx.send(f'{user.mention} was banned. Reason: ')
    
      

  @commands.command(name='banList')
  @commands.has_permissions(ban_members=True)
  async def banList(self, ctx):
    
      embed = discord.Embed(title=f'Banned user in {ctx.guild.name}')
      bans = await ctx.guild.bans()
      for x in bans:
        embed.add_field(name = f'User {x.user.name}#{x.user.discriminator} with ID: {x.user.id}',value=f'Reason: {x.reason}')
      await ctx.author.send(embed=embed)
      await ctx.send('Sent. Check your DM')
    
      

  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, *, id:int):
    
      user = await self.bot.fetch_user(id)
      await ctx.guild.unban(user)
      await ctx.send(f'{user.mention} is unbanned!')

  @commands.command(name='disableFilter',aliases=['df'])
  @commands.has_permissions(manage_messages=True)
  async def df(self,ctx):
    try:
      with open ('cogs/autodisabled.txt', 'a') as f:
        f.write(f', {str(ctx.channel.id)}')
      await ctx.send('Done')
    except ValueError:
      await ctx.send('The channel is already disabled.')
  
  @commands.command(name='enableFilter',aliases=['ef'])
  @commands.has_permissions(manage_messages=True)
  async def ef(self,ctx):
    try:
      a=[]
      with open ('cogs/autodisabled.txt', 'r+') as f:
        e = f.readline()
        a = e.split(', ')
        if '' in a:
          a.remove('')
      with open('cogs/autodisabled.txt','w') as f:
        a.remove(str(ctx.channel.id))
        f.write('0')
        for x in a:
          f.write(f', {x}')
      await ctx.send('Done')
    except ValueError:
      await ctx.send('The channel is already enabled.')

  @commands.Cog.listener()
  async def on_message(self,message):
      scores = perspective.get_score(message.content,tests=["TOXICITY"],langs=["en"])
      if message.author == self.bot.user:
        return
      if message.content.startswith == 'ys?ct' or message.content.startswith == 'ys?checktoxicity':
        My_Attribute = scores["TOXICITY"]
        print(My_Attribute.score)
        if My_Attribute.score > 0.75:
          await message.delete()
          await message.channel.send(f"{message.author.mention} Don't say that >:(",delete_after=3)
                  
      if message.author == self.bot.user:
            return
  
  @commands.command(name='nuke', description='Clone and delete a channel')
  @commands.has_permissions(manage_channels=True)
  async def nuke(self,ctx):
    
      m = ctx.channel.position
      e = await ctx.channel.clone()
      await ctx.channel.delete()
      await e.edit(position=m)
      await e.send(f'{ctx.message.author.mention} nuked the channel')
    
  @commands.command(name='checkToxicity',aliases=['ct'])
  async def ct(self,ctx,*,other):
    scores = perspective.get_score(other,tests=["TOXICITY"],langs=["en"]) # Tests Default Setted To TOXICITY, Langs Default Setted To English
    My_Attribute = scores["TOXICITY"]
    await ctx.reply(f"Toxicity test for {other} completed.\nIt's toxicity is {My_Attribute.score*100}")

  @commands.command(name='mute',description='Mute someone')
  @commands.has_permissions(manage_messages=True)
  async def mute(self,ctx,user:discord.Member,*,reson=None):
    
      overwrite = discord.PermissionOverwrite()
      overwrite.send_messages = False
      overwrite.read_messages = True
      breh = discord.utils.get(ctx.guild.roles,name="Muted by YAIS")
      if breh == None:
        await ctx.guild.create_role(name="Muted by YAIS")
        await self.bot.add_roles(member=user, role = breh)
        for x in ctx.guild.text_channels:
          await x.set_permissions(breh, overwrite=overwrite)
          await ctx.send('Muted')
      else:
        await user.add_roles(breh)
        for x in ctx.guild.text_channels:
          await x.set_permissions(breh, overwrite=overwrite)
      await ctx.send(f'User {user} has been muted. Reason: {reson}')
    
      
    
  @commands.command(name='unmute')
  @commands.has_permissions(manage_messages=True)
  async def unmute(self,ctx,user:discord.Member,*,reson=None):
    
      overwrite = discord.PermissionOverwrite()
      overwrite.send_messages = False
      overwrite.read_messages = True
      breh = discord.utils.get(ctx.guild.roles,name="Muted by YAIS")
      if breh == None:
        await ctx.guild.create_role(name="Muted by YAIS")
        await self.bot.remove_roles(member=user, role = breh)
        for x in ctx.guild.text_channels:
          await x.set_permissions(breh, overwrite=overwrite)
          await ctx.send('Muted')
      else:
        await user.remove_roles(breh)
        for x in ctx.guild.text_channels:
          await x.set_permissions(breh, overwrite=overwrite)
      await ctx.send(f'User {user} has been unmuted. Reason: {reson}')
    
      

  @commands.command(name='purge',description='Delete a number of messages')
  @commands.has_permissions(manage_messages=True)
  async def purge(self,ctx,count:int):
    
      count += 1
      deleted = await ctx.channel.purge(limit = count)
      await ctx.send(f'Deleted {len(deleted)-1} message',delete_after = 3)
    
      

  @commands.command(name='role')
  @commands.has_permissions(manage_roles=True)
  async def role(self,ctx,user:discord.Member,role:discord.Role):
    
      if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f'Successfully removed {user.mention} {role.mention}')
      else:
        await user.add_roles(role)
        await ctx.send(f'Successfully added {user.mention} {role.mention}')
    
      

  #Permssion error

def setup(bot):
    bot.add_cog(Moderation(bot))