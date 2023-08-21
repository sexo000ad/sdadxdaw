import discord
from discord.ext import commands
import json
import os
import datetime
from colored import fg, attr
from colorama import Fore, Style  

with open('config.json') as config_file:
    config = json.load(config_file)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=config['prefix'], self_bot=True, intents=intents)

red_color = fg('red')
reset_color = attr('reset')

ascii_art = r"""
                           {    }
                           K,   }
                          /  ~Y`
                     ,   /   /
                    {_'-K.__/
                      `/-.__L._
                      /  ' /`\_}
                     /  ' /
             ____   /  ' /
      ,-'~~~~    ~~/  ' /_
    ,'             ``~~~  ',
   (                        Y
  {                         I
 {      -                    `,
 |       ',                   )
 |        |   ,..__      __. Y
 |    .,_./  Y ' / ^Y   J   )|
 \           |' /   |   |   ||
  \          L_/    . _ (_,.'(
   \,   ,      ^^""' / |      )
     \_  \          /,L]     /
       '-_~-,       ` `   ./`
          `'{_            )
              ^^\..___,.--`
"""

@bot.event
async def on_ready():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{red_color}{timestamp}{reset_color}] {ascii_art}")
    print(f"[{red_color}{timestamp}{reset_color}] Logged in as {bot.user.name} ({bot.user.id})")
    
    command_names = [command.name for command in bot.commands]
    command_names.sort()
    commands_text = " ".join(command_names)
    print(f"[{red_color}{timestamp}{reset_color}] Commands: {commands_text}")
    
    prefix_output = f"[{red_color}{timestamp}{reset_color}] Prefix: {config['prefix']}"
    print(prefix_output)





bot.remove_command('help')

@bot.command()
async def help(ctx):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    command_names = [command.name for command in bot.commands]
    command_names.sort()
    commands_text = " ".join(command_names)
    formatted_output = f"```\n[{red_color}{timestamp}{reset_color}] Commands: {commands_text}\n[{red_color}{timestamp}{reset_color}] Prefix: {config['prefix']}```"
    await ctx.send(formatted_output)

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        if filename == '__init__.py':
            continue
        try:
            extension_name = f'commands.{filename[:-3]}'
            bot.load_extension(extension_name)
        except commands.ExtensionError as e:
            print(f'Error en la extensión {extension_name}: {e}')

bot.run(config['token'], bot=False)