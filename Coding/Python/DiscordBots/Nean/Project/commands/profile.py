from datetime import datetime
import os
import discord
from discord.ext import commands
from Project.assets.Classes.Bank import Account, Bank
from PIL import Image, ImageFont, ImageDraw
import arabic_reshaper
from Project.assets.Classes.Profile import Profile, ProfilesManager
from Project.config import FONTENGPATH, FONTPATH, PROFILECHANNEL, SERVER_ICON, TEMPPROFILE
from bidi.algorithm import get_display
import requests
from io import BytesIO

def arabic_text(text: str):
  unicode_text = text
  unicode_text_reshaped = arabic_reshaper.reshape(unicode_text)
  unicode_text_reshaped_RTL = get_display(unicode_text_reshaped , base_dir='R')
  return unicode_text_reshaped_RTL

waiting_list = []
profileManager = ProfilesManager()
bank = Bank()

class profile(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @commands.command(name="هوية")
  async def scan(self, ctx: commands.Context):
    if ctx.channel.id == 800415415934124062:
      def check(message):
        return message.author.id == ctx.author.id
      member = ctx.author
      await ctx.send(f"{ctx.author.mention} الرجاء التوجة إلى الخاص")
      await member.send("الاسم الثلاثي؟ :")
      name = await self.bot.wait_for('message', check=check, timeout=40)
      await member.send("رقـم الـهـويـة؟ :")
      id = await self.bot.wait_for('message', check=check, timeout=40)
      await member.send("هـل انـت مـوضـف؟ :")
      staff = await self.bot.wait_for('message', check=check, timeout=40)
      await member.send("مـكـان الـمـيلاد؟ : ")
      place_of_birth = await self.bot.wait_for('message', check=check, timeout=40)
      await member.send("تـاريـخ الـمـيـلاد؟ :")
      date_of_birth = await self.bot.wait_for('message', check=check, timeout=40)
      await member.send("الـكـركـتر؟ :")
      character = await self.bot.wait_for('message', check=check, timeout=40)
      await member.send("الصورة؟ :")
      image = await self.bot.wait_for('message', check=check, timeout=40)
      await member.send('تم أرسال الهوية للأحوال المدنية')

      if len(image.attachments) > 0:
        attachment = image.attachments[0]
        if attachment.filename.endswith(".jpg") or attachment.filename.endswith(".jpeg") or attachment.filename.endswith(".png") or attachment.filename.endswith(".webp") or attachment.filename.endswith(".gif"):
          image = attachment.url
        elif "https://images-ext-1.discordapp.net" in image.content or "https://tenor.com/view/" in image.content:
          image = image.content

      embed = discord.Embed(title="طلب هوية مواطن", timestamp=datetime.now())
      embed.add_field(name="الاسم الثلاثي :", value=name.content)
      embed.add_field(name="رقم الهوية :", value=id.content)
      embed.add_field(name="هل انت موضف :", value=staff.content)
      embed.add_field(name="مكان الميلاد :", value=place_of_birth.content)
      embed.add_field(name="تاريخ الميلاد :", value=date_of_birth.content)
      embed.add_field(name="الكركتر :", value=character.content)
      embed.set_footer(text='ادارة الاحوال المدنية', icon_url=SERVER_ICON)
      embed.set_image(url=image)
      msg_to_add_rection = await self.bot.get_channel(PROFILECHANNEL).send(embed=embed)
      waiting_list.append({"message_id": msg_to_add_rection.id, "member": member, "name": name.content, "id": id.content, "staff": staff.content, "place_of_birth": place_of_birth.content, "date_of_birth": date_of_birth.content, "character": character.content, "image": image, "message": msg_to_add_rection})
      await msg_to_add_rection.add_reaction("✅")
      await msg_to_add_rection.add_reaction("❌")


  @commands.command(name="هويتي")
  async def my_profile(self, ctx: commands.Context):
    img = Image.open(TEMPPROFILE)
    text = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONTPATH, size=65)
    fonteng = ImageFont.truetype(FONTENGPATH, size=65)

    profile = profileManager.getProfileByMemberId(ctx.author.id)
    name = arabic_text(profile.getName())
    id = profile.getId()
    staff = arabic_text(profile.getStaff())
    place_of_birth = arabic_text(profile.getPlaceOfBirth())
    date_of_birth = profile.getDateOfBirth()
    character = arabic_text(profile.getCharacter())
    image = profile.getImage()

    text.text((900, 250),  name, fill=(255, 255, 255), font=font)
    text.text((1300, 400),  id, fill=(255, 255, 255), font=fonteng)
    text.text((1275, 475),  staff, fill=(255, 255, 255), font=font)
    text.text((1035, 600),  place_of_birth, fill=(255, 255, 255), font=font)
    text.text((1075, 750),  date_of_birth, fill=(255, 255, 255), font=fonteng)
    text.text((1275, 825),  character, fill=(255, 255, 255), font=font)
    
    im = Image.open(requests.get(image, stream=True).raw)
    im = im.resize((550, 550), Image.AFFINE)
    img.paste(im, (108, 242))
    
    img.save("profile.png")
    await ctx.send(file=discord.File("profile.png"))


  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    if user.id == self.bot.user.id:
      return
    # TODO: Make the members who doesn't have the role can't accept/unaccept it
    for i in waiting_list:
      if i["message_id"] == reaction.message.id:
        if reaction.emoji == "✅":
          # message = await client.get_channel(980964684146557009).send(f"&temp suffix {ss} {i['url']} 7")
          member = i["member"]
          message_to_edit = i["message"]
          await message_to_edit.clear_reactions()
          await message_to_edit.edit(content=f"{message_to_edit.content}\nتم قبول الهوية الوطنية من قبل {user.mention}")
          await member.send(f"تم قبول طلب الهوية الوطنية")
          del waiting_list[waiting_list.index(i)]
          # TODO: Create a profile class for it
          profile = Profile(i['name'], i['id'], i['staff'], i['place_of_birth'], i['date_of_birth'], i['character'], i['image'], member.id)
          profileManager.add_profile(profile)
          account = Account(profile, 5000)
          bank.add_account(account)
        elif reaction.emoji == "❌":  
          member = i["member"]
          message_to_edit = i["message"]
          await message_to_edit.clear_reactions()
          await message_to_edit.edit(content=f"{message_to_edit.content}\nتم رفض طلب الهوية الوطنية من قبل {user.mention}")
          await member.send("تم رفض طلب الهوية الوطنية !")
          del waiting_list[waiting_list.index(i)]

def setup(bot):
	bot.add_cog(profile(bot))