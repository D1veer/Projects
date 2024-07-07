import asyncio
import re
import discord
from discord.ext import commands
import events
import json
from tabulate import tabulate
from PIL import Image, ImageFont, ImageDraw

fisrtop = []
secondop = []
thirdop = []
XP_chat_dir = r"./STUFF/databases/XP_chat.json"
XP_voice_dir = r"./STUFF/databases/XP_voice.json"
chat_leaderboard_dir = r'./STUFF/assets/images/chat_leaderboard_temp.png'
voice_leaderboard_dir = r'./STUFF/assets/images/voice_leaderboard_temp.png'
font_dir = r'./STUFF/assets/fonts/Roboto-Regular.ttf'

class StaffCommands(commands.Cog):
	def __init__(self, bot: discord.Bot):
		self.bot = bot


	@commands.command(name = "poll", aliases = ["polls"])
	async def poll(self, ctx: commands.context, time: int, firstoption: str, secondoption: str, thirdoption: str, correctoption: int):
		desc = f"""**لديكم {time} ثانية !**
			1- {firstoption}
			2- {secondoption}
			3- {thirdoption}
		"""
		vote_embed = discord.Embed(title = "اختار الصحيح من الآتي", description =f">>> {desc}", color = 0x00ff00)
		vote_embed = await ctx.send(embed = vote_embed)
		await vote_embed.add_reaction("1️⃣")
		await vote_embed.add_reaction("2️⃣")
		await vote_embed.add_reaction("3️⃣")
		print(correctoption)
		if correctoption == 1:
			correctoption = fisrtop
		elif correctoption == 2:
			correctoption = secondop
		elif correctoption == 3:
			correctoption = thirdop
		await asyncio.sleep(time)
		# for i, user in enumerate(correctoption):
		users = [user for user in correctoption]
		message = ', '.join([str(f"<@{elem}>") for elem in users])
		# 	message = "".join(user.mention)
		await ctx.send(f">>> {message} احسنت اخترت الصحيح")






def setup(bot):
	bot.add_cog(StaffCommands(bot))
