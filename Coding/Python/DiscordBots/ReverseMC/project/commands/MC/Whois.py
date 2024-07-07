from discord.ext import commands
import discord
from ...utils import utils
from .rconmc import rconmc

class Whois(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot


  @commands.slash_command(
    guild_ids=[1051872539544133652],
    name='WhoIs',
    guild_only=True,
    description="إيجاد معلومات اللاعب.")
  async def whois(
    self,
    ctx: discord.ApplicationContext,
    member: str,
  ):
    if '@' in member:
      # get member with user
      id = utils.get_member_by_str(member)
      # TODO scan for the player and get data with it.
      
    else:
      # get member with name
      response = await rconmc.run_command(f'whois {member}')
      pass
    


def setup(bot):
  bot.add_cog(Whois(bot))