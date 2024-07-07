import discord
from discord.ext import commands



class react(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @commands.command(name="setup", aliases=["run"])
  async def setup(self, ctx, message_id):
    message = await ctx.fetch_message(message_id)
    await message.add_reaction("<a:WhiteCrown:981603687610875924>")


  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    print(reaction)
    print(reaction.emoji)
    print(type(reaction.emoji))
    if reaction.emoji.id == 981603687610875924:
      if user.id == self.bot.user.id:
        return
      roles = user.roles
      role = self.bot.get_guild(980925847978524684).get_role(983984319108382730)
      if role in roles:
        print("its here")
      else:
        await user.add_roles(role)



def setup(bot):
  bot.add_cog(react(bot))