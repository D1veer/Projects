import asyncio
import datetime
from cv2 import imshow
import discord
from discord.ext import commands
import mysql.connector
from tabulate import tabulate
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")
# c = mysql.connector.connect(host='144.172.80.241',
#                             database='test',
#                             user='u20710_ewWNLyYwnV',
#                             password='SUkhKhXk9A8+c6y3RQ^.+!u1')

# print(c.is_connected())

# conn = c.cursor()
# sql = "DELETE FROM Member_ids WHERE Name = 'xiled'"

# conn.execute(sql)

# c.commit()

# sql = "INSERT INTO Member_ids (Name, id) VALUES (%s, %s)"
# val = ("yosef", 23223)
# conn.execute(sql, val)

# c.commit()

# conn.execute("SELECT * FROM Member_ids")
# myresult = conn.fetchall()

# for x in myresult:
#     print(x)

connection = None
test = {}
sniped_messages = {}

@client.event
async def on_message_delete(message):
	if range(len(sniped_messages)) == 3:
		del sniped_messages[-1]
	history = sniped_messages.get(message.channel.id, [])
	history.insert(0, message)
	sniped_messages[message.channel.id] = history

@client.command()
async def snipe(ctx, *, page: int = 1):
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
	embed.set_footer(text=f"{client.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
	await ctx.send(embed=embed)


@client.event
async def on_ready():
	print("Bot is ready!")
	# role = client.get_guild(692158495235112972).get_role(931185612348866600)
	# names = []
	# ids = []
	# avatarlink = []
	# for i in role.members:
	#     names.append([f"{i.name}#{i.discriminator}"])
	#     ids.append([i.id])
	#     avatarlink.append([i.id])
	# user_name_table = tabulate(names, tablefmt='plain', headers=['ID\n'], numalign='left')
	# user_id_table = tabulate(ids, tablefmt='plain', headers=['Name\n'], numalign='left')
	# user_avatar_table = tabulate(avatarlink, tablefmt='plain', headers=['\n'], numalign='left')

	# image_template = Image.open('STUFF\\assets\\images\\voice_leaderboard_temp.png')

	# # # Font
	# font = ImageFont.truetype('STUFF\\assets\\fonts\\Roboto-Regular.ttf', 14)

	# # # Positions
	# rank_text_position = 30, 50
	# name_text_position = 80, 50
	# rank_time_spent_text_position = 330, 50

	# # # Draws
	# draw_on_image = ImageDraw.Draw(image_template)
	# draw_on_image.text(rank_text_position, user_name_table, 'white', font=font)
	# draw_on_image.text(name_text_position, user_id_table, 'white', font=font)
	# draw_on_image.text(rank_time_spent_text_position, user_avatar_table, 'white', font=font)

	# # # Save image
	# image_template.convert('RGB').save('voice_leaderboard.jpg', 'JPEG')
	# imshow(image_template, 1)
	# c = mysql.connector.connect(host='144.172.80.241',
	#     database='s20710_Minecraft_Discord',
	#     user='u20710_ewWNLyYwnV',
	#     password='SUkhKhXk9A8+c6y3RQ^.+!u1')
	# conn = c.cursor()
	# conn.execute("SELECT * FROM Member_ids")
	# # sql = "INSERT INTO Member_ids (Name, id) VALUES (%s, %s)"
	# # val = ("dive/er040", 123124214)
	# myresult = conn.fetchall()
	# # myresult = conn.execute(sql, val)
	# # c.commit()
	# print(myresult)
	# if 123124214 in myresult:
	#     print("found")
	# for i in myresult:
	#     print(i[1])
	#     if 123124214 == i[1]:
	#         print("found")
	#         break
	#     print(type(i))



# client.load_extension("Admin")
# client.load_extension("StaffCommands")
# client.load_extension("events")
# client.load_extension("VoiceCommands")
client.run("ODE2Nzg2MDUzMDI4NTExODA2.YEABSg.hVozpmO0aDQE7MDPrfV8Eqafaks")