from datetime import datetime
import discord
from discord.ext import commands
import datetime
import discord
from discord.ext import commands
import json
from tabulate import tabulate
from PIL import Image, ImageFont, ImageDraw

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")

Voice_Members = {}
shutuped = []
Voice_Members_seconds = {}
XP_chat_dir = r"./XP_chat.json"
XP_voice_dir = r"./XP_voice.json"
chat_leaderboard_dir = r'./chat_leaderboard_temp.png'
font_dir = r'./Roboto-Regular.ttf'

@client.listen()
async def on_ready():
  print(f"{client.user} is ready!")
  with open(XP_chat_dir, 'r') as file:
    voice_data: dict = json.load(file)
  print(voice_data)
  print(voice_data[str(619340445692067890)])

# @client.slash_command(, name="topchatt", description="Get The XP For A User", usage="top_chatt <type>")
@commands.slash_command(guild_ids=[692158495235112972], name="top", description="Get The XP For A User", usage="top_chat <type (all, members, staffs)>")
async def top_chat(self, ctx, type: str = "all"):
  role = client.get_guild(692158495235112972).get_role(931185612348866600)
  with open(XP_chat_dir, 'r') as file:
    voice_data: dict = json.load(file)

  if type == "all":
    users_xp = list(voice_data.values())
    users_id = list(voice_data.keys())

  if type == "staff" or type == "Staff":
    users_xp = list(voice_data.values())
    users_id = list(voice_data.keys())
    users_id_staff = list()
    users_xp_staff = list()
    for i in role.members:
      if str(i.id) not in voice_data:
        continue
      v = 0
      users_id_staff.append(voice_data[str(i.id)][2])
      users_xp_staff.append(voice_data[str(i.id)])
      v +=1
      users_id = users_id_staff
      users_xp = users_xp_staff

  if type == "member" or type == "Member":
    users_xp = list(voice_data.values())
    users_id = list(voice_data.keys())
    users_id_member = list()
    users_xp_member = list()
    for i in role.members:
      if str(i.id) in voice_data:
        del voice_data[str(i.id)]
    for i in voice_data:
      users_id_member.append(voice_data[str(i)][2])
      users_xp_member.append(voice_data[str(i)])
    users_id = users_id_member
    users_xp = users_xp_member

  if type != "all" and type != "staff" and type != "member":
    await ctx.respond("Please Enter A Valid Type (all, staff, member)")
    return

  new_list = []

  for i, user_id in enumerate(users_id, 1):
    new_list.append([user_id, users_xp[i - 1]])

  new_list.sort(key = lambda x: x[1], reverse = True)

  user_rank = []
  user_name = []
  user_xp = []

  for i, user_id in enumerate(new_list[:10]):
    user_name.append([f"{await client.fetch_user(int(user_id[0]))} ({user_id[1][1]})"])
    user_xp.append([user_id[1][0]])
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
  rank_time_spent_text_position = 925, 50

  # Draws
  draw_on_image = ImageDraw.Draw(image_template)
  draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
  draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
  draw_on_image.text(rank_time_spent_text_position, user_time_spent_table, 'white', font=font)

  # Save image
  image_template.convert('RGB').save('chat_leaderboard.jpg', 'JPEG')

  await ctx.respond(file=discord.File('chat_leaderboard.jpg'))

@client.listen()
async def on_message(message: discord.Message):
  if message.author.bot:
    return

  if message.content.startswith("!"):
    return

  if message.author:
    if message.author.roles:
      roles = message.author.roles
      role_for_check = client.get_guild(692158495235112972).get_role(931185612348866600)

  with open(XP_chat_dir, 'r') as file:
    chat_data = json.load(file)
    new_user = str(message.author.id)
    if new_user in chat_data:
      if role_for_check in roles:
        print(f"Adding XP for staff {message.author.name}")
        chat_data[new_user][0] += 1
        chat_data[new_user][1] = "Staff"
        with open(XP_chat_dir, 'w') as update_user_data:
          json.dump(chat_data, update_user_data, indent=4)
      else:
        print(f"Adding XP for member {message.author.name}")
        chat_data[new_user][0] += 1
        chat_data[new_user][1] = "Member"
        with open(XP_chat_dir, 'w') as update_user_data:
          json.dump(chat_data, update_user_data, indent=4)
    else:
      if role_for_check in roles:
        print(f"Creating XP for staff {message.author.name}")
        chat_data[new_user] = 1, "Staff", message.author.id
        with open(XP_chat_dir, 'w') as new_user_data:
          json.dump(chat_data, new_user_data, indent=4)
      else:
        print(f"Creating XP for member {message.author.name}")
        chat_data[new_user] = 1, "Member", message.author.id
        with open(XP_chat_dir, 'w') as new_user_data:
          json.dump(chat_data, new_user_data, indent=4)

client.run("ODE2Nzg2MDUzMDI4NTExODA2.GLSwRi.M3oLK6Vz0ARLCs2hjHz9tO002aD4mDQo4MPcXI")
# token "OTgwMjQ4MDg3OTgzNDU2MzQ3.GasG2v.u2OvvHCtovGJ-NB8sBQxriYpBiPoU0Ka2UNnLQ"