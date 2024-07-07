from ..config import SERVER_ICON, SERVER_ID, STAFF_ROLE_ID
from tinydb import TinyDB, Query
import discord

db = TinyDB('MC.json')

def get_member_by_str(member: str):
  return member.replace("@", "").replace("<", "").replace(">", "")

def is_staff(member: discord.Member):
  role = member.get_role(STAFF_ROLE_ID)
  if role == None:
    return False
  else:
    return True

def get_member(member: str):
  if "@" in member:
    # todo: Get The ign of member
    User = Query()
    re = db.get(User.id == int(get_member_by_str(member)))
    if re:
      plrName = re["ign"]
      return plrName
    else:
      return None
  else:
    return member

def msgToList(newList):
  msg = ''
  for i, v in enumerate(newList):
    msg += str(v) + " (" + get_member(v) + ")" + " | "
  return msg

