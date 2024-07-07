# from rcon.source import rcon
# from project.config import RCON_IP, RCON_PASS, RCON_PORT, SERVER_ID
# from discord.ext import commands
# import discord
# from ..utils import utils

# class rconmc(commands.Cog):
#   def __init__(self, bot: discord.Bot):
#     self.bot = bot

#   # @commands.command(name='pl', aliases=["plugins", 'plugin'])
#   # async def plugins(self, ctx: commands.Context):
#   #   response = await rcon(
#   #     'pl',
#   #     host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
#   #   await ctx.send(response)

#   @commands.slash_command(guild_ids=[SERVER_ID],
#   name='tag',
#   description='Acceses The Tag Manager',
#   options=[discord.Option(str, name='condition', choices=['unlock', 'lock']), discord.Option(str, name='playername'), discord.Option(str, name='tagname', choices=['Tiktok', "Insta"])])
#   async def tag(self, ctx: discord.ApplicationContext, condition, PlayerName, TagName):
#     if(condition == 'unlock'):
#       if not utils.is_staff(ctx.author): return await ctx.send("Your Aren't Staff!")
#       response = await rcon(
#         'tag', 'unlock', f'{TagName}', f'{PlayerName}',
#         host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
#       await ctx.respond(f'Player [{PlayerName}] Has Recive a Tag [{TagName}]. \n Recvied Output: {response}')

#   @commands.command(name="players", aliases=["mcplayers", 'list', 'mc', 'pl'])
#   async def players(self, ctx: commands.Context):
#     response = await rcon(
#       'list',
#       host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
#     index = response.find("\n")
#     response = response[index + 1:]
#     newList = response.split(",")
#     member_string = utils.msgToList(newList)
#     await ctx.send(member_string + f" {len(newList)} Player(s)")

#   async def run_command(command):
#     response = await rcon(
#       f'{command}',
#       host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
#     return response

#   @commands.command(name='kick', aliases=['k'])
#   async def kick(self, ctx: commands.Context, plrName: str=None, *, reason="No Reason"):
#     pass
#     # * check if the sender is staff
#     if not utils.is_staff(ctx.author): return await ctx.send("Your Aren't Staff!")

#     #  * check if the player name passed
#     if plrName == None: return await ctx.send("Please Type Player Name!")

#     # * check if the member linked or not
#     plrName = utils.get_member(plrName)
#     if plrName == None: return await ctx.send("Member is not linked...")

#     try:
#       response = await rcon(
#         'kick', f'{plrName}', reason,
#       host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
#       if response == "":
#         await ctx.send(f"{plrName} Has Been Kicked For {reason}")
#       else:
#         await ctx.send(response)
#     except Exception as e:
#       if isinstance(e, discord.errors.HTTPException):
#         await ctx.send(f"{plrName} Has Been Kicked For {reason}")
#       else:
#         await ctx.send(e)

#   # @commands.command(name='link', aliases=['linkmc'])
#   # async def link(self, ctx: commands.Context, id):
#   #   response = await rcon(
#   #     'check', f'{id}',
#   #     host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
#   #   # await ctx.send(response)
#   #   if response == "False":
#   #     pass
#   #   else:
#   #     db.insert({"id": ctx.author.id, 'ign': response})
#   #     await ctx.send(f"Linked as {response}")

#   # @commands.command(name="usermc")
#   # async def usermc(self, ctx, member: discord.Member):
#   #   User = Query()
#   #   re = db.search(User.id == member.id)
#   #   if User:
#   #     print(re[0]["ign"])
#   #   await ctx.send(re[0]["ign"])

#   @commands.command(name='rcon', aliases=['r'])
#   async def rcon(self, ctx: commands.Context, *message):
#     if not utils.is_staff(ctx.author): return await ctx.send("Your Aren't Staff!")
#     # if ctx.author.id != 619340445692067890:
#       # return await ctx.send("only my maker diveer (dodo)")
#     await ctx.send(message)
#     for msg in message:
#       if ' ' in msg:
#         y = list(message)
#         y.remove(msg)
#         y.append(f'"{msg}"')
#         message = tuple(y)
#     try:
#       response = await rcon(
#         *message,
#       host=RCON_IP, port=RCON_PORT, passwd=RCON_PASS)
#       await ctx.send(response)
#     except Exception as e:
#       if isinstance(e, discord.errors.HTTPException):
#         await ctx.send("The command run successfully")
#       else:
#         await ctx.send(e)

# def setup(bot):
#   bot.add_cog(rconmc(bot))