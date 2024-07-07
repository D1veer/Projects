import datetime
import discord
from discord.ext import commands
import json
import VoiceCommands
import main

Voice_Members = {}
shutuped = []
Voice_Members_seconds = {}
XP_chat_dir = r"./STUFF/databases/XP_chat.json"
XP_voice_dir = r"./STUFF/databases/XP_voice.json"

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_message_delete(self, message):
		VoiceCommands.VoiceCommands.append_to_list(message.author, message)
		print(message.author, message)

def setup(bot):
	bot.add_cog(Events(bot))
