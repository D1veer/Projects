"""
This Is the main File
"""
import os
from discord.ext import commands
from discord import Bot
import discord
from src import config

bot: Bot = commands.Bot(
  command_prefix="!",
  help_command=None,
  activity=discord.Activity(type=discord.ActivityType.watching, name='discord.gg/reversemc'),
  status=discord.Status.idle,
  case_insensitive=True,
  intents=discord.Intents.all()
)


@bot.event
async def on_ready() -> None:
  print(f'-' * 50, '\n🔃 | Loading Extensions.')
  load_extensions()

def load_extensions() -> None: 
  for filename in os.listdir("./src/commands/staff"):
    if filename.endswith(".py"):
      bot.load_extension(f"src.commands.staff.{filename[:-3]}")
      print(f'\n✅ | Loaded src.commands.staff.{filename[:-3]} Successfully.')
  print(f'-' * 50, '\n✅ | Loaded Extensions Successfully.\n\n')
  print(f"! {bot.user} has connected to Discord !")

bot.run(config.TOKEN)