import discord
from discord.ext import commands
from discord.commands import Option, OptionChoice
from project.utils.DB import add_member, clear, get_member_xp, get_top
from ..config import FONT_DIR, STAFF_ROLE_ID, LEADERBOARD_TEMP
from string import punctuation
from tabulate import tabulate
from PIL import Image, ImageFont, ImageDraw


class leaderboard(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @commands.slash_command(name='top')
  async def top_members(self, ctx: discord.ApplicationContext, _type: Option(str, 'Choose The Type', required=True, choices=[OptionChoice('Staff', 'staff'), OptionChoice('Members', 'members'), OptionChoice('All', 'all')])):
    members = get_top(str(_type), 10)
    if members == None or len(members) == 0: return await ctx.send_response('No Members Found!', ephemeral=True)
    ranks = []
    usernames = []
    xp = []
    for i, v in enumerate(members): 
      ranks.append([i+1])
      usernames.append([f'{await self.bot.get_or_fetch_user(v["id"])} {"(Staff)" if v["staff"]==True else "(Member)"}'])
      xp.append([v['xp']])

    user_rank_table = tabulate(ranks, tablefmt='plain', headers=['#\n'], numalign='left')
    user_name_table = tabulate(usernames, tablefmt='plain', headers=['Name\n'], numalign='left')
    user_time_spent_table = tabulate(xp, tablefmt='plain', headers=['XP\n'],numalign='left')

    image_template = Image.open(LEADERBOARD_TEMP)

    # Font
    font = ImageFont.truetype(FONT_DIR, 38)

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

    await ctx.send_response(file=discord.File('chat_leaderboard.jpg'))

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
    if message.content.startswith('--'):
      command = message.content.split(' ')
      if command[0] == '--top':
        members = get_top(str(command[1]), int(command[2]))
        
        msg = '--topis'
        for i in members:
          msg = msg + ' ' + str(i['id'])
        await message.channel.send(msg)
      elif command[0] == '--leaderboard' and command[1] == 'reset':
        # ! Reset The Leaderboard
        clear()
        await message.channel.send('Resetted The Database...')

    if message.content.startswith(punctuation):
      return
    if message.author.bot:
      return
    id = message.author.id
    role = message.guild.get_role(STAFF_ROLE_ID)
    staff = False
    if role in message.author.roles:
      staff = True
    add_member(id, get_member_xp(id)+1, staff)


def setup(bot):
  bot.add_cog(leaderboard(bot))
