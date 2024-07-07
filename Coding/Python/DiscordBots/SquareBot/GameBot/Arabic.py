import datetime
import random
import discord
import main
from discord.ext import commands
import xlrd
import asyncio
import time
import pyperclip

arabic_list = {"Stats": False, "total": "", "startTime": 0, "amount": 0}
workbook = xlrd.open_workbook("words.xlsx")

worksheet = workbook.sheet_by_index(0)
print(worksheet.nrows)
newlist = {}
print(arabic_list)


class Arabic(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.command("عكس")
    async def arabic(self, ctx: commands.Context):
        if arabic_list["Stats"] == True:
            await ctx.send("هناك جولة جارية")
            return

        for i in range(worksheet.nrows):
            newlist.update({f"{worksheet.cell_value(i, 0)}": f"{worksheet.cell_value(i, 2)}"})

        print(len(newlist))
        id = random.choice(list(newlist))
        #list editing
        arabic_list["Stats"] = True
        arabic_list["total"] = newlist[id]
        arabic_list["startTime"] = time.strftime('%X')
        print(newlist[id])

        desc = f""">>> ```py
: تمتلك 15 ثانية للأجابة عن السؤال الآتي
    عكس كلمة {id} ؟
```
        """

        #Embed message
        arabicEmbed = discord.Embed(title="حاول الاجابة علي السؤال في اسرع وقت ممكن",description = desc, color = 65408, timestamp = datetime.datetime.utcnow())
        arabicEmbed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
        arabicEmbed.set_footer(text=f"{self.bot.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
        pyperclip.copy(newlist[id])
        await ctx.send(embed=arabicEmbed)



        try:
            #wait until someone get the answer
            message = await self.bot.wait_for("message", check=lambda message: message.content == str(newlist[id]), timeout=15)

            # if the message is correct send this embed
            answerEmbed = discord.Embed(color=65408, timestamp=datetime.datetime.utcnow())
            answerEmbed.title = f"**الفائز هو : {message.author.name}**"
            answerEmbed.description = f"{message.author.mention} أجابت على السؤال بشكل صحيح"
            answerEmbed.set_author(name = message.author.name, icon_url = message.author.avatar)
            answerEmbed.set_footer(text=f"{self.bot.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")

            #send the embed
            await ctx.send(embed=answerEmbed)

            #stop the game
            arabic_list["Stats"] = False
        except asyncio.TimeoutError:
            #Embed message
            timoutEmbed = discord.Embed(color=65408, timestamp=datetime.datetime.utcnow())
            timoutEmbed.title = f"انتهي الوقت المحدد"
            timoutEmbed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
            timoutEmbed.set_footer(text=f"{self.bot.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
            
            #send message
            await ctx.send(embed=timoutEmbed)

            #stop the game
            arabic_list["Stats"] = False



def setup(bot):
    bot.add_cog(Arabic(bot))