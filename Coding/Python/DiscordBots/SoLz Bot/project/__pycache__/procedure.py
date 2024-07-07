import datetime
import discord
from discord.ext import commands
from .utils import Classprocedure as Procedure
from ..config import *
import json
from tabulate import tabulate
from PIL import Image, ImageFont, ImageDraw


procedureMananger = Procedure.ProcedureManager()

def save_procedure(procedure: Procedure.Procedure):
    # TODO: Make the procedure a json object
  with open(PROCEDUREDATABASE, "r") as f:
    data = json.load(f)
  data[procedure.get_id()] = procedure.to_json()
  with open(PROCEDUREDATABASE, 'w') as new_user_data:
    json.dump(data, new_user_data, indent=4)


class procedure(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot

  # @commands.command(name="add", aliases=["new", "create"])
  async def procedure_def_add(self, ctx: commands.Context, member, reason, procedure, duration):
    global acmember
    if isinstance(member, str):
      if member[-1] == ">":
        acmember = member.replace(">", "")
        acmember = acmember.replace("<", "")
        acmember = acmember.replace("@", "")
        print(acmember)
        acmember = await self.bot.fetch_user(int(acmember))
        await acmember.send(f"You have been get proof for {reason}, Procedure: {procedure}, Duration: {duration}, By {ctx.author.mention}.")
    attamnts = []
    print(member, reason, procedure, duration, attamnts, ctx.author)
    procedure = Procedure.Procedure(ctx.author.id, acmember.id, reason, procedure, duration, procedureMananger.get_procedure_count(), attamnts, datetime.datetime.now())
    procedureMananger.add_procedure(procedure)
    save_procedure(procedure)
    await ctx.send(f"<a:Mark:981345811927543889> {ctx.author.mention} added a Proof for <@{acmember.id}>.")
    embed = procedure.to_embed()
    for i in ctx.message.attachments:
      attamnts.append(i.url)
      embed.set_image(url=i.url)
    await ctx.send(embed=embed)

  @commands.command(name="get", aliases=["show"])
  async def procedure_def_get(self, ctx: commands.Context, type, text):
    await ctx.send(f"<a:Loading:981347003697090590> Getting Proof by {type} with {str(text)}")
    if type == "id":
      procedure = procedureMananger.get_procedure_by_id(int(text))
      if procedure is None:
        await ctx.send(f"<a:X_:981346307572658246> {ctx.author.mention} no procedure with id {text}.")
      else:
        await ctx.send(embed=procedure.to_embed())
    elif type == "member":
      if isinstance(text, str):
        if text[-1] == ">":
          acmember = text.replace(">", "")
          acmember = acmember.replace("<", "")
          acmember = acmember.replace("@", "")
      procedure = procedureMananger.get_procedure_by_member(int(acmember))
      if procedure is None:
        await ctx.send(f"<a:X_:981346307572658246> {ctx.author.mention} no Proofs for <@{acmember}>.")
      else:
        await ctx.send(embed=procedure.to_embed())
    elif type == "staff":
      newText = text.replace("<", "")
      newText = newText.replace(">", "")
      newText = newText.replace("@", "")
      if "!" in newText:
        newText = newText.replace("!", "")
      staff = self.bot.get_user(int(newText))
      procedure = procedureMananger.get_procedure_by_staff(newText)
      if procedure is None:
        await ctx.send(f"<a:X_:981346307572658246> {ctx.author.mention} no Proofs for <@{newText}>.")
      else:
        await ctx.send(embed=procedure.to_embed())

  @commands.command(name="remove", aliases=["delete"])
  async def procedure_def_remove(self, ctx: commands.Context, text, member):
    if text == "all":
      if member[-1] == ">":
        acmember = member.replace(">", "")
        acmember = acmember.replace("<", "")
        acmember = acmember.replace("@", "")
      procedures = procedureMananger.get_procedures_by_member(int(acmember))
      print(procedures)
      for i in procedures:
        procedureMananger.remove_procedure(i)
      await ctx.send(f"<a:Mark:981345811927543889> {ctx.author.mention} removed all Proofs.")
    else:
      procedure = procedureMananger.get_procedure_by_id(int(member))
      if procedure is None:
        await ctx.send(f"<a:X_:981346307572658246> {ctx.author.mention} no procedure with id {text}.")
      else:
        procedureMananger.remove_procedure(procedure)
        await ctx.send(f"<a:Mark:981345811927543889> {ctx.author.mention} removed a Proof from <@{procedure.get_member()}>.")

  @commands.command(name="list", aliases=["all"])
  async def procedure_def_list(self, ctx: commands.Context, member: discord.Member = None):
    if member is not None:
      await ctx.send(f"<a:Loading:981347003697090590> Getting all Proofs For {member.mention}")
      procedures = procedureMananger.get_procedures_by_member(member.id)
      embed = discord.Embed(title=f"All Proofs For {member.display_name} ({len(procedures)})", color=0x00ff00)
      v = 0
      for procedure in procedures:
        if v != 10:
          if (len(procedures) - 1) == v:
            values = f"""
            🆔 Warn Id ({procedure.get_id()}) - By <@{procedure.get_staff()}>
            ⚠️ User: <@{procedure.get_member()}>
            📝 Reason : `{procedure.get_reason()}`
            __***try !get***__"""
          else:
            values = f"""
            🆔 Warn Id ({procedure.get_id()}) - By <@{procedure.get_staff()}>
            ⚠️ User: <@{procedure.get_member()}>
            📝 Reason : `{procedure.get_reason()}`
            ──────────────────────"""
          time = datetime.datetime.strptime(procedure.get_time(), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %I:%M:%S %p")
          embed.add_field(name=f"⏲️ {time}", value=values, inline=False)
          v += 1
      embed.timestamp = datetime.datetime.now()
      embed.set_footer(text=f"{SERVER_NAME}", icon_url=SERVER_ICON)
      await ctx.send(embed=embed)
    else:
      await ctx.send(f"<a:X_:981346307572658246> No Proofs Found.")

  @commands.command(name="top_proofs", aliases=["tp", "tpf"])
  async def procedure_def_top_proofs(self, ctx: commands.Context):
    await ctx.send(f"<a:Loading:981347003697090590> Getting Top Proofs")
    with open(MEMBERSDATABASE, "r") as f:
      data = json.load(f)
    users_xp = list(data.values())
    users_id = list(data.keys())
    
    top_proofs = []

    for i, user_id in enumerate(users_id, 1):
      top_proofs.append([user_id, users_xp[i - 1]])

    top_proofs.sort(key = lambda x: x[1]['procedures_count'], reverse = True)
    user_rank = []
    user_name = []
    user_xp = []

    for i, user_id in enumerate(top_proofs[:10]):
      user_name.append([f"{await self.bot.fetch_user(int(user_id[0]))}"])
      user_xp.append([user_id[1]["procedures_count"]])
      user_rank.append([i + 1])

    # Append column to table
    user_rank_table = tabulate(user_rank, tablefmt='plain', headers=['#\n'], numalign='left')
    user_name_table = tabulate(user_name, tablefmt='plain', headers=['Name\n'], numalign='left')
    user_time_spent_table = tabulate(user_xp, tablefmt='plain', headers=['Proofs\n'],numalign='left')

    image_template = Image.open(TOP_TEMPALTE)

    # Font
    font = ImageFont.truetype(FONT_DIR, 150)

    # Positions
    rank_text_position = 75, 50
    name_text_position = 275, 50
    rank_time_spent_text_position = 1225, 50

    # Draws
    draw_on_image = ImageDraw.Draw(image_template)
    draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
    draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
    draw_on_image.text(rank_time_spent_text_position, user_time_spent_table, 'white', font=font)

    # Save image
    image_template.convert('RGB').save('chat_leaderboard.jpg', 'JPEG')

    await ctx.send(file=discord.File('chat_leaderboard.jpg'))

def setup(bot):
	bot.add_cog(procedure(bot))