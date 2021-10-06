import discord
import time
from discord.ext import commands

class Music(commands.Cog, name='Developer Commands'):
    '''These are the developer commands'''
    def __init__(self, bot):
        self.bot = bot
    #In dev
    pass

def setup(bot):
    bot.add_cog(Music(bot))