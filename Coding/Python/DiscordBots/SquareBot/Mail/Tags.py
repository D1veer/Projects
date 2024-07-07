import discord
from discord.ext import commands
from urllib.parse import urlparse



intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")


waiting_list = []


class Tags(commands.Cog):
	def __init__(self, bot: discord.Bot):
		self.bot = bot


	@commands.command(name="help", aliases=["h"])
	async def dm_command(ctx: commands.Context):
		if isinstance(ctx.channel, discord.channel.DMChannel):
			embed = discord.Embed(title = "Help", description = "**هاذي قائمة بالأوامر المتاحه : **", color = 0x00ff00)
			embed.add_field(name = "suffix", value = "**تستخدم هاذا الأمر للحصول علي الرتب الأجتماعيه**", inline = False)
			await ctx.send(embed = embed)

	@commands.command(name="suffix", aliases=["s"])
	async def dm_command(ctx: commands.Context, playerName: str, url: str):
		if isinstance(ctx.channel, discord.channel.DMChannel):
			message_id = ctx.message.id
			link = urlparse(f"{url}")
			print(waiting_list)
			print(link.hostname)
			await ctx.send("Your Request is being processed")

		if link.hostname == "www.youtube.com":
			msg = f"""
	Yotube Suffix Request:
	IGN: **{playerName}**
	URL: {url}
	<@&931185612348866600>
	"""
			msg_to_add_rection = await client.get_channel(977908560879046667).send(f"{msg}")
			waiting_list.append({"message_id": msg_to_add_rection.id, "member": ctx.author, "playerName": playerName, "url": "youtube", "message": msg_to_add_rection})
			await msg_to_add_rection.add_reaction("✅")
			await msg_to_add_rection.add_reaction("❌")

		if link.hostname == "www.instagram.com":
			msg = f"""
	Instagram Suffix Request:
	IGN: **{playerName}**
	URL: {url}
	<@&931185612348866600>
	"""
			msg_to_add_rection = await client.get_channel(977908560879046667).send(f"{msg}")
			waiting_list.append({"message_id": msg_to_add_rection.id, "member": ctx.author, "playerName": playerName, "url": "instagram", "message": msg_to_add_rection})
			await msg_to_add_rection.add_reaction("✅")
			await msg_to_add_rection.add_reaction("❌")

		if link.hostname == "www.tiktok.com":
			msg = f"""
	Tiktok Suffix Request:
	IGN: **{playerName}**
	URL: {url}
	<@&931185612348866600>
	"""
			msg_to_add_rection = await client.get_channel(977908560879046667).send(f"{msg}")
			waiting_list.append({"message_id": msg_to_add_rection.id, "member": ctx.author, "playerName": playerName, "url": "tiktok", "message": msg_to_add_rection})
			await msg_to_add_rection.add_reaction("✅")
			await msg_to_add_rection.add_reaction("❌")


	@commands.Cog.listener()
	async def on_reaction_add(reaction, user):
		if user.id == client.user.id:
			return
		for i in waiting_list:
			if i["message_id"] == reaction.message.id:
				if reaction.emoji == "✅":
					plrName = i["playerName"]
					plr = i["playerName"]
					plrName = plrName.split(" ")
					ss = "-".join(plrName)
					print(ss)
					# message = await client.get_channel(980964684146557009).send(f"&temp suffix {ss} {i['url']} 7")
					member = i["member"]
					message_to_edit = i["message"]
					await message_to_edit.clear_reactions()
					await message_to_edit.edit(content=f"{message_to_edit.content}\nHas Been Approved By {user.mention}")
					await member.send(f"Your Request Has Been Approved, You Have it in the game with {plr}!")
					del waiting_list[waiting_list.index(i)]
				elif reaction.emoji == "❌":  
					member = i["member"]
					await member.send("**Your Request Has Been Cancelled**!, Check The Rules!")
					del waiting_list[waiting_list.index(i)]

def setup(bot):
	bot.add_cog(Tags(bot))