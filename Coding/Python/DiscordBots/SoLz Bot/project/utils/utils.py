import discord
from discord.ext import commands
from tinydb import TinyDB, Query

db = TinyDB('MC.json')

def get_member_by_str(member: str):
  return member.replace("@", "").replace("<", "").replace(">", "")

def get_emoji(name: str):
  name = name.lower()
  if name == 'warn':
    return '<:warning:1017110666181615690>'

def get_member(member: str):
  if "@" in member:
    # TODO: Get The ign of member
    User = Query()
    re = db.search(User.id == int(get_member_by_str(member)))
    if re:
      plrName = re[0]["ign"]
      return plrName
    else:
      return None
  else:
    return "Not Linked"

def msgToList(newList):
  msg = ''
  for i, v in enumerate(newList):
    msg += str(v) + " (" + get_member(v) + ")" + " | "
  return msg




