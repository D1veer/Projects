import datetime
import discord
import main
from discord.ext import commands
import random
import asyncio

flag_var = {"Stats": False, "currentFlagID": "", "amount": 0}


class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("أعلام", aliases=["اعلام", "علام"])
    async def flags(self, ctx: commands.Context):
        if flag_var["Stats"] == True:
            await ctx.send("هناك جولة جارية")
            return
        cods = {
            "sa": "السعودية",
            "sd": "السودان",
            "sy": "سوريا",
            "kw": "الكويت",
            "ly": "ليبيا",
            "ma": "المغرب",
            "om": "عمان",
            "qa": "قطر",
            "eg": "مصر",
            "iq": "العراق",
            "lb": "لبنان",
            "mx": "المكسيك",
            "mr": "موريتانيا",
            "ru": "روسيا",
            "rs": "صربيا",
            "tn": "تونس",
            "ye": "اليمن",
            "so": "الصومال",
            "bh": "البحرين",
            "dz": "الجزائر",
            "ae": "الإمارات",
            "jo": "الأردن",
            "km": "جزر القمر‎",
            "dj": "جيبوتي",
            "ps": "فلسطين",
        }
        random_flag_id = random.choice(list(cods))
        flag_var["currentFlagID"] = cods[random_flag_id]
        flag_var["Stats"] = True

        flagImageLink = f"https://flagcdn.com/256x192/{random_flag_id}.png"

        desc = f""">>> ```py
: تمتلك 15 ثانية للأجابة عن السؤال الآتي
    ما هو اسم العلم ؟
```
        """

        #Embed message
        flagEmbed = discord.Embed(title="حاول الاجابة علي السؤال في اسرع وقت ممكن",description = desc, color = 65408, timestamp = datetime.datetime.utcnow())
        flagEmbed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
        flagEmbed.set_footer(text=f"{self.bot.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
        flagEmbed.set_image(flagImageLink)
        await ctx.send(embed=flagEmbed)



        try:
            #wait until someone get the answer
            message = await self.bot.wait_for("message", check=lambda message: message.content == str(main.flag_var["currentFlagID"]), timeout=15)

            # if the message is correct send this embed
            answerEmbed = discord.Embed(color=65408, timestamp=datetime.datetime.utcnow())
            answerEmbed.title = f"**الفائز هو : {message.author.name}**"
            answerEmbed.description = f"{message.author.mention} أجاب على السؤال بشكل صحيح"
            answerEmbed.set_author(name = message.author.name, icon_url = message.author.avatar)
            answerEmbed.set_footer(text=f"{self.bot.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")

            #send the embed
            await ctx.send(embed=answerEmbed)

            #stop the game
            flag_var["Stats"] = False
        except asyncio.TimeoutError:
            #Embed message
            timoutEmbed = discord.Embed(color=65408, timestamp=datetime.datetime.utcnow())
            timoutEmbed.title = f"انتهي الوقت المحدد"
            timoutEmbed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar)
            timoutEmbed.set_footer(text=f"{self.bot.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
            
            #send message
            await ctx.send(embed=timoutEmbed)

            #stop the game
            flag_var["Stats"] = False

def setup(bot):
    bot.add_cog(games(bot))