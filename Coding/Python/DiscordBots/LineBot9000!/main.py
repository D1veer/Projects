import discord


bot = discord.Bot()
# bot.intents = discord.Intents.all()

channels = []

@bot.event
async def on_ready():
  print(f"{bot.user} is ready and online!")

@bot.slash_command(name="setup", description="Setup a channel for sending lines")
async def hello(ctx: discord.ApplicationContext, channel: discord.TextChannel):
  if channel == None:
    await ctx.send("Please Select a channel.")
    return
  
  print(channel.id)
  
  channels.append(channel.id)
  
@bot.event
async def on_message(message: discord.Message):
  if message.channel.id in channels and message.author.bot == False:
    await message.channel.send("Line")



bot.run("MTIzODkxMzA3NjgwODY1MDg3Mw.GmYiWH.OsCvY8T_FoDte21gbQYtL8V34AVaBbmg2od2kw") # run the bot with the token