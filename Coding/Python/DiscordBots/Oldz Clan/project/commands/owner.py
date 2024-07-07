import contextlib
import io
from sys import stdout
from traceback import format_exception
from discord.ext import commands
import discord
import textwrap

owners = [685820797834493964, 619340445692067890]

# to expose to the eval command
import datetime
from collections import Counter

class Admin(commands.Cog):
	"""Admin-only commands that make the bot dynamic."""

	def __init__(self, bot: discord.Bot):
		self.bot = bot

	@commands.command(hidden=True)
	async def load(self, ctx, *, module : str):
		if ctx.author.id == 619340445692067890 or ctx.author.id == 685820797834493964:
			pass
		else:
			return await ctx.send('Only Diveer (Bot Maker), ! W (The Owner and the best)')
		"""Loads a module."""
		try:
			self.bot.load_extension(f"project.commands.{module}")
		except Exception as e:
			await ctx.reply('\N{PISTOL}')
			await ctx.reply('{}: {}'.format(type(e).__name__, e))
		else:
			await ctx.reply('\N{OK HAND SIGN}')

	@commands.command(hidden=True)
	async def unload(self, ctx, *, module : str):
		if ctx.author.id == 619340445692067890 or ctx.author.id == 685820797834493964:
			pass
		else:
			return await ctx.send('Only Diveer (Bot Maker), ! W (The Owner and the best)')
		"""Unloads a module."""
		try:
			self.bot.unload_extension(f"project.commands.{module}")
		except Exception as e:
			await ctx.reply('\N{PISTOL}')
			await ctx.reply('{}: {}'.format(type(e).__name__, e))
		else:
			await ctx.reply('\N{OK HAND SIGN}')

	@commands.command(name='reload', hidden=True)
	async def _reload(self, ctx, *, module : str):
		if ctx.author.id == 619340445692067890 or ctx.author.id == 685820797834493964:
			pass
		else:
			return await ctx.send('Only Diveer (Bot Maker), ! W (The Owner and the best)')
		"""Reloads a module."""
		try:
			self.bot.unload_extension(f"project.commands.{module}")
			self.bot.load_extension(f"project.commands.{module}")
		except Exception as e:
			await ctx.reply('\N{PISTOL}')
			await ctx.reply('{}: {}'.format(type(e).__name__, e))
		else:
			await ctx.reply('\N{OK HAND SIGN}')

	@commands.command(pass_context=True, hidden=True, aliases=["exe", "elva", "run"])
	async def debug(self, ctx: commands.Context, *, code : str):
			"""Evaluates code."""
			if ctx.author.id == 619340445692067890 or ctx.author.id == 685820797834493964:
					if code.startswith("```") and code.endswith("```"):
							code = code[5:-3]
							code.replace("py", "")
					# python = '```py\n{}\n```'
					# result = None

					local_vars = {
							'bot': self.bot,
							'ctx': ctx,
							'message': ctx.message,
							'channel': ctx.channel,
							'author': ctx.author,
							"discord": discord,
							"commands": commands,
							"guild": ctx.guild,
					}

					stdout = io.StringIO()
					try:
							with contextlib.redirect_stdout(stdout):
									exec(f"async def func():\n{textwrap.indent(code, '    ')}", local_vars,)

									obj = await local_vars["func"]()
									result_of_code = f"{stdout.getvalue()}\n-- {obj}\n"
					except Exception as e:
							result_of_code = "".join(format_exception(e, e, e.__traceback__))

					embed=discord.Embed(title="Exuctued", description=f">>> ```py\n{result_of_code}```", color=3978097)
					#embed.set_footer(text="Made With ❤️ By Diveer#1059")
					await ctx.send(embed=embed)

			else:
				await ctx.send("**You are not the owner of the bot.**")

def setup(bot):
		bot.add_cog(Admin(bot))