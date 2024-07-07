from datetime import datetime
import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import arabic_reshaper
import requests
from ..Classes.Bank import Account, BANK
from ..Classes.Profile import Profile, PROFILES_MANAGER
from ..config import FONTENGPATH, FONTPATH, PROFILECHANNEL, SERVER_ICON, SERVER_ID, SERVER_NAME, TEMPPROFILE
from bidi.algorithm import get_display

waiting_list = []

class profile(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @commands.command(name="هوية")
  async def scan(self, ctx: commands.Context):
    if PROFILES_MANAGER.getProfileByMemberId(ctx.author.id) != None:
      await ctx.reply("__أنت تمتلك هوية بالفعل !__")
      return
    if ctx.channel.id == 800415415934124062:
      def check(message):
        return message.author.id == ctx.author.id
      member = ctx.author
      try:
        await member.send("الاسم الثلاثي؟ :")
        await ctx.send(f"{ctx.author.mention} الرجاء التوجة إلى الخاص")
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
        
      except Exception as e:
        if '403' in str(e):
          await ctx.reply("الرجاء فتح الخاص.")

  @commands.command(name="هويتي")
  async def my_profile(self, ctx: commands.Context):
    if PROFILES_MANAGER.getProfileByMemberId(ctx.author.id) != None:
      img = Image.open(TEMPPROFILE)
      text = ImageDraw.Draw(img)
      font = ImageFont.truetype(FONTPATH, size=65)
      fonteng = ImageFont.truetype(FONTENGPATH, size=65)

      profile = PROFILES_MANAGER.getProfileByMemberId(ctx.author.id)
      name =  "الاسم الثلاثي: " + profile.getName()
      id = profile.getId()
      staff = profile.getStaff()
      place_of_birth = profile.getPlaceOfBirth()
      date_of_birth = profile.getDateOfBirth()
      character = profile.getCharacter()
      image = profile.getImage()

      text.text((250, 250),  name, fill=(255, 255, 255), font=font)
      # text.text((1300, 400),  id, fill=(255, 255, 255), font=fonteng)
      # text.text((1275, 475),  staff, fill=(255, 255, 255), direction='ltr', font=font)
      # text.text((1035, 600),  place_of_birth, fill=(255, 255, 255), direction='ltr', font=font)
      # text.text((1075, 750),  date_of_birth, fill=(255, 255, 255), font=fonteng)
      # text.text((1275, 825),  character, fill=(255, 255, 255), direction='ltr', font=font)
      
      # im = Image.open(requests.get(image, stream=True).raw)
      # im = im.resize((550, 550), Image.AFFINE)
      # img.paste(im, (108, 242))
      
      img.save("profile.png")
      await ctx.send(file=discord.File("profile.png"))
    else:
      await ctx.reply("__لا تمتلك هوية__")

  @commands.command(name="الغاء")
  async def cancelProfile(self, ctx: commands.Context, types = None, member: discord.Member = None):
    if types == "هوية":
      if member != None:
        profile = PROFILES_MANAGER.getProfileByMemberId(member.id)
        PROFILES_MANAGER.remove_profile(profile)
        await member.send("تم الغاء هويتك.")
      else:
        return await ctx.send("يرجى تحديد شخص")
    elif types == None:
      pass

  @commands.Cog.listener()
  async def on_message(self, message: discord.Message):
    if message.content.startswith("هوية"):
      if '#' in message.content:
        id = message.content.lstrip('هوية#')
        profile = PROFILES_MANAGER.getProfileById(id)
        if profile != None:
          msg = f'''
          
            **| الـهـويـة تـابـعـة لـ : <@{profile.getMemberId()}>**

            **| رقم الهوية الوطنية : {profile.getId()}**

            **| حـالـة الـهـويـة : تم الحصول عليها**
          
          
          '''
          await message.channel.send(msg)
        else:
          return await message.channel.send("__لم يتم الحصول على الهوية__")
      else:
        return await message.channel.send('__يرجى تحديد رقم الهوية__')

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
          await member.send(f"__تم قبول طلب الهوية الوطنية__")
          del waiting_list[waiting_list.index(i)]
          # TODO: Create a profile class for it
          profile = Profile(i['name'], i['id'], i['staff'], i['place_of_birth'], i['date_of_birth'], i['character'], i['image'], member.id)
          PROFILES_MANAGER.add_profile(profile)
          account: Account = Account(profile.getId(), 5000, 0, False)
          BANK.add_account(account)
        elif reaction.emoji == "❌":  
          member = i["member"]
          message_to_edit = i["message"]
          await message_to_edit.clear_reactions()
          await message_to_edit.edit(content=f"{message_to_edit.content}\nتم رفض طلب الهوية الوطنية من قبل {user.mention}")
          await member.send("__تم رفض طلب الهوية الوطنية !__")
          del waiting_list[waiting_list.index(i)]

def setup(bot):
	bot.add_cog(profile(bot))