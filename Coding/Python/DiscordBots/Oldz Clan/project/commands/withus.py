from datetime import datetime
import discord
from discord.ext import commands
# from ..config import *
import sqlite3

from project.commands.verify import getUser

db = sqlite3.connect("WITHUS.db")
c = db.cursor()
sql = """
CREATE TABLE IF NOT EXISTS MEMBERS
(IGN TEXT, MI INT)
"""
c.execute(sql)


def GetMember(MI):
  c.execute("SELECT MI FROM MEMBERS WHERE MI = ?", (MI,))
  data = c.fetchone()
  return data

def AddMember(IGN, MI):
  data = GetMember(MI)
  if data != None:
    return [False, data]
  prams = (IGN, MI)
  sql = f"insert into MEMBERS VALUES(?, ?)"
  c.execute(sql, prams)
  db.commit()
  return True

def RemoveMember():
  pass

def GetAllMembers():
  sql = """SELECT * from MEMBERS"""
  c.execute(sql)
  records = c.fetchall()
  return [records, len(records)]

class withus(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @commands.command(name='withus')
  async def withus_def(self, ctx: commands.Context, type = None, member: discord.Member = None):
    if type == None:
      # Get the list of with us members
      members = GetAllMembers()
      withusMembers = []
      for i in members[0]:
        embed = discord.Embed(title='With Us List', timestamp=datetime.now(), color=discord.Color.yellow())
        member = await self.bot.get_or_fetch_user(i[1])
        IGN = getUser(member.id)
        withusMembers.append(f'{member.name}#{member.discriminator} ({IGN[0]})')
      allMembers = ", ".join(withusMembers)
      embed.description = f">>> ```{allMembers}``` \n {members[1]} Member"
      await ctx.send(embed=embed)
    elif type == 'add':
      # Add a member to the with us list
      if member is None:
        return await ctx.send('__Please Insert a Member To add !__')
      user = getUser(member.id)
      if user is None:
        return await ctx.send('__Please Make Sure its verifid !__')
      result = AddMember(user[0], member.id)
      print(result)
      await ctx.send(f'>>> Add To The With Us List Succusfly {member.mention} as {user[0]}')
      pass
    elif type == 'remove':
      #  Remove a memeber to the with list
      pass 



def setup(bot):
	bot.add_cog(withus(bot))