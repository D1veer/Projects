import os
from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")


@client.event
async def on_ready():
  print(f"{client.user} has connected to Discord!")

async def get_member(member):
  if isinstance(member, discord.Member) or isinstance(member, discord.User):
    return member
  if member is int:
    member = await client.fetch_user(member)
  if member is str:
    # TODO: check if member linked minecraft account with discord and get it
    if member[-1] == ">":
      acmember = member.replace(">", "")
      acmember = acmember.replace("<", "")
      acmember = acmember.replace("@", "")
      print(acmember)
      member = await client.fetch_user(int(acmember))
  return member

for filename in os.listdir("./project/commands"):
  if filename.endswith(".py"):
    client.load_extension(f"project.commands.{filename[:-3]}")

client.run("OTk5NzMzODA1MzU3MjExNzc5.GmBZwk.gCaQbUHA2ViVYs-Z3X64UvdgTZDCaU4ClG-aYg")
