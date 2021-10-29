import disnake
from disnake.ext import commands
from disnake.ext.commands import has_permissions, MissingPermissions

class Suggest(commands.Cog, name='Suggest Commands'):
    '''These are the Suggest commands'''
    def __init__(self, bot):
      self.bot = bot
		
    @commands.command(name='suggest', description='Suggest a idea',aliases=['sg'])
    async def suggest(self,ctx,*,idea):
        embedVar = disnake.Embed(title=f"Suggest from user with ID: {ctx.author.id}", description=f'{idea}', color=0x6FB9FF)
        with open('cogs/isban.txt')as file:
          for isBanned in file:
            isBanned = int(isBanned)
            if ctx.author.id != isBanned:
              with open('cogs/channel.txt')as f:
                  for hey in f:
                    hey=int(hey)
                    channel = ctx.guild.get_channel(hey)
                    if channel is not None:
                      hmm = await channel.send(content=ctx.author.id,embed=embedVar)
                      cross = '\N{THUMBS DOWN SIGN}'
                      checkM = '\N{THUMBS UP SIGN}'
                      await hmm.add_reaction(checkM)
                      await hmm.add_reaction(cross)
              embedBreh = disnake.Embed(title='Sent',value='Your suggestion has been sent!')
              await ctx.send(embed=embedBreh)
            else:
              ctx.send("You have been banned from our system.")
              return 0
    @commands.command(name='approve', description='Approve a suggestion',aliases=['ap'])
    @has_permissions(manage_messages=True)
    async def _approve(self,ctx,id):
        id=int(id)
        global yay
        huh = await ctx.channel.fetch_message(id)
        member = huh.content
        member = int(member)
        user = await ctx.bot.fetch_user(member)
        await huh.reply(f'Suggest is approved!')
        await huh.edit(content=f'{user.mention} Your suggest has been approved!')
        

    @commands.command(name='decline', description='Decline a suggestion',aliases=['dc'])
    @has_permissions(manage_messages=True)
    async def _decline(self,ctx,id):
        id=int(id)
        global yay
        huh = await ctx.fetch_message(id)
        await huh.reply(f'{huh.author.mention} Your suggest has been declined!')
        await huh.edit(content='Declined.')

  

    @commands.command(name='Setup', description='Set up channel that suggestions will be sent to it')
    @has_permissions(manage_channels=True)
    async def _setup(self,ctx,id=None):
        if id is None:
            with open('cogs/channel.txt','a') as f:
                f.write('\n')
                f.write(str(ctx.channel.id))
        else:
            with open('cogs/channel.txt','a') as f:
                f.write('\n')
                f.write(id)
        embedVar = disnake.Embed(title="Set up done!",color=0x85C4FF)
        await ctx.send(embed=embedVar)

    @commands.command(name='report',description='Report a suggestion',aliases=['rp'])
    async def _report(self,ctx,messagelink):
        re = await ctx.bot.fetch_channel(883956344472895529)
        await re.send(content=messagelink)
        await ctx.send(content='Sent')

    @_setup.error
    async def error(self,ctx, error):
        if isinstance(error, MissingPermissions):
            text = f"Sorry {ctx.author.mention}, you do not have permissions to do that!"
            await ctx.send(text,delete_after=2)

def setup(bot):
    bot.add_cog(Suggest(bot))