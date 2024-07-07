import os
from discord.ext import commands
import discord
from project.config import TOKEN

bot = commands.Bot(
  command_prefix = "!",
  help_command = None,
  activity = discord.Activity(type=discord.ActivityType.watching, name='discord.gg/reversemc'),
  status = discord.Status.idle,
  case_insensitive=True,
  intents = discord.Intents.all())

@bot.slash_command(
  name="first_slash",
  guild_ids=[816363645671571517]
)
async def first_slash(ctx): 
  await ctx.respond("You executed the slash command!")


@bot.slash_command(
  guild_ids=[816363645671571517],
  name="player",
  description="Get a player name with a good style",
  options=[discord.Option(str, name="name", description="The player name")]
)
async def player(ctx, name: str):
  await ctx.respond(f"**{name.title()}**")


# @bot.event
# async def on_ready():
#   print(f"{bot.user} has connected to Discord!")
#   print(f'_' * 50, '\nLoading Extensions.')

# for filename in os.listdir("./project/commands"):
#   if filename.endswith(".py"):
#     bot.load_extension(f"project.commands.{filename[:-3]}")

print(f'_' * 50, '\nLoaded Extensions Successfully.')

bot.run(TOKEN)
