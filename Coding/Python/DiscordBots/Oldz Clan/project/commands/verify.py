import discord
from discord.ext import commands
from ..config import *
import sqlite3


db = sqlite3.connect("MCPE.db")
c = db.cursor()
sql = """
CREATE TABLE IF NOT EXISTS MCPE
(MI INT, IGN TEXT)"""

c.execute(sql)

def addUser(MI, IGN):
  data = getUser(MI)
  if data != None:
    return [False, data]
  prams = (MI, IGN)
  sql = f"insert into MCPE VALUES(?, ?)"
  c.execute(sql, prams)
  db.commit()
  return True

def getUser(MI):
  c.execute("SELECT IGN FROM MCPE WHERE MI = ?", (MI,))
  data = c.fetchone()
  return data

def deleteUser(MI):
  sql = 'DELETE FROM MCPE WHERE MI=?'
  c.execute(sql, (MI,))
  db.commit()

class verify(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot
  
  @commands.command(name='verify')
  async def verify(self, ctx: commands.context, member: discord.Member = None, *, ign: str = None):
    if member is None:
      return await ctx.send('>>> __Mention member to verify.__')
    if ign is None:
      return await ctx.send('>>> __Type the in game name to the member to verify.__')

    if member.bot:
      return await ctx.send("__You Can't add a bot.__")
    member_id = member.id
    added = addUser(member_id, ign)
    if added == True:
      await member.edit(nick=f"{member.name} ({ign})")
      await ctx.send(f">>> Added User {member.mention} as {ign}")
    else:
      await ctx.send(f">>> You Already Added as {added[1][0]}")

  @commands.command(name='find')
  async def find(self, ctx, member: discord.Member):
    data = getUser(member.id)
    if data != None:
      await ctx.send(f">>> __{member.mention} is verified as {data[0]}__")
    else:
      await ctx.send(f">>> __I can't find {member.mention}.__")

  @commands.command(name='unverify')
  async def unverify(self, ctx, member: discord.Member):
    data = getUser(member.id)
    await member.edit(nick=member.name)
    if data == None:
      await ctx.send('>>> __Member is not Verified.__')
    else:
      await ctx.send(f'>>> __Done, {member.mention} is not Verify now !__')
      deleteUser(member.id)


def setup(bot):
	bot.add_cog(verify(bot))