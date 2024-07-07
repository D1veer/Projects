"""
  This Is the main File
  This Project Made By Diveer (@D1veer) yosefbesher34@gmail.com
  Thanks For Using My Projects
  Github Link: 
"""

import os
import discord.commands
from discord.ext import commands
import discord
import discord.bot
from src import config

bot = commands.Bot(
  command_prefix="!",
  help_command=None,
  activity=discord.Activity(type=discord.ActivityType.streaming, name='Made By @Diveer.'),
  status=discord.Status.idle,
  case_insensitive=True,
  intents=discord.Intents.all()
)

for filename in os.listdir("./src/commands"):
  if filename.endswith(".py"):
    bot.load_extension(f"src.commands.{filename[:-3]}")
    print(f'\n✅ | Loaded src.commands.{filename[:-3]} Successfully.')
print(f'-' * 50, '\n✅ | Loaded Extensions Successfully.\n\n')
print(f"! {bot.user} has connected to Discord and Ready To Run")


@bot.event
async def on_ready() -> None:
  print('Try To Conneting To Discord..')
  print(f'Connected To Discord Discord as {bot.user.display_name}')
  print(f'-' * 50, '\n🔃 | Loading Extensions.')


bot.run(config.TOKEN)