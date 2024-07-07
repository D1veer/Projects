import os
from discord.ext import commands
import discord
from project.config import TOKEN


bot = commands.Bot(
  command_prefix = "!",
  help_command = None,
  activity = discord.Activity(type=discord.ActivityType.watching, name='discord.gg/solz'),
  status = discord.Status.idle,
  case_insensitive=True,
  intents = discord.Intents.all()
  )

@bot.event
async def on_ready():
  print(f"{bot.user} has connected to Discord!")

for filename in os.listdir("./project/commands"):
  if filename.endswith(".py"):
    bot.load_extension(f"project.commands.{filename[:-3]}")

bot.run(TOKEN)
