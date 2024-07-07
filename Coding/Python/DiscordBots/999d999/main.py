import json
import asyncio
import time

import requests
import discord
from discord.ext import commands

with open('config.json') as f:
	config = json.load(f)
	print(config[ 'user_token' ])

with open('ids.txt') as f:
	ids = f.read().splitlines()

if len(ids) == 0:
	print('No IDs found in ids.txt')
	input("\nPress enter to exit...")
	exit(1)
elif config[ 'user_token' ] == '':
	print('No token found in config.json')
	input("\nPress enter to exit...")
	exit(1)
elif config[ 'cooldown-seconds' ] == '':
	print('No cooldown-seconds found in config.json')
	input("\nPress enter to exit...")
	exit(1)
elif config[ 'loops' ] == '':
	print('No loops found in config.json')
	input("\nPress enter to exit...")
	exit(1)

bot = commands.Bot(command_prefix='.', self_bot=True)
delay = [ ]


@bot.event
async def on_ready():
	print("Logged in as: " + bot.user.name)
	Seconds = 1

	loops = config[ 'loops' ]
	for _ in range(int(loops)):

		for id in ids:
			channel = bot.get_channel(int(id))
			try:
				if channel is None:
					print(f"\nChannel with ID {id} not found.")
					continue
				if channel.slowmode_delay == 0:
					await channel.send(config[ 'message' ])
				else:
					if not delay:
						delay.append([ channel.id, Seconds ])
					for info in delay:
						if channel.id in info:
							left_time = Seconds - info[1]
							if left_time >= channel.slowmode_delay:
								await channel.send(config[ 'message' ])
								delay.pop(delay.index(info))
								delay.append([ channel.id, Seconds ])
						else:
							delay.append([ channel.id, Seconds ])
							continue
					# if Seconds % channel.slowmode_delay == 0:
					# 	await channel.send(config[ 'message' ])
			except Exception as e:
				print(f"Error sending message to channel: {e}")
				if '403' in e:
					if id in ids:
						ids.remove(id)
				continue

			print(f"\nSent message to channel: {channel.name}")
			print(f"Guild: {channel.guild.name}\nWaiting {config[ 'cooldown-seconds' ]} seconds...")
			Seconds = Seconds + 1
			await asyncio.sleep(int(config[ 'cooldown-seconds' ]))
			Seconds = Seconds + 2
		else:
			print("\nFinished sending messages to all channels.")


bot.run(config[ 'user_token' ])
