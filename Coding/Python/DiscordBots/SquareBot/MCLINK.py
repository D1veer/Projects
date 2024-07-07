import asyncio
import datetime
import discord
from discord.ext import commands
import mysql.connector
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")
# c = mysql.connector.connect(host='144.172.80.241',
#                             database='test',
#                             user='u20710_ewWNLyYwnV',
#                             password='SUkhKhXk9A8+c6y3RQ^.+!u1')

# print(c.is_connected())

# conn = c.cursor()
# sql = "DELETE FROM Users WHERE Name = 'xiled'"

# conn.execute(sql)

# c.commit()

# sql = "INSERT INTO Users (Name, id) VALUES (%s, %s)"
# val = ("yosef", 23223)
# conn.execute(sql, val)

# c.commit()

# conn.execute("SELECT * FROM Users")
# myresult = conn.fetchall()

# for x in myresult:
#     print(x)

connection = None

@client.command()
async def link(ctx, *, ID: int = 1):
    c = mysql.connector.connect(
        host='166.0.225.27',
        database='s20710_Minecraft_Discord',
        user='u20710_ewWNLyYwnV',
        password='SUkhKhXk9A8+c6y3RQ^.+!u1')
    conn = c.cursor()
    conn.execute(f"SELECT * FROM Users")
    myresult = conn.fetchall()
    print(myresult)
    await ctx.send(f"{myresult}")


@client.event
async def on_ready():
	print("Bot is ready!")
	# c = mysql.connector.connect(host='144.172.80.241',
	#     database='s20710_Minecraft_Discord',
	#     user='u20710_ewWNLyYwnV',
	#     password='SUkhKhXk9A8+c6y3RQ^.+!u1')
	# conn = c.cursor()
	# conn.execute("SELECT * FROM Users")
	# # sql = "INSERT INTO Users (Name, id) VALUES (%s, %s)"
	# # val = ("dive/er040", 123124214)
	# myresult = conn.fetchall()
	# # myresult = conn.execute(sql, val)
	# # c.commit()
	# print(myresult)
	# if 123124214 in myresult:
	#     print("found")
	# for i in myresult:
	#     print(i[1])
	#     if 123124214 == i[1]:
	#         print("found")
	#         break
	#     print(type(i))



# client.load_extension("Admin")
# client.load_extension("StaffCommands")
# client.load_extension("events")
# client.load_extension("VoiceCommands")
client.run("ODE2Nzg2MDUzMDI4NTExODA2.YEABSg.hVozpmO0aDQE7MDPrfV8Eqafaks")