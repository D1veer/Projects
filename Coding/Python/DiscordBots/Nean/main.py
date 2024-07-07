from discord.ext import commands
import discord

intents = discord.Intents.default()
client = commands.Bot(command_prefix = "!", intents = intents)

@client.event
async def on_ready():
  print(f"{client.user} has connected to Discord! {client.user.id}")



client.load_extension("Project.commands.profile")
client.load_extension("Project.commands.bank")
client.run("OTkyNjQ2NjkyMDMxNzA1MTY4.GfVa0o.XlBLdltgN1Q7Qn5S63mr6T8bDZEFhHufRhuwMU")
