import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import re
from replit import db

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
    
  @commands.command(name='addBadWord',aliases=['abw'])
  @commands.has_permissions(manage_messages=True)
  async def addBadWord(self,ctx,badword:str):
    with open('cogs/badwords.txt','r+')as f:
      hmm = f.readline()
      check=re.findall(f'{badword}',hmm)
      if len(check) > 0:
        await ctx.send("Hmm.. Seem like this word is already in the bad words list")
      else:
        f.seek(0)
        f.write(f', {badword}')
        await ctx.send('Added successfully!')

  @commands.command(name='ShowBadWord',aliases=['sbw'])
  async def ShowBadWord(seld, ctx):
    with open('cogs/badwords.txt','r') as f:
      f.seek(2)
      hmm=f.readline()
    await ctx.send(f'Bad words list: {hmm}.')
    
  @commands.command(name='enableFilter',aliases=['ef'])
  @commands.has_permissions(manage_messages=True)
  async def df(self,ctx):
    with open ('cogs/autodisabled.txt', 'r+') as f:
      e = f.readline()
      i = e.split(', ')
      a=''
      for x in i:
        if x == str(ctx.guild.id):
          pass
        else:
          a+=f', {x}'
      f.seek(0)
      f.truncate()
      f.write(a)
    await ctx.send('Done')
    
  @commands.command(name='disableFilter',aliases=['df'])
  @commands.has_permissions(manage_messages=True)
  async def ef(self,ctx):
    with open ('cogs/autodisabled.txt', 'a') as f:
      f.write(f'{str(ctx.guild.id)}, ')
    await ctx.send('Done')

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
                try:
                  db[f"{message.author.id}, {message.author.guild.id}"]
                except:
                  db[f"{message.author.id}, {message.author.guild.id}"] ='1'
                
        if message.author == self.bot.user:
          return
  
  @commands.command()
  async def check(self,ctx):
    e=db.keys()
    print(e)
  
  @commands.command()
  async def clearwarn(self,ctx,mem:discord.Member):
    try:
      del db[f"{mem.id}, {mem.guild}"]
    except:
      print(db[f"{mem.id}, {mem.guild}"])
  
  @commands.command(name='nuke', description='Clone and delete a channel')
  @has_permissions(manage_channels=True)
  async def nuke(self,ctx):
    m = ctx.channel.position
    e = await ctx.channel.clone()
    await ctx.channel.delete()
    await e.edit(position=m)
    await e.send(f'{ctx.message.author.mention} nuked the channel')

  @commands.command(name='mute',description='Mute someone')
  @has_permissions(manage_messages=True)
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
  @has_permissions(manage_messages=True)
  async def purge(self,ctx,count:int):
    count+=1
    mscount=-1
    async for message in ctx.channel.history(limit=count):
      await message.delete()
      mscount+=1
    await ctx.send(f'Successfully deleted {mscount} message',delete_after=3)

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