from ast import Str
from dis import dis
from typing import Optional
import discord
from discord.ext import commands
import Procedure

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")


procedureMananger = Procedure.ProcedureManager()

@client.command(name="add", aliases=["new", "create"])
async def procedure_def_add(ctx: commands.Context, member, reason, procedure, duration):
  attamnts = []
  for i in ctx.message.attachments:
    attamnts.append(i.url)
  print(member, reason, procedure, duration, attamnts, ctx.author)
  procedure = Procedure.Procedure(ctx.author, member, reason, procedure, duration, procedureMananger.get_procedure_count(), attamnts)
  procedureMananger.add_procedure(procedure)

  await ctx.send(f"{ctx.author.mention} added a procedure for {member}.")

  # send procedure embed
  embed = discord.Embed(title = f"Procedure {procedure.get_id()}", description = f"{procedure.get_member()}", color = 0x00ff00, timestamp=procedure.get_time())
  embed.add_field(name = "Staff", value = f"{procedure.get_staff()}", inline = True)
  embed.add_field(name = "Reason", value = f"{procedure.get_reason()}", inline = True)
  embed.add_field(name = "Procedure", value = f"{procedure.get_procedure()}", inline = True)
  embed.add_field(name = "Duration", value = f"{procedure.get_duration()}", inline = True)
  embed.add_field(name = "Attachments", value = f"{procedure.get_attachments()}", inline = True)
  embed.set_footer(text=f"{client.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
  await ctx.send(embed = embed)

@client.command(name="get", aliases=["show"])
async def procedure_def_get(ctx: commands.Context, type, text):
  await ctx.send(f"Getting Procedure by {type} with {str(text)}")
  if type == "id":
    procedure = procedureMananger.get_procedure_by_id(int(text))
    if procedure is None:
      await ctx.send(f"{ctx.author.mention} no procedure with id {text}.")
    else:
      # send procedure embed
      embed = discord.Embed(title = f"Procedure {procedure.get_id()}", description = f"{procedure.get_member()}", color = 0x00ff00, timestamp=procedure.get_time())
      embed.add_field(name = "Staff", value = f"{procedure.get_staff()}", inline = True)
      embed.add_field(name = "Reason", value = f"{procedure.get_reason()}", inline = True)
      embed.add_field(name = "Procedure", value = f"{procedure.get_procedure()}", inline = True)
      embed.add_field(name = "Duration", value = f"{procedure.get_duration()}", inline = True)
      embed.add_field(name = "Attachments", value = f"{procedure.get_attachments()}", inline = True)
      embed.set_footer(text=f"{client.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
      await ctx.send(embed = embed)
  elif type == "member":
    # FIXME: member is not a member and not found
    procedure = procedureMananger.get_procedure_by_member(text)
    print(text, procedureMananger.get_procedure_by_member(text))
    if procedure is None:
      await ctx.send(f"{ctx.author.mention} no procedure for {text}.")
    else:
      # send procedure embed
      embed = discord.Embed(title = f"Procedure {procedure.get_id()}", description = f"{procedure.get_member()}", color = 0x00ff00, timestamp=procedure.get_time())
      embed.add_field(name = "Staff", value = f"{procedure.get_staff()}", inline = True)
      embed.add_field(name = "Reason", value = f"{procedure.get_reason()}", inline = True)
      embed.add_field(name = "Procedure", value = f"{procedure.get_procedure()}", inline = True)
      embed.add_field(name = "Duration", value = f"{procedure.get_duration()}", inline = True)
      embed.add_field(name = "Attachments", value = f"{procedure.get_attachments()}", inline = True)
      embed.set_footer(text=f"{client.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
      await ctx.send(embed = embed)
  elif type == "staff":
    newText = text.replace("<", " ")
    newText = newText.replace(">", " ")
    newText = newText.replace("@", " ")
    if "!" in newText:
      newText = newText.replace("!", " ")
    staff = client.get_user(int(newText))
    procedure = procedureMananger.get_procedure_by_staff(staff)
    if procedure is None:
      await ctx.send(f"{ctx.author.mention} no procedure for {staff}.")
    else:
      # send procedure embed
      embed = discord.Embed(title = f"Procedure {procedure.get_id()}", description = f"{procedure.get_member()}", color = 0x00ff00, timestamp=procedure.get_time())
      embed.add_field(name = "Staff", value = f"{procedure.get_staff()}", inline = True)
      embed.add_field(name = "Reason", value = f"{procedure.get_reason()}", inline = True)
      embed.add_field(name = "Procedure", value = f"{procedure.get_procedure()}", inline = True)
      embed.add_field(name = "Duration", value = f"{procedure.get_duration()}", inline = True)
      embed.add_field(name = "Attachments", value = f"{procedure.get_attachments()}", inline = True)
      embed.set_footer(text=f"{client.get_guild(692158495235112972).name}", icon_url=f"https://cdn.discordapp.com/icons/692158495235112972/a_6f1d135f835b9db06660961952575a23.gif?size=4096")
      await ctx.send(embed = embed)

@client.event
async def on_ready():
	print("Bot is ready!")


client.run("ODE2Nzg2MDUzMDI4NTExODA2.YEABSg.hVozpmO0aDQE7MDPrfV8Eqafaks")