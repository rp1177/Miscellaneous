import discord
from discord.ext import commands

"""
Any Miscellaneous Commands not associated with gmail,
for general testing purposes.

"""

class General(commands.Cog):
    
    # Initialize Bot 
    def __init__(self, bot):
        self.bot = bot
    
    # Make sure General cog is activated 
    @commands.Cog.listener()
    async def on_ready(self):
        print("General cog loaded")

    # A general test command !misc [enter text]
    @commands.command(name='misc')
    async def misc(self, ctx, *args):
        arguments = ' '.join(args)
        await ctx.send(arguments)


async def setup(bot):
    await bot.add_cog(General(bot))
    print("Setup and adding cog completed.")


