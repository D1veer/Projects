import discord
from discord.ext import commands
# from ..config import SERVER_ICON, SERVER_ID
from .Bank.Bank import bank, Account
import random

sniped_messages = {}

class casino(commands.Cog):
	def __init__(self, bot: discord.Bot):
		self.bot = bot

	@commands.command('قمار')
	async def gamble(self, ctx: discord.context.ApplicationContext, amount: int = None):
		if amount != None:
			account = bank.getAccountById(ctx.author.id)
			if account != None:
				multi = random.randint(2, 4)
				newAmount = amount * multi
				account.addMoney(newAmount)
				bank.update(account)
				await ctx.send(f'لقد ربحت {newAmount} \n فلوسك حاليًا: {account.getMoney()}')
			else:
				account = Account(str(ctx.author.id), 0, False)
				bank.addAccount(account)
				multi = random.randint(2, 4)
				newAmount = amount * multi
				account.addMoney(newAmount)
				bank.update(account)
				await ctx.send(f'لقد ربحت {newAmount} \n فلوسك حاليًا: {account.getMoney()}')
		else:
			await ctx.send(f'الرجاء ادخال مبلغ للقمار...')
	
	@commands.slash_command(guild_ids=[816363645671571517], name="money")
	async def myMoney(self, ctx: discord.ApplicationContext):
		account = bank.getAccountById(str(ctx.author.id))
		if account != None:
			await ctx.send(f'فلوسك: {account.getMoney()}')
		else:
			account = Account(str(ctx.author.id), 0, False)
			bank.addAccount(account)
			await ctx.send(f'فلوسك: {account.getMoney()}')

	@commands.command('نرد')
	async def dice(self, ctx: discord.context.ApplicationContext, amount: int):
		if amount != None:
			account = bank.getAccountById(str(ctx.author.id))
			if account == None:
				account = Account(str(ctx.author.id), 0, False)
				bank.addAccount(account)
			if account != None:
				win = random.randint(0, 1)
				if win == 1:
					newAmount = amount * 2
					account.addMoney(newAmount)
					bank.update(account)
					await ctx.send(f'فزت علي، ربحت {newAmount}، فلوسك الحين: {account.getMoney()} ')
				else: # otherwise
					account.delMoney(amount)
					bank.update(account)
					await ctx.send(f'فزت عليك يالسبك، فلوسك الحين: {account.getMoney()}')

	@commands.command('راتب')
	async def job(self, ctx: discord.context.ApplicationContext):
		amount = random.randint(1, 3000)
		account = bank.getAccountById(str(ctx.author.id))

		if account == None:
			account = Account(str(ctx.author.id), 0, False)
			bank.addAccount(account)
		account.addMoney(amount)
		bank.update(account=account)
		await ctx.send(f'تم إضافه مبلغ قدره: {amount}')
	
	@commands.command('قرض')
	async def job(self, ctx: discord.context.ApplicationContext):
		amount = 100000
		account = bank.getAccountById(str(ctx.author.id))

		if account == None:
			account = Account(str(ctx.author.id), 0, False)
			bank.addAccount(account)
		account.addMoney(amount)
		bank.update(account=account)
		await ctx.send(f'تم إضافه مبلغ قدره: {amount}')





def setup(bot):
	bot.add_cog(casino(bot))
