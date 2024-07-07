import os
from unittest import async_case
from discord.ext import commands
import discord


bot = commands.Bot(
  command_prefix = "!",
  help_command = None,
  activity = discord.Activity(type=discord.ActivityType.watching, name='discord.gg/solz'),
  status = discord.Status.idle,
  case_insensitive=True,
  intents = discord.Intents.all()
)

client.run("ODc2MDIzMzY4MDI4MTQzNjY3.GNzQdL.dK13lnHphGwIkVwPB6tiPCvgSjq2AIDkvi6jl0")
