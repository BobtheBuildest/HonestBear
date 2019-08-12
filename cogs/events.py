import discord
from discord.ext import commands
from time import gmtime, strftime
import logging
logging.basicConfig(filename = 'bot.log', level = logging.INFO, format='%(asctime)s %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Bot Online")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)


    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.id != message.author.id:

            if 'aww man' in message.content.lower() or 'aw man' in message.content.lower():
                await message.channel.send('Oh we back in the mine')
            elif 'creeper' in message.content.lower():
                await message.channel.send('aww man')

            if 'owo' in message.content.lower():
                await message.channel.send("OwO What's this?")

            if 'no u' in message.content.lower():
                await message.channel.send("NO U")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        logging.info(f'{member} has joined the server!\n')


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        logging.info(f'{member} has left the server!\n')
        

def setup(bot):
    bot.add_cog(Events(bot))
