import os
from discord.ext import commands
import discord

from project.config import *

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")


@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.idle ,activity=discord.Activity(type=discord.ActivityType.listening, name="Oldz Clan"))
  print(f"{client.user} has connected to Discord!")


for filename in os.listdir("./project/commands"):
  if filename.endswith(".py"):
    client.load_extension(f"project.commands.{filename[:-3]}")

client.run(BOT_TOKEN)
