import discord
import os
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from discord.utils import get
import time

class DevCommands(commands.Cog, name='Developer Commands'):
    '''These are the developer commands'''
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
		The default check for this cog whenever a command is used. Returns True if the command is allowed.
		'''
        return ctx.author.id == self.bot.author_id

    @commands.command(  # Decorator to declare where a command is.
        name='reload',  # Name of the command, defaults to function name.
        aliases=['rl']  # Aliases for the command.
    )
    async def reload(self, ctx, cog):
        '''
		Reloads a cog.
		'''
        extensions = self.bot.extensions  # A list of the bot's cogs/extensions.
        if cog == 'all':  # Lets you reload all cogs at once
            for extension in extensions:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            await ctx.send('Done')
        if cog in extensions:
            self.bot.unload_extension(cog)  # Unloads the cog
            self.bot.load_extension(cog)  # Loads the cog
            await ctx.send('Done')  # Sends a message where content='Done'
        else:
            await ctx.send('Unknown Cog')  # If the cog isn't found/loaded.

    @commands.command(name="unload", aliases=['ul'])
    async def unload(self, ctx, cog):
        '''
		Unload a cog.
		'''
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.send("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.send(f"`{cog}` has successfully been unloaded.")

    @commands.command(name="load")
    async def load(self, ctx, cog):
        '''
		Loads a cog.
		'''
        try:

            self.bot.load_extension(cog)
            await ctx.send(f"`{cog}` has successfully been loaded.")

        except commands.errors.ExtensionNotFound:
            await ctx.send(f"`{cog}` does not exist!")

    @commands.command(name="listcogs", aliases=['lc'])
    async def listcogs(self, ctx):
        '''
		Returns a list of all enabled commands.
		'''
        base_string = "```css\n"  # Gives some styling to the list (on pc side)
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n```"
        await ctx.send(base_string)


class Moderation(commands.Cog, name='Moderation'):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        '''
		The default check for this cog whenever a command is used. Returns True if the command is allowed.
		'''
        return ctx.author.id == self.bot.author_id

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await ctx.send(f'{user.mention} was banned. Reason: ')
        await ctx.guild.ban(user, reason=reason)

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await ctx.guild.kick(user, reason=reason)
        await user.send(
            f'You got banned from {user.guild.name}. Reason:{reason} ')
        await ctx.send(f'{user.mention} was banned. Reason: ')

    @commands.command(name='banList')
    @commands.has_permissions(ban_members=True)
    async def banList(self, ctx):
        bans = await ctx.guild.bans()
        for x in bans:
          x = str(x)
          x.split(',')
          await ctx.send(x)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, id:int):
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f'{user.mention} is unbanned!')
		
    @commands.command(name='addBadWord',aliases=['abw'])
    @commands.has_permissions(manage_messages=True)
    async def addBadWord(self,ctx,badword):
        with open('cogs/badwords.txt','a')as f:
          f.write('\n')
          f.write(badword)
        await ctx.send('Added successfully!')
        return 0

    @commands.command(name='ShowBadWord',aliases=['sbw'])
    async def ShowBadWord(seld, ctx):
        breh = []
        with open('cogs/badwords.txt') as f:
          for x in f:
            breh.append(x)
        await ctx.send(breh)

    @commands.Cog.listener()
    async def on_message(self,message):
        with open('cogs/badwords.txt')as f:
          for x in f:
            if x.upper() in message.content.upper() and message.author != self.bot.user:
              await message.delete()
              await message.channel.send(f"{message.author.mention} Don't say that!")
        if message.author == self.bot.user:
          return

def setup(bot):
    bot.add_cog(DevCommands(bot))
    bot.add_cog(Moderation(bot))
