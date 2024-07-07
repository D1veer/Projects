import discord
from discord.ext import commands

client = commands.Bot(command_prefix = "!")


@client.event
async def on_ready():
    print("bot is ready for fahd")




client.run("OTQ4MzI5MDgyNzIxMDMwMjA1.Yh6OSA.hSzU_IN7ZkzCFSpMZlxnYxL94v4")