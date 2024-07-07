from sys import flags
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = "-", intents = intents)
client.remove_command("help")


flags_ids_link = "https://flagcdn.com/en/codes.json"











@client.event
async def on_ready():
    print(f"Bot is ready username: {client.user.name}")

# client.load_extension("events")
client.load_extension("Arabic")
client.run("ODE2Nzg2MDUzMDI4NTExODA2.YEABSg.hVozpmO0aDQE7MDPrfV8Eqafaks")