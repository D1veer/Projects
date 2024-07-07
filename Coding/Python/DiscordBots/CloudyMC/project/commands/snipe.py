import discord
from discord.ext import commands
from ..config import SERVER_ICON, SERVER_ID

sniped_messages = {}

class snipe(commands.Cog):
	def __init__(self, bot: discord.Bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if range(len(sniped_messages)) == 3:
			del sniped_messages[-1]
		history = sniped_messages.get(message.channel.id, [])
		history.insert(0, message)
		sniped_messages[message.channel.id] = history

	@commands.command()
	async def snipe(self, ctx, *, page: int = 1):
		role = self.bot.get_guild(SERVER_ID).get_role(974525778073092167)
		if role in ctx.author.roles:
			channel = ctx.channel
			try:
				message = sniped_messages[ctx.message.channel.id][page-1]
			except Exception as e:
				await ctx.channel.send(f"No available snips at page : {page}")
				return
			embed = discord.Embed(color = discord.Color.purple())
			embed.set_author(name=f"Last Deleted Message In {channel.name}")
			embed.add_field(name="Author:", value=message.author.mention)
			embed.add_field(name="Message:", value=message.content)
			if ctx.author.avatar == None:
				avatar = "https://cdn.discordapp.com/embed/avatars/0.png"
				embed.set_author(name=f"{ctx.author.name}", icon_url=f"{avatar}")
			else:
				embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar}")
			embed.timestamp = message.created_at
			embed.set_footer(text=f"{self.bot.get_guild(SERVER_ID).name}", icon_url=f"{SERVER_ICON}")
			await ctx.send(embed=embed)
		else:
			await ctx.send("You do not have the required permissions to use this command.")

def setup(bot):
	bot.add_cog(snipe(bot))
