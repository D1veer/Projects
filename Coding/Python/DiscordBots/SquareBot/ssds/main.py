import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")

@client.event
async def on_ready():
    print("bot is ready ")


kick_channel_log = client.get_channel(id)

# client.load_extension("Main_Commands")
# client.load_extension("Events")
# client.load_extension("Moderation")
client.load_extension("Music")
# client.load_extension("Fun")
# client.load_extension("Utility")
client.load_extension("Owner")
client.run("ODE2Nzg2MDUzMDI4NTExODA2.YEABSg.1N4gxzOgVdy__ioFRo9rB05N1ao")
