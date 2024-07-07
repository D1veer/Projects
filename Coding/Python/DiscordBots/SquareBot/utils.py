import discord
from discord.ext import commands

ppls = {315896513240760321, 619340445692067890}

class VoiceCommands(commands.Cog):
	def __init__(self, bot: discord.Bot):
		self.bot = bot

	def check_for_ppls(member_id: int):
		for i in ppls:
			if i in ppls:
				return True
		return False


def setup(bot):
	bot.add_cog(VoiceCommands(bot))
