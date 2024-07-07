from discord import Role, Member, User
from discord.ext import commands
from .. import config


def check_staff(ctx: commands.Context, user: Member | User) -> bool:
  """
  Checks if a user Have the `Staff` role.
  
  :return: Returns True if the user has the `Staff` role or False if not.
  """
  
  role: Role = ctx.guild.get_role(config.STAFF_ROLE_ID)
  
  if role in user.roles:
    return True
  else:
    return False