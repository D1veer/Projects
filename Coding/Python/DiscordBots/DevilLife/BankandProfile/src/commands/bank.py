from datetime import datetime
import discord
from discord.ext import commands
from ..Classes.Bank import Account, BANK
from ..Classes.Profile import Profile, PROFILES_MANAGER
from ..config import FONTENGPATH, FONTPATH, PROFILECHANNEL, SERVER_ICON, SERVER_ID, SERVER_NAME, TEMPPROFILE


class bank(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot

  @commands.command("فلوسي")
  async def my_money(self, ctx: commands.Context, member: discord.Member = None):
    if member == None:
      member = ctx.author
    print(PROFILES_MANAGER.getProfileByMemberId(member.id))
    if PROFILES_MANAGER.getProfileByMemberId(member.id) == None:
      await ctx.send("__لا يوجد لديك حساب بنكي.__")
      return
    
    profile = PROFILES_MANAGER.getProfileByMemberId(member.id)
    account = BANK.getAccountById(profile.getId())
    total = account.getCash() + account.getMoney()

    msg = f'''
    ━━━━━━━━━━  
    <a:954789654647943199:996049263979147386> **| العميل :** {member.mention}

    <a:954789654647943199:996049263979147386> **| الكاش :** __**{account.getCash()}**__ **﷼ **

    <a:954789654647943199:996049263979147386> **| البنك :** __**{account.getMoney()}**__ **﷼ **

    <a:954789654647943199:996049263979147386> **| الاجمالي :** __**{total}**__ **﷼ **
    '''
    
    # <a:954789654647943199:996049263979147386>  | **الكاش** : __{account.getCash()}__ ريال­
    
    # <a:954789654647943199:996049263979147386>  | **البنك ** : __{account.getMoney()}__ ريال
    
    # <a:954789654647943199:996049263979147386>  | **الاجمالي** : __{total}__ ريال
    #  description=msg,
    embed = discord.Embed(description=msg, color=discord.Color.dark_red())
    embed.set_author(name="𝗗𝗘𝗩𝗜𝗟 𝗟𝗜𝗙𝗘", icon_url=f"{self.bot.user.display_avatar}")
    embed.set_footer(text=f'بنك ديـفـل لآيــف المركزي', icon_url="https://cdn.discordapp.com/icons/954771483866071122/a_66bb82b6dc88bdeff6f1c5f1d365a64a.gif?size=32")
    embed.set_thumbnail(url=f'https://cdn.discordapp.com/icons/954771483866071122/a_66bb82b6dc88bdeff6f1c5f1d365a64a.gif?size=128')
    # embed.add_field(name=f'­', value=f'<a:954789654647943199:996049263979147386> **| العميل :** {member.mention}', inline=False)
    # embed.add_field(name=f'<a:954789654647943199:996049263979147386> | **الكاش** :', value=f'SAR __{account.getCash()}__ ', inline=False)
    # embed.add_field(name=f'', value=f'', inline=False)
    # embed.add_field(name=f' | **الاجمالي** :', value=f'SAR __{total}__ ', inline=False)
    # embed.add_field(name='<a:954789654647943199:996049263979147386> | **Cash** :', value=f'__{total}__ ريال', inline=False)
    # embed.add_field(name='<a:954789654647943199:996049263979147386> | **Bank** :', value=f'__{total}__ ريال', inline=False)
    # embed.add_field(name='<a:954789654647943199:996049263979147386> | **Total** :', value=f'__{total}__ ريال', inline=False)
    # embed.add_field(name='<a:954789654647943199:996049263979147386> | **الكاش** :', value=f'__{account.getCash()}__ ريال')
    # embed.s

    await ctx.send(embed=embed)

  @commands.command(name='سحب')
  async def withdraw(self, ctx: commands.Context, member = None, amount = None):
    role = ctx.guild.get_role(791680372966293504)
    Withdrawtype = ""
    if member == None:
      return await ctx.reply("__يرجى تحديد مبلغ السحب__")
    if "@" in member:
      if ~(role in ctx.author.roles):
        await ctx.send("__ليس لديك الصلاحية.__")
        return
      member = await ctx.guild.fetch_member(member)
      profile = PROFILES_MANAGER.getProfileByMemberId(member_id=member.id)
      amount = amount
      Withdrawtype = "From Mebmer"
    else:
      profile = PROFILES_MANAGER.getProfileByMemberId(ctx.author.id)
      amount = member
      Withdrawtype = "From Himself"
    
    print(amount, member)
    
    if profile == False:
      if Withdrawtype == "From Himself":
        await ctx.send("__لا يوجد لديك حساب بنكي.__")
      elif Withdrawtype == "From Mebmer":
        await ctx.send("__لا يوجد لديه حساب بنكي.__")
      return

    account = BANK.getAccountById(profile.getId())
    print(member, amount)
    if amount != None:
      amount = int(amount)
      if amount <= account.getMoney():
        if account.getFreeze(): return await ctx.send("__الحساب مجمد !__")
        account.addCash(amount)
        account.delMoney(amount)
        embed=discord.Embed(title="تنبيه بسحب الرصيد", color=0x37ff00, timestamp=datetime.now())
        embed.add_field(name="تم سحب من رصيد الحساب المبلغ ادناه", value=f"{amount} ريال", inline=False)
        embed.set_footer(text='البنك المركزي', icon_url=SERVER_ICON)
        await ctx.send(embed=embed)
        BANK.update(account)
      else:
        await ctx.reply("__الرصيد لا يسمح__")
    else:
      print(member, amount, type(member), type(amount))
      await ctx.reply("__يرجى تحديد مبلغ السحب__")

  @commands.command(name='ايداع')
  async def deipost(self, ctx: commands.Context, amount=None):
    profile = PROFILES_MANAGER.getProfileByMemberId(ctx.author.id)
    
    if profile == False:
      await ctx.send("__لا يوجد لديك حساب بنكي.__")
      return

    account = BANK.getAccountById(profile.getId())
    if amount != None:
      amount = int(amount)
      if amount <= account.getCash():
        if account.getFreeze(): return await ctx.send("__الحساب مجمد !__")
        account.addMoney(amount)
        account.delCash(amount)
        embed=discord.Embed(title="تنبيه ايداع للرصيد", color=0x37ff00, timestamp=datetime.now())
        embed.add_field(name="تم ايداع مبلغ للرصيد قدره", value=f"{amount} ريال", inline=False)
        embed.set_footer(text='البنك المركزي', icon_url=SERVER_ICON)
        await ctx.send(embed=embed)
        BANK.update(account)
      else:
        await ctx.reply("__الرصيد لا يسمح__")
    else:
      await ctx.reply("__يرجى تحديد مبلغ السحب")

  @commands.command(name='تحويل')
  async def transfer(self, ctx, type, member: discord.Member=None, amount=None):
    if type == "بنكي":
      if member is None:
        return await ctx.send("__يرجى تحديد شخص للتحويل__")
      if amount is None:
        return await ctx.send("__يرجى تحديد المبلغ للتحويل__")
      profile = PROFILES_MANAGER.getProfileByMemberId(ctx.author.id)
      memberprofile = PROFILES_MANAGER.getProfileByMemberId(member.id)

      if profile == False:
        await ctx.send("__لا يوجد لديك حساب بنكي.__")
        return
      
      if memberprofile == False:
        await ctx.send("__لا يوجد حساب بنكي للشخص المحول له.__")
        return

      account = BANK.getAccountById(profile.getId())
      memberaccount = BANK.getAccountById(memberprofile.getId())


    amount = int(amount)
    if amount <= account.getMoney():
      if account.getFreeze(): return await ctx.send("__الحساب مجمد !__")
      account.delMoney(amount)
      memberaccount.addMoney(amount)

      msg = f'''
      تحويل مبلغ
      
      العميل : {ctx.author.mention}
      
      الشخص الذي تم تحويل المبلغ له : {member.mention}

      المبلغ المحول : {amount} ريال
      '''

      embed=discord.Embed(title="تحويل مبلغ مالي", color=0x37ff00, description=msg, timestamp=datetime.now())
      embed.set_footer(text='البنك المركزي', icon_url=SERVER_ICON)
      await ctx.send(embed=embed)
      BANK.update(account)
      BANK.update(memberaccount)
    else:
      await ctx.reply("__الرصيد لا يسمح__")

  @commands.command(name='اعطاء')
  async def give(self, ctx, type, member: discord.Member, amount):
    if type == "كاش":
      profile = PROFILES_MANAGER.getProfileByMemberId(ctx.author.id)
      memberprofile = PROFILES_MANAGER.getProfileByMemberId(member.id)

      if profile == False:
        await ctx.send("__لا يوجد لديك حساب بنكي.__")
        return
      
      if memberprofile == False:
        await ctx.send("__لا يوجد حساب بنكي للشخص المحول له.__")
        return

      account = BANK.getAccountById(profile.getId())
      memberaccount = BANK.getAccountById(memberprofile.getId())


      amount = int(amount)
      if amount <= account.getCash():
        if account.getFreeze(): return await ctx.send("__الحساب مجمد !__")
        account.delCash(amount)
        memberaccount.addCash(amount)

        msg = f'''
        أعطاء مبلغ
        
        العميل : {member.mention}
        
        الشخص الذي تم اعطائه المبلغ له : {ctx.author.mention}

        المبلغ المعطى : {amount} ريال
        '''

        embed=discord.Embed(title="اعطاء مبلغ مالي", color=0x37ff00, description=msg, timestamp=datetime.now())
        embed.set_footer(text='البنك المركزي', icon_url=SERVER_ICON)
        await ctx.send(embed=embed)
        BANK.update(account)
        BANK.update(memberaccount)
      else:
        await ctx.reply("__الرصيد لا يسمح__")

  @commands.command(name="تصفير")
  async def zero(self, ctx, user: str):
    if '&' in user:
      # NOTE: its a role
      id = user[3:-1]
      guild = ctx.message.guild
      role = guild.get_role(int(id))
      for i in role.members:
        if ~i.bot:
          if PROFILES_MANAGER.getProfileByMemberId(i.id) != False:
            account = BANK.getAccountById(PROFILES_MANAGER.getProfileByMemberId(i.id).getId())
            account.setCash(0)
            account.setMoney(0)
            BANK.update(account=account)
      await ctx.send(f"__تم تصفير جميع من يملك الرتبه {len(role.members)} عضو تم تصفيره__")
    elif '@' in user:
      id = user[2:-1]
      member = await self.bot.get_or_fetch_user(id)
      if PROFILES_MANAGER.getProfileByMemberId(member.id) != None:
        account = BANK.getAccountById(PROFILES_MANAGER.getProfileByMemberId(member.id).getId())
        account.setCash(0)
        account.setMoney(0)
        BANK.update(account=account)
        await ctx.send(f"__تم تصفير {member.mention}__")

  @commands.command(name="اضافة")
  async def add(self, ctx: commands.Context, types, user, amount):
    guild = ctx.guild
    role = guild.get_role(791680372966293504)
    if types == "فلوس":
      if role in ctx.author.roles:
        if '&' in user:
          # NOTE: its a role
          id = user[3:-1]
          role = guild.get_role(int(id))
          for i in role.members:
            if ~i.bot:
              if PROFILES_MANAGER.getProfileByMemberId(i.id) != False:
                account = BANK.getAccountById(PROFILES_MANAGER.getProfileByMemberId(i.id).getId())
                account.addCash(int(amount))
                account.addMoney(int(amount))
                BANK.update(account=account)
          await ctx.send(f'__تم اضافة مبلغ قدرة {amount} لجميع من يملك الرتبة {len(role.members)} شخص تم اعطائه__')
        else:
          id = user[2:-1]
          member = await self.bot.get_or_fetch_user(id)
          if PROFILES_MANAGER.getProfileByMemberId(member.id) != False:
            account = BANK.getAccountById(PROFILES_MANAGER.getProfileByMemberId(member.id).getId())
            account.addCash(int(amount))
            account.addMoney(int(amount))
            BANK.update(account=account)
            await ctx.send(f'__تم اعطائة مبلغ قدرة {amount}__')

  @commands.command(name='تجميد')
  async def freeze(self, ctx, user):
    if '&' in user:
      # NOTE: its a role
      id = user[3:-1]
      guild = ctx.message.guild
      role = guild.get_role(int(id))
      for i in role.members:
        if ~i.bot:
          if PROFILES_MANAGER.getProfileByMemberId(i.id) != False:
            account = BANK.getAccountById(PROFILES_MANAGER.getProfileByMemberId(i.id).getId())
            account.setFreeze(True)
            BANK.update(account=account)
      await ctx.send(f'__تم تجميد حسابات الاشخاص، تم تجميد {len(role.members)} حساب__')
    elif '@' in user:
      id = user[2:-1]
      member = await self.bot.get_or_fetch_user(id)
      if PROFILES_MANAGER.getProfileByMemberId(member.id) != False:
        account = BANK.getAccountById(PROFILES_MANAGER.getProfileByMemberId(member.id).getId())
        account.setFreeze(True)
        BANK.update(account=account)
        await ctx.send(f"__تم تجميد حساب {member.mention}__")

  @commands.command(name='إزالة')
  async def unfreeze(self, ctx, types, user):
    if types == "تجميد":
      if '&' in user:
        # NOTE: its a role
        id = user[3:-1]
        guild = ctx.message.guild
        role = guild.get_role(int(id))
        for i in role.members:
          if ~i.bot:
            if PROFILES_MANAGER.getProfileByMemberId(i.id) != False:
              account = BANK.getAccountById(PROFILES_MANAGER.getProfileByMemberId(i.id).getId())
              account.setFreeze(False)
              BANK.update(account=account)
        await ctx.send(f'__تم إزالة التجميد عن  الاشخاص التالية، تم إزالة {len(role.members)}__')
      elif '@' in user:
        id = user[2:-1]
        member = await self.bot.get_or_fetch_user(id)
        if PROFILES_MANAGER.getProfileByMemberId(member.id) != False:
          account = BANK.getAccountById(PROFILES_MANAGER.getProfileByMemberId(member.id).getId())
          if account.getFreeze() == True:
            account.setFreeze(False)
            BANK.update(account=account)
            await ctx.send(f"__تم إزالة تجميد حساب {member.mention}__")
          else:
            await ctx.send(f"__لم يتم تجميد {member.mention}__")

def setup(bot):
	bot.add_cog(bank(bot))