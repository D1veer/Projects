import discord
import main
from discord.ext import commands
import time

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith("-"):
            return

        if(main.math_plus["Stats"] == True):
            if(message.content == str(main.math_plus["total"])):
                await message.channel.send("أحسنت {}".format(message.author.mention))
                main.math_plus["Stats"] = False

        if(main.flag_var["Stats"] == True):
            if(message.content == str(main.flag_var["currentFlagID"])):
                await message.channel.send(f"صحيح {message.author.mention}")
                main.flag_var["Stats"] = False
                main.math_plus["amount"] += 1

def setup(bot):
    bot.add_cog(events(bot))