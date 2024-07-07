import os
import sys
sys.dont_write_bytecode = True

from discord.ext import commands
import discord
from src import config 

bot: discord.Bot = commands.Bot(
  command_prefix="!",
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
  print(f'-' * 50, '\n✅ | Loaded Extensions Successfully.\n\n')
  print(f"! {bot.user} has connected to Discord !")

@bot.command(name="r")
async def reset(ctx):
  bot.unload_extension("src.commands.remnant")
  bot.load_extension("src.commands.remnant")
  await ctx.send("Done.")

bot.load_extension("src.commands.remnant")
bot.run(config.TOKEN)
