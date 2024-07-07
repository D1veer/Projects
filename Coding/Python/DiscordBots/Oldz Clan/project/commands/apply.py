from datetime import datetime
import discord
from discord.ext import commands
from ..config import *
import sqlite3

waiting_messages = []

db = sqlite3.connect("MEMBERS.db")
c = db.cursor()
sql = """
CREATE TABLE IF NOT EXISTS MEMBERS
(NAME TEXT, AGE INT, IGN TEXT, DV TEXT, CPS INT, INPUT TEXT, SEVERS TEXT, TIME TEXT, MI INT)"""
c.execute(sql)


def addMember(NAME: str, AGE, IGN, DV, CPS, INPUT, SERVERS, TIME, MI):
  data = getUser(MI)
  if data != None:
    return [False, data]
  prams = (NAME.encode("UTF-8"), AGE, IGN, DV, CPS, INPUT, SERVERS, TIME, MI)
  sql = f"insert into MEMBERS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
  c.execute(sql, prams)
  db.commit()
  return True

def getUser(MI):
  c.execute("SELECT MI FROM MEMBERS WHERE MI = ?", (MI,))
  data = c.fetchone()
  return data


class apply(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @commands.command(name='staff')
  async def staffList(self, ctx: commands.Context):
    staffs = []
    role = ctx.guild.get_role(992365642877517844)
    embed = discord.Embed(title='Staff List', timestamp=datetime.now(), color=discord.Color.yellow())
    for i in role.members:
      staffs.append(f'{i.name}#{i.discriminator}')
    allstaff = ", ".join(staffs)
    embed.description = f">>> ```{allstaff}``` \n {len(role.members)} staff"
    await ctx.send(embed=embed)
  
  @commands.command(name='apply')
  async def apply(self, ctx: commands.Context, type = None):
    member = ctx.author
    if type is None:
      data = getUser(member.id)
      if data != None:
        return await ctx.send('__You Already Applied !__')
      await ctx.reply(">>> __Please Check Your DMs.__")
      def check(message):
        return message.author.id == ctx.author.id
      await member.send('اسمك :')
      name = await self.bot.wait_for('message', check=check, timeout=20)
      await member.send('عمرك :')
      age = await self.bot.wait_for('message', check=check, timeout=20)
      await member.send('اسمك باللعبه :')
      ign = await self.bot.wait_for('message', check=check, timeout=20)
      await member.send('جهازك :')
      dev = await self.bot.wait_for('message', check=check, timeout=20)
      await member.send('ضرباتك في الثانيه (CPS) :')
      cps = await self.bot.wait_for('message', check=check, timeout=20)
      await member.send('تستخدم ماوس ولا يد؟ :')
      Input = await self.bot.wait_for('message', check=check, timeout=20)
      await member.send('السيرفرات الي تلعبها  :')
      servers = await self.bot.wait_for('message', check=check, timeout=40)
      await member.send('متى تبي نختبرك :')
      when = await self.bot.wait_for('message', check=check, timeout=20)
      await member.send("تم إرسال طلبك للأدارة، الرجاء الانتظار.")

      embed = discord.Embed(title='تقديم على عضوية الكلان', timestamp=datetime.now())
      embed.set_footer(text=F'{SERVER_NAME}', icon_url=SERVER_ICON)
      embed.add_field(name='الاسم : ', value=f'{name.content}')
      embed.add_field(name='العمر : ', value=f'{age.content}')
      embed.add_field(name='الاسم في اللعبة :', value=f'{ign.content}')
      embed.add_field(name="الجهاز : ", value=f'{dev.content}')
      embed.add_field(name="كم ضربة في ثانية (CPS) : ", value=f'{cps.content}')
      embed.add_field(name="ماوس ولا يد : ", value=f'{Input.content}')
      embed.add_field(name="السيرفرات اللي يلعب فيها : ", value=f'{servers.content}')
      embed.add_field(name="متي تبي اختبارك : ", value=f'{when.content}')
      msg = await self.bot.get_channel(996660847034257538).send(embed=embed)
      await msg.add_reaction("✅")
      await msg.add_reaction("❎")
      waiting_messages.append({"message_id": msg.id, "member": member, "name": name.content, "age": age.content, "ign": ign.content, "dev": dev.content, "cps": cps.content, "Input": Input.content, "servers": servers.content, "when": when.content,"message": msg})

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    if user.id == self.bot.user.id:
      return
    for i in waiting_messages:
      if i["message_id"] == reaction.message.id:
        if reaction.emoji == "✅":
          member = i["member"]
          message_to_edit = i["message"]
          await message_to_edit.clear_reactions()
          await message_to_edit.edit(content=f"{message_to_edit.content}\nتم قبول الطلب من قبل {user.mention}")
          await member.send('__! تم قبول الطلب__')
          del waiting_messages[waiting_messages.index(i)]
          addMember(i['name'], i['age'], i['ign'], i['dev'], i['cps'], i['Input'], i['servers'], i['when'], member.id)
        elif reaction.emoji == "❎":  
          member = i["member"]
          message_to_edit = i["message"]
          await message_to_edit.clear_reactions()
          await message_to_edit.edit(content=f"{message_to_edit.content}\nتم رفض الطلب من قبل {user.mention}")
          await member.send("__تم رفض طلبك !__")
          del waiting_messages[waiting_messages.index(i)]




def setup(bot):
	bot.add_cog(apply(bot))