import os
from discord.ext import commands
import discord
from dataclasses import dataclass
from typing import Literal

def main():
    print("Starting")
    if True:
        print("Starting x2")
    
    
    path: Literal['/project/assets/databases/Members.json'] = '/project/assets/databases/Members.json'
    print(path)

main()

# @dataclass
# class Account():
#     id: str
#     cash: int
#     blance: int = 1_000

#     def have_cash(self) -> bool:
#         if self.cash > 0:
#             return True


# account = Account('1', 1_000)

# account.id = '123323'

# print(account)


# intents = discord.Intents.default()
# intents.members = True
# client: discord.Bot = commands.Bot(command_prefix="!", intents=intents)
# client.remove_command("help")
# print(client.status)

# sdawd = 'awdwadwa'


# @client.event
# async def on_ready():
#     print(f"{client.user} has connected to Discord!")


# async def get_member(member):
#     if isinstance(member, discord.Member) or isinstance(member, discord.User):
#         return member
#     if member is int:
#         member = await client.fetch_user(member)
#     if member is str:
#         # TODO: check if member linked minecraft account with discord and get it
#         if member[-1] == ">":
#             acmember = member.replace(">", "")
#             acmember = acmember.replace("<", "")
#             acmember = acmember.replace("@", "")
#             print(acmember)
#             member = await client.fetch_user(int(acmember))
#     return member

# for filename in os.listdir("./project/commands"):
#     if filename.endswith(".py"):
#         client.load_extension(f"project.commands.{filename[:-3]}")

# client.run("OTgxMzMzODA5NjE2Mjg1NzM2.GbjwxF.AHw09shBZB7zov-WxipizREuZvBuEevXjhQf9A")
