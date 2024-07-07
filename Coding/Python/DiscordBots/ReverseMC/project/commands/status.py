import discord
from discord.ext import commands
from ..config import SERVER_ICON, SERVER_ID, STATUS_CHANNEL_ID


class status(commands.Cog):
	def __init__(self, bot: discord.Bot):
		self.bot = bot
		self.timeout_status_msgcommand = 5

	@commands.slash_command(guild_ids=[SERVER_ID], name="status", description='Change the status of the server', options=[discord.Option(str, name='condition', choices=['working', 'maintenance', 'updating'])])
	async def setStatus(self, ctx: discord.ApplicationContext, status):
		if status == 'working':
			pass
			msg = '✅ Server is Running.'
			channel = self.bot.get_channel(STATUS_CHANNEL_ID)
			await channel.purge()
			embed = discord.Embed(title="ReverseMC (Status)", color=0xada800)
			embed.description = f'{msg} \nThe Server Now Is Closed.'
			await channel.send(embed=embed)
			await ctx.respond('Change The Status.', ephemeral=True, delete_after=self.timeout_status_msgcommand)
			pass
		elif status == 'maintenance':
			pass
			msg = '⚠️ Server is under Maintenance.'
			channel = self.bot.get_channel(STATUS_CHANNEL_ID)
			await channel.purge()
			embed = discord.Embed(title="ReverseMC (Status)", color=0xada800)
			embed.description = f'{msg} \nThe Server Now Is Closed.'
			await channel.send(embed=embed)
			await ctx.respond('Change The Status.', ephemeral=True, delete_after=self.timeout_status_msgcommand)
			pass
		elif status == 'updating':
			pass
			msg = '🔜 We Working on a new Update.'
			channel = self.bot.get_channel(STATUS_CHANNEL_ID)
			await channel.purge()
			embed = discord.Embed(title="ReverseMC (Status)", color=0xada800)
			embed.description = f'{msg} \nThe Server Now Is Closed.'
			await channel.send(embed=embed)
			await ctx.respond('Change The Status.', ephemeral=True, delete_after=self.timeout_status_msgcommand)
			pass


def setup(bot):
	bot.add_cog(status(bot))
