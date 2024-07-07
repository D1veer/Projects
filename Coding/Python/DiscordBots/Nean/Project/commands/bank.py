from datetime import datetime
import discord
from discord.ext import commands
from Project.assets.Classes.Bank import Account, Bank
from Project.assets.Classes.Profile import Profile, ProfilesManager
from Project.config import FONTENGPATH, FONTPATH, PROFILECHANNEL, SERVER_ICON, TEMPPROFILE


Bank = Bank()
profileManager = ProfilesManager()

class bank(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @commands.command("رصيدي")
  async def my_money(self, ctx: commands.Context, member: discord.Member = None):
    if member == None:
      member = ctx.author
    
    if profileManager.getProfileByMemberId(member.id) == False:
      await ctx.send("لا يوجد لديك حساب بنكي.")
      return
    
    profile = profileManager.getProfileByMemberId(member.id)
    account = Bank.getAccountById(profile.getId())
    embed = discord.Embed(title="استعلام الرصيد", timestamp=datetime.now())
    embed.add_field(name=f"<@{member.id}>", value=f"{account.getMoney()}SR")
    embed.set_footer(text='البنك المركزي', icon_url=SERVER_ICON)
    await ctx.send(embed=embed)




def setup(bot):
	bot.add_cog(bank(bot))