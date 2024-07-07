import os
import sys
sys.dont_write_bytecode = True

"""
This Is the main File For DevilLife Bot.
"""


from discord.ext import commands
import discord
from .src import config

bot: discord.Bot = commands.Bot(
  command_prefix="-",
  help_command=None,
  activity=discord.Activity(type=discord.ActivityType.watching, name='discord.gg/devilife'),
  status=discord.Status.idle,
  case_insensitive=True,
  intents=discord.Intents.all()
)

@bot.event
async def on_ready() -> None:
  print(f'-' * 50, '\n🔃 | Loading Extensions.')
  load_extensions()

def load_extensions() -> None: 
  # for filename in os.listdir("./src/commands/staff"):
  #   if filename.endswith(".py"):
  #     bot.load_extension(f"src.commands.staff.{filename[:-3]}")
  #     print(f'\n✅ | Loaded src.commands.staff.{filename[:-3]} Successfully.')
  print(f'-' * 50, '\n✅ | Loaded Extensions Successfully.\n\n')
  print(f"! {bot.user} has connected to Discord !")

@bot.command(name="r")
async def reset(ctx):
  bot.unload_extension("src.commands.profile")
  bot.load_extension("src.commands.profile")
  bot.unload_extension("src.commands.bank")
  bot.load_extension("src.commands.bank")
  await ctx.send("Done.")

bot.load_extension("src.commands.profile")
bot.load_extension("src.commands.bank")
bot.run(config.TOKEN)
