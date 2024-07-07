import datetime
import discord
import main
from discord.ext import commands
import random
import asyncio
import time
import pyperclip

math_plus = {"Stats": False, "total": 0, "startTime": 0, "amount": 0}


class Math(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.command("رياضيات")
    async def math_plus(self, ctx: commands.Context):
        if math_plus["Stats"] == True:
            await ctx.send("هناك جولة جارية")
            return
        random_number_one = random.randint(1, 100)
        random_number_two = random.randint(1, 100)
        total = random_number_one + random_number_two
        #list editing
        math_plus["Stats"] = True
        math_plus["total"] = total
        math_plus["startTime"] = time.strftime('%X')


        desc = f""">>> ```py
: تمتلك 15 ثانية للأجابة عن السؤال الآتي

    {random_number_one} + {random_number_two} = ?
```
        """

        #Embed message
        mathEmbed = discord.Embed(title="حاول الاجابة علي السؤال في اسرع وقت ممكن",description = desc, color = 65408, timestamp = datetime.datetime.utcnow())
        mathEmbed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
        mathEmbed.set_footer(text=f"{self.bot.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
        pyperclip.copy(total)
        await ctx.send(embed=mathEmbed)



        try:
            #wait until someone get the answer
            message = await self.bot.wait_for("message", check=lambda message: message.content == str(total), timeout=15)

            # if the message is correct send this embed
            answerEmbed = discord.Embed(color=65408, timestamp=datetime.datetime.utcnow())
            answerEmbed.title = f"**الفائز هو : {message.author.name}**"
            answerEmbed.description = f"{message.author.mention} أجابت على السؤال بشكل صحيح"
            answerEmbed.set_author(name = message.author.name, icon_url = message.author.avatar)
            answerEmbed.set_footer(text=f"{self.bot.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")

            #send the embed
            await ctx.send(embed=answerEmbed)

            #stop the game
            math_plus["Stats"] = False
        except asyncio.TimeoutError:
            #Embed message
            timoutEmbed = discord.Embed(color=65408, timestamp=datetime.datetime.utcnow())
            timoutEmbed.title = f"انتهي الوقت المحدد"
            timoutEmbed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
            timoutEmbed.set_footer(text=f"{self.bot.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
            
            #send message
            await ctx.send(embed=timoutEmbed)

            #stop the game
            math_plus["Stats"] = False



def setup(bot):
    bot.add_cog(Math(bot))