import os
import disnake
from disnake.ext import commands
import requests
import json
from google_translate_py import Translator
import urllib3
from replit import db

urllib3.disable_warnings()
apikey = os.environ['perapi']

from pyspective import pyspective

perspective = pyspective.PyspectiveAPI(apikey)


class Moderation(commands.Cog, name='Moderation Commands'):
    '''Moderation command'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban',description='Ban user')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: disnake.Member, *, reason=None):

        await ctx.send(f'{user.mention} was banned. Reason: {reason}')
        await ctx.guild.ban(user, reason=reason)

    @commands.command(name='kick',description='Kick user')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: disnake.Member, *, reason=None):

        await ctx.guild.kick(user, reason=reason)
        await user.send(
            f'You got banned from {user.guild.name}. Reason:{reason} ')
        await ctx.send(f'{user.mention} was banned. Reason: ')

    @commands.command(name='banList',description='Get the banned users list')
    @commands.has_permissions(ban_members=True)
    async def banList(self, ctx):

        embed = disnake.Embed(title=f'Banned user in {ctx.guild.name}')
        bans = await ctx.guild.bans()
        for x in bans:
            embed.add_field(
                name=
                f'User {x.user.name}#{x.user.discriminator} with ID: {x.user.id}',
                value=f'Reason: {x.reason}')
        await ctx.author.send(embed=embed)
        await ctx.send('Sent. Check your DM')

    @commands.command(name='unBan',description='Unban user')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, id: int):

        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f'{user.mention} is unbanned!')

    @commands.command(name='disableFilter', aliases=['df'],description='Disable the AI based filter')
    @commands.has_permissions(manage_messages=True)
    async def df(self, ctx):
        value = db["AI gone"]
        if ctx.channel.id in value:
            await ctx.send('This channel is already disabled.')
            return
        else:
            value.append(ctx.channel.id)
            db["AI gone"] = value
        await ctx.send('Done')

    @commands.command(name='enableFilter', aliases=['ef'],description='Enable the AI based filter')
    @commands.has_permissions(manage_messages=True)
    async def ef(self, ctx):
        value = db["AI gone"]
        if ctx.channel.id in value:
            value.remove(ctx.channel.id)
        else:
            await ctx.send('This channel is already disabled.')
            return
        await ctx.send('Done')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        value = db["AI gone"]
        if str(message.channel.id) not in value:
            if message.content != '':
                translator = Translator()
                tranThis = translator.translate(f"{message.content}", "", "en")
                scores = perspective.score(str(tranThis))
                if 'ys checktoxicity' not in  message.content.lower():
                    if float(scores['TOXICITY']) > 0.9:
                        await message.delete()
                        await message.channel.send(f"{message.author.mention} Don't say that >:(",delete_after=3)
                else:
                    return
            else:
                return

    @commands.command(name='nuke', description='Clone and delete a channel')
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx):
        m = ctx.channel.position
        e = await ctx.channel.clone()
        await ctx.channel.delete()
        await e.edit(position=m)
        await e.send(f'{ctx.message.author.mention} nuked the channel')

    @commands.command(name='checkToxicity',description='Check the toxicity of a word/sentence')
    async def ct(self, ctx, *, other):
        scores = perspective.get_score(other, tests=["TOXICITY"], langs=["en"])  # Tests Default Setted To TOXICITY, Langs Default Setted To English
        My_Attribute = scores["TOXICITY"]
        await ctx.reply(
            f"Toxicity test for {other} completed.\nIt's toxicity is {My_Attribute.score*100}"
        )

    @commands.command(name='mute', description='Mute user')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: disnake.Member, *, reson=None):

        overwrite = disnake.PermissionOverwrite()
        overwrite.send_messages = False
        overwrite.read_messages = True
        breh = disnake.utils.get(ctx.guild.roles, name="Muted by YAIS")
        if breh == None:
            await ctx.guild.create_role(name="Muted by YAIS")
            await self.bot.add_roles(member=user, role=breh)
            for x in ctx.guild.text_channels:
                await x.set_permissions(breh, overwrite=overwrite)
                await ctx.send('Muted')
        else:
            await user.add_roles(breh)
            for x in ctx.guild.text_channels:
                await x.set_permissions(breh, overwrite=overwrite)
        await ctx.send(f'User {user} has been muted. Reason: {reson}')

    @commands.command(name='unmute',description='Unmute user')
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: disnake.Member, *, reson=None):

        overwrite = disnake.PermissionOverwrite()
        overwrite.send_messages = False
        overwrite.read_messages = True
        breh = disnake.utils.get(ctx.guild.roles, name="Muted by YAIS")
        if breh == None:
            await ctx.guild.create_role(name="Muted by YAIS")
            await self.bot.remove_roles(member=user, role=breh)
            for x in ctx.guild.text_channels:
                await x.set_permissions(breh, overwrite=overwrite)
                await ctx.send('Muted')
        else:
            await user.remove_roles(breh)
            for x in ctx.guild.text_channels:
                await x.set_permissions(breh, overwrite=overwrite)
        await ctx.send(f'User {user} has been unmuted. Reason: {reson}')

    @commands.command(name='purge', description='Delete a number of messages')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, count: int):

        count += 1
        deleted = await ctx.channel.purge(limit=count)
        await ctx.send(f'Deleted {len(deleted)-1} message', delete_after=3)

    @commands.command(name='role',description='Give/remove role from an user')
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, user: disnake.Member, role: disnake.Role):

        if role in user.roles:
            await user.remove_roles(role)
            await ctx.send(
                f'Successfully removed {user.mention} {role.mention}')
        else:
            await user.add_roles(role)
            await ctx.send(f'Successfully added {user.mention} {role.mention}')

    @commands.command(name='isScammer',description='Check is a user a scammer. Not always true')
    async def isScammer(self, ctx, user: disnake.User):
        r = requests.get(
            f"https://disnakescammers.com/api/v1/search/{user.id}",
            verify=False)
        response = r.json()
        print(response['status'])
        if response['status'] == 'not_found':
            await ctx.send('That user **might** not a scammer.')
        else:
            await ctx.send('That user is a scammer.')

    @commands.command(name='reportScammer',description='Report scammer')
    async def reportScammer(self, ctx, user: disnake.User, *, info):
        daata = {
            'ScammerID': f"{user.id}",
            'ScammerUsername': f"{user.name}",
            'AdditionalInfo': info
        }
        postME = json.dumps(daata)
        requests.post('https://disnakescammers.com/api/v1/report',
                      data=postME,
                      verify=False)
        await ctx.send('Reported!')


def setup(bot):
    bot.add_cog(Moderation(bot))
