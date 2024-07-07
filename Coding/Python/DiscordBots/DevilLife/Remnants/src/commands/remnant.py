from datetime import datetime
import discord
from discord.ext import commands
from src.classes.Remnant import Remnant, RM, Type
from tinydb import Query, TinyDB  

class remnant(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot = bot
    self.data: TinyDB = TinyDB('remnants.json', indent=2, separators=(',', ': '))

  @commands.command("اضافة-مخالفه")
  async def createOne(self, ctx: commands.Context, name: str=None, price: int=None, type: str=None):
    def check(message):
      return message.author.id == ctx.author.id
    embed: discord.Embed = discord.Embed(title='** اسم المخالفه :**')
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
    # embed.set_author(ctx.author.name)
    await ctx.send(embed=embed)
    name: discord.Message = await self.bot.wait_for('message', check=check, timeout=10)
    print("📢[remnant.py:20]: ", name)
    embed.title = '** سعر المخالفه :**'
    await ctx.send(embed=embed)
    price = await self.bot.wait_for('message', check=check, timeout=10)
    print("📢[remnant.py:23]: ", price)
    embed.title = '** نوع المخالفه :**'
    await ctx.send(embed=embed)
    type = await self.bot.wait_for('message', check=check, timeout=10)
    
    if name.content == None:
      return await ctx.send('(الاسم) اكمل الفراغات')
    if price.content == None:
      return await ctx.send('(السعر) اكمل الفراغات')
    if type.content == None:
      return await ctx.send('(النوع | مرورية | سرقة) اكمل الفراغات')
    global new
    if type.content == 'مرورية':
      new = Remnant(999, name.content, price.content, Type.R1)
    elif type.content == 'سرقة':
      new = Remnant(999, name.content, price.content, Type.R2)
    if not new in RM.getRemnants():
      can_add = RM.getRemnantsByType(new.type)
      if len(can_add) == 25:
        await ctx.send('المخلفات ممتلئة')
        return
      RM.addRemnant(new)
      await ctx.send('تم الاضافه')
    else:
      await ctx.send('المخالفة مسجله مسبقًا')
  
  @commands.command("مخالفه")
  async def my_money(self, ctx: commands.Context, member: discord.Member = None):
    if member == ctx.author:
      return False
    if member is None:
      return await ctx.send('**.. منشن لاعب**')
    global message_to_delete
    async def select_callback(asd: discord.Interaction):
      global b
      global select_list_new
      
      if(ctx.author != asd.user):
        return False
      b = asd
      if select_list.values[0] == 'السرقات':
        select_list_new = discord.ui.Select(
          custom_id="1",
          max_values=len(RM.getRemnantsByType(Type.R2)),
          placeholder = 'قم باختيار مخالفة سرقه',
          options = [discord.SelectOption(label=i.title, description=str(i.cash)) for i in RM.getRemnantsByType(Type.R2)]
        )
      else:
        # emoji = discord.utils.get(self.bot.emojis, name='emoji_4')
        emoji = '📄'
        select_list_new = discord.ui.Select(
          custom_id='2',
          max_values=len(RM.getRemnantsByType(Type.R1)),
          placeholder = 'قم باختيار المخالفه المرورية',
          options = [discord.SelectOption(label=f'{i.title}', emoji=emoji, description=f'السعر : {i.cash} ريال') for i in RM.getRemnantsByType(Type.R1)]
        )
      view: discord.ui.View = discord.ui.View(select_list_new)
      select_list_new.callback = select_callback_2
      await asd.response.edit_message(view=view)
    
    async def select_callback_2(interaction: discord.Interaction):
      prices = [RM.getRemnantByName(n.replace(' ✅', '')).cash for n in select_list_new._selected_values]
      await ctx.message.delete()
      await b.message.delete()
      
      remnants = '\n'.join(['       - ' + n.replace(' ✅', '') for n in select_list_new._selected_values])
      
      User = Query()
      test = self.data.search(User.id == member.id)
      if test:
        count =  test[0]["count"] + 1
        print("📢[remnant.py:54]: ", count)
        self.data.update({'count': count}, User.id == member.id)
      else:
        print('added')
        self.data.upsert({'id': member.id, 'count': 1}, User.id == member.id)
        count = 1
      
      
      des = f"""   **     | مخالفة    

      | العسكري : <@!{ctx.author.id}>

      | تم مخالفة <@!{member.id}> بقيمة {sum(prices)} ريال

      | المخالفة : \n{remnants}

      | رقم المخالفة : {count}

      | وزارة الداخلية 
      | وزارة المالية**"""
      await interaction.channel.send(des)
      
      des1 = """
        | رسالة واردة من قبل الوزارة الداخلية 

        | عزيزي المواطن : 

        | لقد تم مخالفتك بقيمة 

        | المخالفه : 

        | رقم المخالفة :

        | وزارة الداخلية 
        | ديفل لايف
      """

    
    select_list: discord.ui.Select = discord.ui.Select(
      placeholder = 'قم بأختيار نوع المخالفات',
      options = [discord.SelectOption(label='مخالفات المرور', description='اي مخالفة لها علاقه بالمرور: السرعه، قطع اشاره الخ.'),
      discord.SelectOption(label='السرقات', description='اي نوع سرقه: سرقه بقاله، سرقه بنك الخ...')],
    )
    select_list.callback = select_callback
    
    view: discord.ui.View = discord.ui.View(select_list)
    
    await ctx.send(view = view)


def setup(bot):
	bot.add_cog(remnant(bot))