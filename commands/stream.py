import discord
from discord.ext import commands

class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stream')
    async def set_stream(self, ctx, *, stream_message):
        await self.bot.change_presence(activity=discord.Streaming(name=stream_message, url="https://www.twitch.tv/tunombre"))
        await ctx.send(f"```Ahora estoy transmitiendo en vivo con el mensaje: {stream_message}```")

def setup(bot):
    bot.add_cog(Stream(bot))