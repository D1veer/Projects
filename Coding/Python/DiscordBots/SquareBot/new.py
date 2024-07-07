		import discord
		from discord.ext import commands
		import events
		import json
		from tabulate import tabulate
		from PIL import Image, ImageFont, ImageDraw

		XP_chat_dir = r"./STUFF/databases/XP_chat.json"
		XP_voice_dir = r"./STUFF/databases/XP_voice.json"
		chat_leaderboard_dir = r'./STUFF/assets/images/chat_leaderboard_temp.png'
		voice_leaderboard_dir = r'./STUFF/assets/images/voice_leaderboard_temp.png'
		font_dir = r'./STUFF/assets/fonts/Roboto-Regular.ttf'

		class StaffCommands(commands.Cog):
			def __init__(self, bot):
				self.bot = bot
			@commands.command(hidden=True)
			@commands.is_owner()
			async def load(self, *, module : str):
				"""Loads a module."""
				try:
					self.bot.load_extension(module)
				except Exception as e:
					await self.bot.say('\N{PISTOL}')
					await self.bot.say('{}: {}'.format(type(e).__name__, e))
				else:
					await self.bot.say('\N{OK HAND SIGN}')

			@commands.command(hidden=True)
			@commands.is_owner()
			async def unload(self, *, module : str):
				"""Unloads a module."""
				try:
					self.bot.unload_extension(module)
				except Exception as e:
					await self.bot.say('\N{PISTOL}')
					await self.bot.say('{}: {}'.format(type(e).__name__, e))
				else:
					await self.bot.say('\N{OK HAND SIGN}')

			@commands.command(name='reload', hidden=True)
			@commands.is_owner()
			async def _reload(self, *, module : str):
				"""Reloads a module."""
				try:
					self.bot.unload_extension(module)
					self.bot.load_extension(module)
				except Exception as e:
					await self.bot.say('\N{PISTOL}')
					await self.bot.say('{}: {}'.format(type(e).__name__, e))
				else:
					await self.bot.say('\N{OK HAND SIGN}')
			@commands.slash_command(name = "shutup")
			async def shutup(self, ctx, member: discord.Member = None):
				if ctx.author.id == 619340445692067890:
					if member:
						events.shutuped[member.id] = True
				else:
					await ctx.send(f"سبك لازم بس يوسف <@619340445692067890>")
			
			@commands.slash_command(name = "unshutup")
			async def shutup(self, ctx, member: discord.Member = None):
				if ctx.author.id == 619340445692067890:
					if member:
						if member.id in events.shutuped:
							del events.shutuped[member.id]
				else:
					await ctx.send(f"سبك لازم بس يوسف <@619340445692067890>")

			@commands.slash_command(guild_ids=[692158495235112972], name="xpchat", description="Get The XP For A User", usage="xp_chat <user>")
			async def xp_chat_def(self, ctx, member: discord.Member = None):
				member_to_find_id = None
				xp_of_chat = None

				if member is None:
					member_to_find_id = ctx.author.id
				else:
					member_to_find_id = member.id


				with open(XP_chat_dir, 'r') as file:
					XP_data = json.load(file)
				
				new_user = member_to_find_id

				if f"{new_user}" in XP_data:
					xp_of_chat = XP_data[f"{new_user}"]

				
				await ctx.respond(f"<@!{member_to_find_id}> has: {xp_of_chat} XP in chat")

			@commands.slash_command(guild_ids=[692158495235112972], name="xpvoice", description="Get The XP For A User", usage="xp_voice <user>")
			async def xp_voice_def(self, ctx, member: discord.Member = None):
				member_to_find_id = None
				xp_of_chat = None

				if member is None:
					member_to_find_id = ctx.author.id
				else:
					member_to_find_id = member.id


				with open(XP_voice_dir, 'r') as file:
					XP_data = json.load(file)
				
				new_user = member_to_find_id

				if f"{new_user}" in XP_data:
					xp_of_chat = XP_data[f"{new_user}"]

				
				await ctx.respond(f"<@!{member_to_find_id}> has: {xp_of_chat} XP in voice")


			@commands.slash_command(guild_ids=[692158495235112972], name="addxpchat", description="Add XP To A User", usage="addxp_chat <user> <amount>")
			@commands.has_permissions(administrator = True)
			async def addxpchat_def(self, ctx, member: discord.Member = None, xp_to_add: int = None):

				if member is None:
					await ctx.send("Please specify a member.")
					return

				if xp_to_add is None:
					await ctx.send("Please specify a amount of XP.")
					return

				member_ID = member.id

				if f"{member_ID}" in events.XP:
					events.XP[f"{member_ID}"] += xp_to_add
					await ctx.send(f"Add {xp_to_add} XP To <@!{member_ID}> Successfully!")
				else:
					events.XP[f"{member_ID}"] = xp_to_add
					await ctx.respond(f"Add {xp_to_add} XP To <@!{member_ID}> Successfully!")

			@commands.command(name = "delxp")
			@commands.has_permissions(administrator = True)
			async def deletexp(self, ctx, member: discord.Member = None, xp_to_add: int = None):

				if member is None:
					await ctx.send("Please specify a member.")
					return

				if xp_to_add is None:
					await ctx.send("Please specify a amount of XP.")
					return

				member_ID = member.id

				if f"{member_ID}" in events.XP:
					if xp_to_add > events.XP[f"{member_ID}"]:
						events.XP[f"{member_ID}"] = 0
					else:
						events.XP[f"{member_ID}"] -= xp_to_add
					await ctx.send(f"Removed {xp_to_add} XP From <@!{member_ID}> Successfully!")
				else:
					await ctx.send(f"<@!{member_ID}> Have 0 XP")
					return

			@commands.slash_command(guild_ids=[692158495235112972], name="topchat", description="Get The XP For A User", usage="top_chat")
			async def top_chat(self, ctx):
				with open(XP_chat_dir, 'r') as file:
					voice_data = json.load(file)
				
				users_xp = list(voice_data.values())
				users_id = list(voice_data.keys())

				new_list = []

				for i, user_id in enumerate(users_id, 1):
					new_list.append([user_id, users_xp[i - 1]])

				new_list.sort(key = lambda x: x[1], reverse = True)

				user_rank = []
				user_name = []
				user_xp = []

				for i, user_id in enumerate(new_list[:10]):
					user_name.append([await self.bot.fetch_user(int(user_id[0]))])
					user_xp.append([user_id[1]])
					user_rank.append([i + 1])
					

				# Append column to table
				user_rank_table = tabulate(user_rank, tablefmt='plain', headers=['#\n'], numalign='left')
				user_name_table = tabulate(user_name, tablefmt='plain', headers=['Name\n'], numalign='left')
				user_time_spent_table = tabulate(user_xp, tablefmt='plain', headers=['XP\n'],numalign='left')

				image_template = Image.open(chat_leaderboard_dir)

				# Font
				font = ImageFont.truetype(font_dir, 38)

				# Positions
				rank_text_position = 30, 50
				name_text_position = 80, 50
				rank_time_spent_text_position = 500, 50

				# Draws
				draw_on_image = ImageDraw.Draw(image_template)
				draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
				draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
				draw_on_image.text(rank_time_spent_text_position, user_time_spent_table, 'white', font=font)

				# Save image
				image_template.convert('RGB').save('chat_leaderboard.jpg', 'JPEG')

				await ctx.respond(file=discord.File('chat_leaderboard.jpg'))


			@commands.slash_command(guild_ids=[692158495235112972], name="topvoice", description="Get The XP For A User", usage="top_voice")
			async def top_voice(self, ctx):
				with open(XP_voice_dir, 'r') as file:
					voice_data = json.load(file)
				
				users_xp = list(voice_data.values())
				users_id = list(voice_data.keys())

				new_list = []

				for i, user_id in enumerate(users_id, 1):
					new_list.append([user_id, users_xp[i - 1]])

				new_list.sort(key = lambda x: x[1], reverse = True)

				user_rank = []
				user_name = []
				user_xp = []


				for i, user_id in enumerate(new_list[:10]):
					n = user_id[1]

					day = n // (24 * 3600)
					n = n % (24 * 3600)
					hour = n // 3600

					n %= 3600
					minutes = n // 60

					n %= 60
					seconds = n

					
					user_name.append([await self.bot.fetch_user(int(user_id[0]))])
					user_xp.append([f"{day}d:{hour}h:{minutes}m:{seconds}s"])
					user_rank.append([i + 1])

				# Append column to table
				user_rank_table = tabulate(user_rank, tablefmt='plain', headers=['#\n'], numalign='left')
				user_name_table = tabulate(user_name, tablefmt='plain', headers=['Name\n'], numalign='left')
				user_time_spent_table = tabulate(user_xp, tablefmt='plain', headers=['Time Spent\n'],numalign='left')

				image_template = Image.open(voice_leaderboard_dir)

				# Font
				font = ImageFont.truetype(font_dir, 38)

				# Positions
				rank_text_position = 30, 50
				name_text_position = 80, 50
				rank_time_spent_text_position = 500, 50

				# Draws
				draw_on_image = ImageDraw.Draw(image_template)
				draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
				draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
				draw_on_image.text(rank_time_spent_text_position, user_time_spent_table, 'white', font=font)

				# Save image
				image_template.convert('RGB').save('voice_leaderboard_temp.jpg', 'JPEG')

				await ctx.respond(file=discord.File('voice_leaderboard_temp.jpg'))




			@commands.command(name = "kick")
			@commands.has_permissions(administrator = True)
			async def kick(self, ctx, member: discord.Member = None, *, reason = None):
				# embed.set_image(f"{member.avatar_url}")

				if member is None:
					await ctx.send("Please specify a member.")
					return

				embed = discord.Embed(title = "Kicked Member Notification", description = f"{member.mention} Has Been Kicked For {reason}", colour = discord.colour.Colour.red())
				embed.set_footer(text = f"Kicked By <@{ctx.author.id}>")
				# await member.kick(reason = reason)
				await ctx.send(embed = embed)


		def setup(bot):
			bot.add_cog(StaffCommands(bot))
