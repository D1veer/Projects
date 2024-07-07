import discord
from discord.ext import commands
from ...config import SERVER_ICON, SERVER_ID


async def get_member(bot, member):
  if isinstance(member, discord.Member) or isinstance(member, discord.User):
    return member
  if member is int:
    await bot.fetch_user(member)
  if member is str:
    # TODO: check if member linked minecraft account with discord and get it
    if member[-1] == ">":
      acmember = member.replace(">", "")
      acmember = acmember.replace("<", "")
      acmember = acmember.replace("@", "")
      print(acmember)
      member = await bot.fetch_user(int(acmember))
  return member