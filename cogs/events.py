import discord
from discord.ext import commands
from time import gmtime, strftime
import logging
import helper_files.settings as settings

logger = logging.getLogger('HonestBear')


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Bot Online")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)


    @commands.Cog.listener()
    async def on_message(self, message):
        # If a message is sent not in #debate and is not sent by the bot
        if message.channel.id != 606880223199363172 and self.bot.user.id != message.author.id:
            if 'aww man' in message.content.lower() or 'aw man' in message.content.lower():
                await message.channel.send('Oh we back in the mine')
            elif 'creeper' in message.content.lower():
                await message.channel.send('aww man')

            if 'owo' in message.content.lower():
                await message.channel.send("OwO What's this?")

            if 'no u' in message.content.lower():
                await message.channel.send("NO U")
        
            # If a message is posted in #suggestions, allow people to vote
            if message.channel.id == 607102047195496456:
                await message.add_reaction('✅')
                await message.add_reaction('❌')

def setup(bot):
    bot.add_cog(Events(bot))
    