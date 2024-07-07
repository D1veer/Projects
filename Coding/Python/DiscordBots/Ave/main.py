import discord
from discord.ext import commands
from urllib.parse import urlparse



intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")




client.load_extension("Project.commands.react")
client.run("OTg1OTU4NjEyNzQ2Nzk3MTE3.GpjvCZ.xvNuoyybiNLyD9VZ8GzKOGFzPaCv0I67OkBV_I")