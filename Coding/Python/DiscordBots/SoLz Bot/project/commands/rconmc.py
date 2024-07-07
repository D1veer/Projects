import re
from discord.ext import commands
import discord
from rcon.source import rcon
from tinydb import TinyDB, Query

from project.config import RCON_IP, RCON_PASS, RCON_PORT, SERVER_ID
from ..utils.utils import get_member, msgToList, get_emoji

db = TinyDB(r'MC.json')


class rconmc(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @commands.command(name='pl', aliases=["plugins", 'plugin'])
  async def plugins(self, ctx: commands.Context):
    response = await rcon(
      'pl',
      host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
    await ctx.send(response)

  @commands.command(name="players", aliases=["mcplayers"])
  async def players(self, ctx: commands.Context):
    response = await rcon(
      'list',
      host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
    index = response.find("\n")
    response = response[index + 1:]
    newList = response.split(",")
    member_string = msgToList(newList)
    await ctx.send(member_string + f" {len(newList)} Player(s)")

  @commands.command(name='kick', aliases=['k'])
  async def kick(self, ctx: commands.Context, plrName: str=None, *, reason="No Reason"):
    role = self.bot.get_guild(SERVER_ID).get_role(987045962751041576)
    if role not in ctx.author.roles:
      return await ctx.send("You Can't Use This Command (You Aren't staff)")
    if plrName == None:
      return await ctx.send("Please Type Your Name In The Game.")
    plrName = get_member(plrName)
    if plrName == None:
      return await ctx.send("Member is not linked...")
    try:
      response = await rcon(
        'kick', f'{plrName}', reason,
        host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
      if response == "":
        await ctx.send(f"{plrName} Has Been Kicked For {reason}")
      else:
        await ctx.send(response)
    except Exception as e:
      if isinstance(e, discord.errors.HTTPException):
        await ctx.send(f"{plrName} Has Been Kicked For {reason}")
      else:
        await ctx.send(e)

  @commands.command(name='link', aliases=['linkmc'])
  async def link(self, ctx: commands.Context, id):
    response = await rcon(
      'check', f'{id}',
      host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
    # await ctx.send(response)
    if response == "False":
      pass
      await ctx.send('Please Check your Id')
    else:
      await ctx.send('You Have Been Linked')
      db.insert({"id": ctx.author.id, 'ign': response})
      await ctx.send(f"Linked as {response}")


  @commands.command(name="usermc")
  async def usermc(self, ctx, member: discord.Member):
    User = Query()
    re = db.get(User.id == member.id)
    if re:
      print(re["ign"])
      await ctx.send(re["ign"])
    else:
      await ctx.send(f'{get_emoji("warn")} | can\'t find the user')

  @commands.command(name='rcon', aliases=['r'])
  async def rcon(self, ctx: commands.Context, *message):
    role = self.bot.get_guild(SERVER_ID).get_role(987045962751041576)
    if role not in ctx.author.roles:
      return await ctx.send("You Can't Use This Command (You Aren't staff)")
    # if ctx.author.id != 619340445692067890:
      # return await ctx.send("only my maker diveer (dodo)")
    await ctx.send(message)
    for msg in message:
      if ' ' in msg:
        y = list(message)
        y.remove(msg)
        y.append(f'"{msg}"')
        message = tuple(y)
    try:
      response = await rcon(
        *message,
        host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
      await ctx.send(response)
    except Exception as e:
      if isinstance(e, discord.errors.HTTPException):
        await ctx.send("The command run successfully")
      else:
        await ctx.send(e)

def setup(bot):
  bot.add_cog(rconmc(bot))